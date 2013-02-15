import __builtin__, os, sys, platform, traceback, re, jumpy
from xml.etree.ElementTree import ElementTree, fromstring
#from xml.dom.minidom import parse
from xml.dom.minidom import parseString
from xml.sax.saxutils import escape, unescape
from itertools import groupby
import atexit

version = '0.3.5-dev'

# see http://wiki.xbmc.org/index.php?title=Special_protocol
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
		_special['home'] = home if home else os.getenv('HOME') + '/.xbmc'
		_special['temp'] = _special['home'] + '/temp'
	elif sys.platform.startswith('win32'):
		_special['xbmc'] = main if main else \
			(os.getenv('PROGRAMFILES(X86)') if 'PROGRAMFILES(X86)' in os.environ \
			else os.getenv('PROGRAMFILES')) + '\\XBMC'
		_special['home'] = home if home else os.getenv('APPDATA') + '\\XBMC'
		_special['temp'] = _special['home'] + '\\cache'
	elif sys.platform.startswith('darwin'):
		_special['xbmc'] = main if main else \
			'/Applications/XBMC.app/Contents/Resources/XBMC'
		_special['home'] = home if home else os.getenv('HOME') + '/Library/Application Support/XBMC'
		_special['temp'] = os.getenv('HOME') + '.xbmc/temp'
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

def read_xbmc_settings():
	_settings['xbmc'] = {}
	_settings['xbmc'][u'theme'] = 0
	lang = os.getenv('xbmc_lang')
	if lang is None:
		guisettings = os.path.join(_special['userdata'], 'guisettings.xml')
		if os.path.isfile(guisettings):
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
			xml = parseString(quickesc(f))
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
			xml = parseString(quickesc(f))
			for tag in xml.getElementsByTagName('string'):
				frags = []
				for node in tag.childNodes:
					frags.append(node.data)
				_strings[id][tag.getAttribute('id')] = unesc(''.join(frags))
			return

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

try: _settings
except NameError:
	sys.meta_path.append(xbmcimport())
	__builtin__._settings = {}
	__builtin__._strings = {}
	__builtin__._info = {}
	read_xbmc_settings()
	__builtin__._mainid = read_addon()

	if _mainid:
		print ""
		print "Settings:", _settings[_mainid]


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


