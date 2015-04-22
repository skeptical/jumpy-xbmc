import __builtin__, os, sys, atexit, traceback, re, types, marshal
import jumpy
from xml.etree.ElementTree import ElementTree, fromstring
from xml.dom.minidom import parseString
from xml.sax.saxutils import escape, unescape
from itertools import groupby
from urlparse import urlparse
from UserDict import IterableUserDict, DictMixin
from importlib import import_module
try: import simplejson as json
except: import json

__builtin__.got_soup = False
try:
	from bs4 import BeautifulSoup
	# bs4 won't parse xml without lxml: https://bugs.launchpad.net/beautifulsoup/+bug/1181589
	import lxml
	got_soup = 4
	def xmlsoup(f): return BeautifulSoup(open(f).read(), 'xml')
except:
	try:
		from BeautifulSoup import BeautifulStoneSoup
		got_soup = 3
		def xmlsoup(f): return BeautifulStoneSoup(open(f).read())
	except: pass
pms.log('using %s to parse xml' % ('minidom' if not got_soup else 'beautifulsoup%s' % got_soup), once=True)

version = '0.3.12'

def resolve_xbmc():
	xbmc_main = os.getenv('xbmc_main') if 'xbmc_main' in os.environ else pms.getProperty('xbmc.main.path')
	if xbmc_main:
		try:
			name = re.compile(r'.*(KODI|kodi|XBMC|xbmc).*').match(xbmc_main).group(1)
			return (name, xbmc_main)
		except:
			xbmc_main = None
	if sys.platform.startswith('linux'):
		for name in ['kodi', 'xbmc']:
			# FIXME: this won't find xbmc if it's installed to another prefix
			for d in ['/usr/local/share', '/usr/share']:
				path = os.path.join(d, name)
				if os.path.exists(path):
					return (name, path)
	elif sys.platform.startswith('win32'):
		programfiles = (os.getenv('PROGRAMFILES(X86)') if 'PROGRAMFILES(X86)' in os.environ \
			else os.getenv('PROGRAMFILES'))
		for name in ['KODI', 'XBMC']:
			path = os.path.join(programfiles, name)
			if os.path.exists(path):
				return (name, path)
	elif sys.platform.startswith('darwin'):
		for name in ['KODI', 'XBMC']:
			path = os.path.join('/Applications/XBMC.app/Contents/Resources', name)
			if os.path.exists(path):
				return (name, path)
	return (name, path)

try: _special
except NameError:
	__builtin__._special = {}
	xbmc_name, xbmc_main = resolve_xbmc()
	xbmc_home = os.getenv('xbmc_home') if 'xbmc_home' in os.environ else pms.getProperty('xbmc.home.path')
	if not xbmc_home:
		xbmc_home = pms.getProperty('xbmc.path')
	_special['xbmc'] = xbmc_main
	_special['xbmc_name'] = xbmc_name.lower()
	if sys.platform.startswith('linux'):
		_special['xbmcbin'] = _special['xbmc'].replace('share', 'lib')
		_special['home'] = xbmc_home if xbmc_home else os.getenv('HOME') + '/.' + xbmc_name
		_special['userhome'] = _special['home']
		_special['temp'] = _special['home'] + '/temp'
		_special['logpath'] = _special['temp']
		os.environ['OS'] = 'linux'
	elif sys.platform.startswith('win32'):
		_special['xbmcbin'] = _special['xbmc']
		_special['home'] = xbmc_home if xbmc_home else os.getenv('APPDATA') + '\\' + xbmc_name
		_special['userhome'] = os.getenv('USERPROFILE')
		_special['temp'] = _special['home'] + '\\cache'
		_special['logpath'] = _special['home']
		os.environ['OS'] = 'win32'
	elif sys.platform.startswith('darwin'):
		_special['xbmcbin'] = _special['xbmc']
		_special['home'] = xbmc_home if xbmc_home else os.getenv('HOME') + '/Library/Application Support/' + xbmc_name
		_special['userhome'] = _special['home']
		_special['temp'] = os.getenv('HOME') + '.' + xbmc_name + '/temp'
		_special['logpath'] = os.getenv('HOME') + '/Library/Logs'
		os.environ['OS'] = 'darwin'
	mprofile = os.path.join(_special['home'], 'userdata')
	_special['masterprofile'] = mprofile
	_special['profile'] = mprofile # FIXME: actually special://masterprofile/profile_name
