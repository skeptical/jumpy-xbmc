import __builtin__, os, sys, traceback
from xml.etree.ElementTree import ElementTree, fromstring
#from xml.dom.minidom import parse
from xml.dom.minidom import parseString
from xml.sax.saxutils import unescape

version = '0.2.10'

# see http://wiki.xbmc.org/index.php?title=Special_protocol
try: _special
except NameError:
	__builtin__._special = {}
	platform = sys.platform
#	_special['xbmc'] = #TODO
	home = os.getenv('xbmc_home') if 'xbmc_home' in os.environ else None
	if platform.startswith('linux'):
		_special['home'] = home if home else os.getenv('HOME') + '/.xbmc'
		_special['temp'] = _special['home'] + '/temp'
	elif platform.startswith('win32'):
		_special['home'] = home if home else os.getenv('APPDATA') + '\\XBMC'
		_special['temp'] = _special['home'] + '\\temp'
	elif platform.startswith('darwin'):
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

def quickesc(file):
	# for some reason xbmc xml files allow unescaped ampersands
	return unescape(open(file).read()).replace('&','&amp;')

def read_settings(f):
	if os.path.isfile(f):
		print "Loading", f
#		xml = parse(f)
		xml = parseString(quickesc(f))
		for tag in xml.getElementsByTagName('setting'):
			val = tag.getAttribute('value') if tag.hasAttribute('value') else tag.getAttribute('default')
			_settings[tag.getAttribute('id')] = val
		return True
	return False

def read_addon(dir, deps=None):
	plugin=False
	if not deps:
		deps = {}
		plugin=True
	xml = os.path.join(dir, 'addon.xml')
	
	if os.path.isfile(xml):
#		addon = ElementTree()
#		addon.parse(xml)
		addon = ElementTree(fromstring(quickesc(xml)))
		script = None
		if plugin:
			try: script = addon.find('.//extension[@point="xbmc.python.pluginsource"]').attrib['library']
			except AttributeError: return None
		addonsdir = os.path.dirname(dir)
		try:
			# set any required lib deps
			for mod in addon.findall('.//requires/import'):
				dep = mod.attrib['addon']
				if dep != 'xbmc.python' and not dep in deps:
					deps[dep] = os.path.join(addonsdir, dep, 'lib')
					# check for sub-deps
					read_addon(os.path.join(addonsdir, dep), deps)
			if plugin:
				id = addon.getroot().attrib['id']
				name = addon.getroot().attrib['name']
				thumb = os.path.join(dir, 'icon.png')
				script = os.path.join(dir, script)
				return id, name, script, thumb, os.path.pathsep.join(deps.values())
		except:
			traceback.print_exc(file=sys.stdout)
	return None

try: _addon
except NameError:
	__builtin__._addon = ElementTree()
	__builtin__._settings = {}
	__builtin__._addonstrings = {}

	if os.path.isfile('addon.xml'):
#		_addon.parse('addon.xml')
		_addon = ElementTree(fromstring(quickesc('addon.xml')))

		_settings[u'theme'] = u'0'
		id = _addon.getroot().attrib['id']
		_settings[u'__xbmcaddonid__'] = id
		read_settings(os.path.join('resources', 'settings.xml'))
		read_settings(os.path.join(_special['userdata'], 'addon_data', id, 'settings.xml'))
		print "Settings:", _settings

		f = os.path.join('resources', 'language', 'English', 'strings.xml')
		if os.path.isfile(f):
#			xml = parse(f)
			xml = parseString(quickesc(f))
			for tag in xml.getElementsByTagName('string'):
				frags = []
				for node in tag.childNodes:
					frags.append(node.data)
				_addonstrings[tag.getAttribute('id')] = ''.join(frags)

