import __builtin__, os, sys, platform, atexit, traceback, re, jumpy
import imp, types, marshal
from xml.etree.ElementTree import ElementTree, fromstring
#from xml.dom.minidom import parse
from xml.dom.minidom import parseString
from xml.sax.saxutils import escape, unescape
from itertools import groupby
from urlparse import urlparse

version = '0.3.5'

try: _special
except NameError:
	__builtin__._special = {}
	home = os.getenv('xbmc_home') if 'xbmc_home' in os.environ else None
	main = os.getenv('xbmc_main') if 'xbmc_main' in os.environ else None
	if sys.platform.startswith('linux'):
		# FIXME: this won't find xbmc if it's installed to another prefix
		_special['xbmc'] = main if main else \
			('/usr/local/share/xbmc' if os.path.exists('/usr/local/share/xbmc') \
			else '/usr/share/xbmc')
		_special['xbmcbin'] = _special['xbmc'].replace('share', 'lib')
		_special['home'] = home if home else os.getenv('HOME') + '/.xbmc'
		_special['userhome'] = _special['home']
		_special['temp'] = _special['home'] + '/temp'
		_special['logpath'] = _special['temp']
	elif sys.platform.startswith('win32'):
		_special['xbmc'] = main if main else \
			(os.getenv('PROGRAMFILES(X86)') if 'PROGRAMFILES(X86)' in os.environ \
			else os.getenv('PROGRAMFILES')) + '\\XBMC'
		_special['xbmcbin'] = _special['xbmc']
		_special['home'] = home if home else os.getenv('APPDATA') + '\\XBMC'
		_special['userhome'] = os.getenv('USERPROFILE')
		_special['temp'] = _special['home'] + '\\cache'
		_special['logpath'] = _special['home']
	elif sys.platform.startswith('darwin'):
		_special['xbmc'] = main if main else \
			'/Applications/XBMC.app/Contents/Resources/XBMC'
		_special['xbmcbin'] = _special['xbmc']
		_special['home'] = home if home else os.getenv('HOME') + '/Library/Application Support/XBMC'
		_special['userhome'] = _special['home']
		_special['temp'] = os.getenv('HOME') + '.xbmc/temp'
		_special['logpath'] = os.getenv('HOME') + '/Library/Logs'
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
			xml = parsexml(quickesc(f))
			for tag in xml.getElementsByTagName('string'):
				frags = []
				for node in tag.childNodes:
					frags.append(node.data)
				_strings[id][tag.getAttribute('id')] = unesc(''.join(frags))
			return

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


def read_addon(id=None, dir=None, full=True):

	if id is not None and id in _info and _info[id] is not None:
		return id

	for dir in [dir] if dir else ['.'] if id is None else [
				os.path.join(_special['home'], 'addons', id),
				os.path.join(_special['xbmc'], 'addons', id)
			]:
		xml = os.path.join(dir, 'addon.xml')
		if os.path.isfile(xml): break
		xml = None

	if xml is not None:
		addon = ElementTree(fromstring(quickesc(xml)))
		id = addon.getroot().attrib['id']
		if not id in _info:
			_info[id] = xml2d(addon.getroot())['addon']
			_info[id]['path'] = os.path.abspath(os.path.dirname(xml))
			_info[id]['profile'] = os.path.join(_special['profile'], 'addon_data', id)
			_info[id]['icon'] = 'icon.png'
			paths = []
			try:
				_info[id]['_script'] = addon.find('.//extension[@point="xbmc.python.pluginsource"]').attrib['library']
			except AttributeError:
				try:
					_info[id]['_lib'] = addon.find('.//extension[@point="xbmc.python.module"]').attrib['library']
					paths = [os.path.join(dir, _info[id]['_lib'])]
				except KeyError:
					# no 'library' means it's the top dir
					paths = [_info[id]['path']]
				except:
					pass

			try:
				# recurse through dep tree to gather PYTHONPATH
				for mod in addon.findall('.//requires/import'):
					dep = mod.attrib['addon']
					if dep != 'xbmc.python' and not dep in paths and \
							read_addon(id=dep, full=full) != None:
						paths.extend(_info[dep]['_pythonpath'].split(os.path.pathsep))
				_info[id]['_pythonpath'] = os.path.pathsep.join(set(paths))
			except:
				traceback.print_exc(file=sys.stdout)

		if full and not id in _settings:
			read_settings(id)
			_strings[id] = {}
			# start with english
			read_strings(id, 'English')
			# overlay any non-english strings
			if not 'english' in _settings['xbmc'][u'language'].lower():
				read_strings(id, _settings['xbmc'][u'language'])

		return id
	return None

# see http://nedbatchelder.com/blog/200905/running_a_python_file_as_main_take_2.html
# http://stackoverflow.com/questions/1830727/how-to-load-compiled-python-modules-from-memory

def load_addon(id):
	print 'loading %s' % id
	script = os.path.join(_info[id]['path'], _info[id]['_script'])
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
	mod = types.ModuleType('__main__')
#	mod = imp.new_module('__main__') # also works
	mod.__file__ = script
	mod.__path__ = [os.path.dirname(script)]
	mod.__builtins__ = sys.modules['__builtin__']
	_addons[id] = (mod, codeobj)

# see also http://pyunit.sourceforge.net/notes/reloading.html
#          http://www.indelible.org/ink/python-reloading/

from UserDict import IterableUserDict

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

def run_addon(pluginurl):
	# execute a 'plugin://' url
	print '\nrun_addon: %s' % pluginurl
	import xbmc, xbmcplugin
	# save state
	home = os.getcwd()
	mainid = _mainid
	main = sys.modules['__main__']
	path0 = sys.path[0]
	argv = sys.argv
	xargv0 = xbmcplugin.argv0
	sysmods = sys.modules
	basemods = revertableDict(sys.modules)
	try:
		# reset and run
		id = urlparse(pluginurl).netloc
		reset(id)
		addondir = _info[id]['path']
		os.chdir(addondir)
		sys.path[0] = addondir
		if not id in _addons:
			paths = _info[id]['_pythonpath'].split(os.path.pathsep)
			sys.path += [p for p in paths if p not in sys.path]
			load_addon(id)
		mod, codeobj = _addons[id]
		xbmcplugin.setargv([mod.__file__, pluginurl])
		sys.modules['__main__'] = mod
		sys.modules = basemods
		exec codeobj in mod.__dict__
	except:
		print 'Error: run_addon'
		traceback.print_exc(file=sys.stdout)
	finally:
		# restore state
		basemods.revert()
		sys.modules = sysmods
		os.chdir(home)
		__builtin__._mainid = mainid
		sys.modules['__main__'] = main
		sys.path[0] = path0
		sys.argv = argv
		xbmcplugin.argv0 = xargv0

class xbmcimport:
	# a finder to amend sys.path on the fly in case an addon
	# tries to import a non-dep script.module (e.g. classiccinema)
	def find_module(self, fullname, path=None):
		id = "script.module.%s" % (fullname)
		if path is None and not id in _info:
			id = read_addon(id)
			if id is not None:
				lib = os.path.join(_info[id]['path'], _info[id]['_lib'])
				pms.addPath(lib)
				sys.path.append(lib)
		return None

def reset(id=None):
	__builtin__._mainid = read_addon(id)
	if _mainid:
		print ""
		print "Settings:", _settings[_mainid]

try: _settings
except NameError:
	sys.meta_path.append(xbmcimport())
	__builtin__._settings = {}
	__builtin__._strings = {}
	__builtin__._info = {}
	__builtin__._addons = {}
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