#	_special['subtitles'] = #TODO: user-defined
	_special['userdata'] = mprofile
	_special['database'] = os.path.join(mprofile, 'Database')
	_special['thumbnails'] = os.path.join(mprofile, 'Thumbnails')
#	_special['recordings'] = #TODO: user-defined
#	_special['screenshots'] = #TODO: user-defined
	_special['musicplaylists'] = os.path.join(_special['profile'], 'playlists', 'music')
	_special['videoplaylists'] = os.path.join(_special['profile'], 'playlists', 'video')
#	_special['cdrips'] = #TODO: user-defined
#	_special['skin'] = # ?

	__builtin__.force_resolve = [x.strip() for x in os.getenv('force_resolve', '').split('\n')]

def unesc(s):
	return unescape(s, {"&apos;": "'", "&quot;": '"'})

def quickesc(file):
	# for some reason xbmc xml files allow unescaped ampersands
	return unescape(open(file).read()).replace('&','&amp;')

def parsexml(xml):
	if not xml or xml.isspace():
		xml = '<null/>'
	try:
		return parseString(xml)
	except:
		# it's likely latin1 without a header
		return parseString(jumpy.decode(xml).encode('utf-8'))

have_xbmc = False

def read_xbmc_settings():
	global have_xbmc
	_settings['xbmc'] = {}
	_settings['xbmc'][u'theme'] = 0
	lang = os.getenv('xbmc_lang')
	if lang is None:
		guisettings = os.path.join(_special['userdata'], 'guisettings.xml')
		if os.path.isfile(guisettings):
			have_xbmc = True
			print "Reading", guisettings
			try:
				xml = ElementTree(fromstring(quickesc(guisettings)))
				lang = xml.find('./locale/language').text
			except: pass
		if lang is None: lang = 'English'
		pms.setEnv('xbmc_lang', lang)
	_settings['xbmc'][u'language'] = lang

class masked(str):
	# a str that hides its repr (e.g. in a dict printout)
	def __repr__(self):
		return '\'####\''

sensitive = re.compile('pass|pw|user')

def read_settings(id):
	_settings[id] = {}
	for f in [
				os.path.join(_info[id]['path'], 'resources', 'settings.xml'),
				os.path.join(_special['userdata'], 'addon_data', id, 'settings.xml')
			]:
		if os.path.isfile(f):
			print "Reading", f
			if got_soup:
				xml = xmlsoup(f)
				for tag in xml.findAll('setting'):
					key = tag.get('id')
					if key:
						val = tag.get('value' if 'value' in tag.attrs else 'default') or ''
						if not val == '' and sensitive.search(key.lower()):
							val = masked(val)
						_settings[id][key] = val
			else:
				xml = parsexml(quickesc(f))
				for tag in xml.getElementsByTagName('setting'):
					key = tag.getAttribute('id')
					val = unesc(tag.getAttribute('value') if tag.hasAttribute('value') else tag.getAttribute('default'))
					if not val == '' and sensitive.search(key.lower()):
						val = masked(val)
					_settings[id][key] = val

def save_settings(id):
	print 'Saving settings: %s' % id
	xml = ['<settings>']
	for k in sorted(_settings[id].keys()):
		if k: xml.append('	<setting id="%s" value="%s" />' % \
			(k, escape(_settings[id][k], {"'": "&apos;", '"': "&quot;"})))
	xml.append('</settings>')
	open(os.path.join(_special['userdata'], 'addon_data', id, 'settings.xml'), 'w') \
		.write('\n'.join(xml))

changed = set()

def done():
	global changed
	for id in changed:
		save_settings(id)

atexit.register(done)

def read_strings(id, lang):
	# lang folder name is usually title case, sometimes lowercase
	for l in [lang, lang.title()]:
		f = os.path.join(_info[id]['path'], 'resources', 'language', l, 'strings.xml')
		if os.path.isfile(f):
			print "Reading", f
			if got_soup:
				xml = xmlsoup(f)
				for tag in xml.findAll('string'):
					_strings[id][tag['id']] = tag.string
			else:
				xml = parsexml(quickesc(f))
				for tag in xml.getElementsByTagName('string'):
					frags = []
					for node in tag.childNodes:
						frags.append(node.data)
					_strings[id][tag.getAttribute('id')] = unesc(''.join(frags))

def read_dialogs():
	__builtin__._dialogs = {}
	dlgfile = os.path.join(pms.getProfileDir(), 'xbmc.dialogs')
	if os.path.exists(dlgfile):
		f = open(dlgfile)
		for line in f:
			line = line.strip()
			if not line: continue
			sel,dlg = line.split('<<<', 1)
			_dialogs[dlg.strip()] = eval(sel.strip())


# slightly modified from http://code.activestate.com/recipes/577722-xml-to-python-dictionary-and-back/

def xml2d(e):
	 """Convert an etree element into a dict structure"""
	 def _xml2d(e):
		  kids = dict(e.attrib)
		  if e.text and e.text.strip():
				kids['__text__'] = e.text
		  if e.tail and e.tail.strip():
				kids['__tail__'] = e.tail
		  for k, g in groupby(e, lambda x: x.tag):
				g = [ _xml2d(x) for x in g ]
				kids[k] = g
		  return kids
	 return { e.tag : _xml2d(e) }

def get_addon_path(id):
	path = _info[id]['path'] if id in _info else None
	if not path:
		for p in [
				os.path.join(_special['home'], 'addons', id),
				os.path.join(_special['xbmc'], 'addons', id)
			]:
			if os.path.isdir(p): return p
	return path

EXPANDED = 1
COMPLETE = 2
REQUIRED = 4

class addonDict(DictMixin):

	def __init__(self, jdata=None):
		self.data = {}
		self.flags = {}
		self.vars = {
			'A':os.path.join(_special['home'], 'addons'),
			'X':os.path.join(_special['xbmc'], 'addons'),
			'I':None}
		if jdata and jdata.strip():
			self.baseflag = 0
			self.update(json.loads(jdata))
		self.baseflag = EXPANDED

	def __getitem__(self, key):
		if key in self.data:
			if not self.flags[key] & EXPANDED:
				self.expand(key)
			return self.data[key]
		raise KeyError(key)

	def __setitem__(self, key, item):
		self.data[key] = item
		self.flags[key] = self.baseflag

	def __delitem__(self, key):
		if key in self.data:
			del self.data[key]
			del self.flags[key]
		else:
			raise KeyError(key)

	def keys(self):
		return self.data.keys()

	def expand(self, key):
#		print 'expanding %s'%key
		self.flags[key] |= EXPANDED
		self.vars['I'] = key
		if '{p}' in self.data[key]:
			self.data[key]['path'] = self.data[key]['{p}'].format(**self.vars)
			del self.data[key]['{p}']
		if '{q}' in self.data[key]:
			self.data[key]['_pythonpath'] = []
			for s in self.data[key]['{q}']:
				self.data[key]['_pythonpath'].append(s.format(**self.vars))
			del self.data[key]['{q}']

	def compr(self, string):
		s = string
		for k,v in self.vars.items():
			s = s.replace(v,'{%s}' % k)
		return s

	def digest(self, compress=True):
		compressed = {}
		paths = []
		for key in self.data.keys():
#			print 'compressing %s'%key
			if compress:
				self.vars['I'] = key
				compressed[key] = {}
				if 'path' in self.data[key]:
					compressed[key]['{p}'] = self.compr(self.data[key]['path'])
				if '_pythonpath' in self.data[key]:
					compressed[key]['{q}'] = []
					for s in self.data[key]['_pythonpath']:
						compressed[key]['{q}'].append(self.compr(s))
			if self.flags[key] & REQUIRED:
				paths.append(os.path.join(self.data[key]['path'], self.data[key]['_lib']) if '_lib' in self.data[key] else self.data[key]['path'])
#		print 'paths=%s'%paths
		# marshal also seems to work but may cause encoding issues with py4j
		return (os.path.pathsep.join(paths), json.dumps(compressed) if compress else None)

def read_addon(id=None, dir=None, full=True):

	if id and id in _info and _info[id] is not None and \
			(_info.flags[id] & COMPLETE or \
			(not full and '_pythonpath' in _info[id])):
		return id

	if not dir:
		dir = '.' if id is None else get_addon_path(id)

	xml = os.path.join(dir, 'addon.xml') if dir else None

	if xml and os.path.isfile(xml):
		addon = ElementTree(fromstring(quickesc(xml)))
		id = addon.getroot().attrib['id']
		if not id in _info:
			_info[id] = {}
		_info[id].update(xml2d(addon.getroot())['addon'])
		_info[id]['path'] = os.path.abspath(os.path.dirname(xml))
		_info[id]['profile'] = os.path.join(_special['profile'], 'addon_data', id)
		_info[id]['icon'] = 'icon.png'
		provides = addon.find('.//extension/provides')
		_info[id]['provides'] = (provides.text if provides is not None else None)
		paths = []
		try:
			_info[id]['_script'] = addon.find('.//extension[@point="xbmc.python.pluginsource"]').attrib['library']
		except:
			try:
				_info[id]['_lib'] = addon.find('.//extension[@point="xbmc.python.module"]').attrib['library']
				paths = [os.path.join(dir, _info[id]['_lib'])]
				# hack
				if id == 'script.module.urlresolver':
					paths.append(os.path.join(paths[0], 'urlresolver', 'plugins'))
			except KeyError:
				# no 'library' means it's the top dir
				paths = [_info[id]['path']]
			except:
				pass

		addonlib = os.path.join(_info[id]['path'], 'resources', 'lib')
		if os.path.exists(addonlib) and not addonlib in paths:
			paths.append(addonlib)

		try:
			required = [a['addon'] for a in _info[id]['requires'][0]['import'] if not a['addon'].startswith('xbmc.')]
		except:
			required = []

		if not '_pythonpath' in _info[id]:
			try:
				# recurse through dep tree to gather PYTHONPATH
				for dep in required:
					if read_addon(id=dep, full=full) != None:
						paths.extend(_info[dep]['_pythonpath'])
						_info.flags[dep] |= REQUIRED
				_info[id]['_pythonpath'] = list(set(paths))
			except:
				traceback.print_exc(file=sys.stdout)

		if full:
			for i in [id] + required:
				if not i in _settings:
					read_settings(i)
					_strings[i] = {}
					# start with english
					read_strings(i, 'English')
					# overlay any non-english strings
					if not 'english' in _settings['xbmc'][u'language'].lower():
						read_strings(i, _settings['xbmc'][u'language'])
			_info.flags[id] |= COMPLETE
		return id
	if id: print 'Error: %s not found.' % id
	return None

# see http://nedbatchelder.com/blog/200905/running_a_python_file_as_main_take_2.html
# http://stackoverflow.com/questions/1830727/how-to-load-compiled-python-modules-from-memory

def load_addon(id):
	print 'loading %s' % id
	script = os.path.join(_info[id]['path'], _info[id]['_script'])
	if id in _addons:
		mod, codeobj = _addons[id]
	else:
		pyc = '%sc' % script
		if os.path.exists(pyc):
			src = open(pyc, 'rb')
			codeobj = marshal.loads(src.read()[8:])
		else:
			src = open(script)
			code = src.read()
			if not code or code[-1] != '\n':
				code += '\n'
			codeobj = compile(code, script, 'exec')
		src.close()
	# always re-instantiate the module
	mod = types.ModuleType('__main__')
#	mod = imp.new_module('__main__') # also works
	mod.__file__ = script
	mod.__path__ = [os.path.dirname(script)]
	mod.__builtins__ = sys.modules['__builtin__']
	_addons[id] = (mod, codeobj)
	return _addons[id]

class mainImporter:
	"""a finder to import __main__.foo as foo"""
	def find_module(self, fullname, path=None):
		return self if fullname and fullname[0:9] == '__main__.' else None

	def load_module(self, fullname):
		name = fullname[9:]
		if name in sys.modules:
			return sys.modules[name]
		print 'importing %s as %s' % (fullname, name)
		return import_module(name)

# see also http://pyunit.sourceforge.net/notes/reloading.html
#          http://www.indelible.org/ink/python-reloading/

class revertableDict(IterableUserDict):
	"""A dict wrapper to allow reverting to the initial state"""
	def __init__(self, otherdict):
		self.data = otherdict
		self.basekeys = list(self.data.keys())
	def revert(self):
		for key in self.data.keys():
			if not key in self.basekeys:
				del self.data[key]
	def clear(self):
		self.revert()

jobs = []
importer = mainImporter()

def run_addon(pluginurl=None):
	# execute 'plugin://' urls, one at a time
	global jobs, importer
	queued = False
	if not pluginurl:
		pluginurl = jobs[0]
		queued = True
	elif not pluginurl in jobs:
		jobs.append(pluginurl)
		if len(jobs) > 1:
			print 'queueing: %s' % pluginurl
			return
	else:
		# ignore duplicate jobs
		return
	url = pluginurl.encode('utf-8') if isinstance(pluginurl, unicode) else pluginurl
	print '\nrun_addon%s: %s' % (' (queued)' if queued else '', url)
	import xbmc, xbmcplugin
	# save state
	home = os.getcwd()
	mainid = _mainid
	main = sys.modules['__main__']
	syspath = sys.path
	argv = sys.argv
	xargv0 = xbmcplugin.argv0
	sysmods = sys.modules
	basemods = revertableDict(sys.modules)
	# pull any state-sensitive modules to force re-import
	sensitives = [sys.modules.pop(m) for m in [
			'urllib', 'urllib2', 'cookielib'
		] if m in sys.modules]
	try:
		# reset and run
		id = urlparse(url).netloc
		reset(id)
		addondir = _info[id]['path']
		os.chdir(addondir)
		mod, codeobj = load_addon(id)
		xbmcplugin.setargv([mod.__file__, url])
		sys.modules = basemods
		sys.modules['__main__'] = mod
		sys.meta_path.append(importer)
		exec codeobj in mod.__dict__
	except:
		print 'Error: run_addon'
		traceback.print_exc(file=sys.stdout)
	finally:
		# restore state
		basemods.revert()
		sys.modules = sysmods
		for m in sensitives:
			sys.modules[m.__name__] = m
		os.chdir(home)
		__builtin__._mainid = mainid
		sys.meta_path.remove(importer)
		sys.modules['__main__'] = main
		sys.path = syspath
		sys.argv = argv
		xbmcplugin.argv0 = xargv0
		del jobs[0]
		if len(jobs):
			run_addon()


def reset(id=None):
	__builtin__._mainid = read_addon(id)
	if _mainid:
		mainpath = [_info[_mainid]['path']] + _info[_mainid]['_pythonpath']
		extrapaths = [p for p in xbmc_paths if p not in mainpath]
		for d in [p for p in mainpath + extrapaths if p in sys.path]:
			sys.path.remove(d)
		sys.path = mainpath + sys.path + extrapaths
		print ""
		print "Settings:", _settings[_mainid]

try: _settings
except NameError:
	__builtin__._info = addonDict(pms.getVar('xbmc_info'))
	__builtin__._settings = {}
	__builtin__._strings = {}
	__builtin__._addons = {}
	paths = pms.getVar('xbmc_paths')
	__builtin__.xbmc_paths = (paths.split(os.path.pathsep) if paths else [])
	read_xbmc_settings()

try: _mainid
except NameError:
	reset()

class mock(object):
	'''
	A shapeless self-referring class that never raises
	an AttributeError, is always callable and will always
	evaluate as a string, int, float, bool, or container.
	'''
	# http://www.rafekettler.com/magicmethods.html
	def __new__(cls, *args): return object.__new__(cls)
	def __init__(self, *args): pass
	def __getattr__(self, name): return self
	def __call__(self, *args, **kwargs): return self
	def __int__(self): return 0
	def __float__(self): return 0
	def __str__(self): return '0'
	def __nonzero__(self): return False
	def __getitem__(self, key): return self
	def __setitem__(self, key,value): pass
	def __delitem__(self, key): pass
	def __len__(self): return 3
	def __iter__(self): return iter([self,self,self])

