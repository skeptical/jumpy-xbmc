import __builtin__, os, sys, traceback
from xml.etree.ElementTree import ElementTree
from xml.dom.minidom import parse

version = '0.2.4'

# see http://wiki.xbmc.org/index.php?title=Special_protocol
try: _special
except NameError:
	__builtin__._special = {}
	platform = sys.platform
#	_special['xbmc'] = #TODO
	if platform.startswith('linux'):
		_special['home'] = os.getenv('HOME') + '/.xbmc'
		_special['temp'] = _special['home'] + '/temp'
	elif platform.startswith('win32'):
		_special['home'] = os.getenv('APPDATA') + '\\XBMC'
		_special['temp'] = _special['home'] + '\\temp'
	elif platform.startswith('darwin'):
		_special['home'] = os.getenv('HOME') + '/Library/Application Support/XBMC'
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

def read_settings(f):
	if os.path.isfile(f):
		print "Loading", f
		xml = parse(f)
		for tag in xml.getElementsByTagName('setting'):
			val = tag.getAttribute('value') if tag.hasAttribute('value') else tag.getAttribute('default')
			_settings[tag.getAttribute('id')] = val
		return True
	return False

def read_addon(dir):
	xml = os.path.join(dir, 'addon.xml')
	addonsdir = os.path.dirname(dir)
	if os.path.isfile(xml):
		addon = ElementTree()
		addon.parse(xml)
		script = addon.find('.//extension[@point="xbmc.python.pluginsource"]').attrib['library']
		if script is not None:
			try:
				# set any required lib paths
				path = ''
				for mod in addon.findall('.//requires/import'):
					dep = mod.attrib['addon']
					if dep != 'xbmc.python':
						path = path + os.path.pathsep + os.path.join(addonsdir, dep, 'lib')
				id = addon.getroot().attrib['id']
				name = addon.getroot().attrib['name']
				thumb = os.path.join(dir, 'icon.png')
				script = os.path.join(dir, script)
				return id, name, script, thumb, path
			except:
				traceback.print_exc(file=sys.stdout)
	return None

try: _addon
except NameError:
	__builtin__._addon = ElementTree()
	__builtin__._settings = {}
	__builtin__._addonstrings = {}
	if os.path.isfile('addon.xml'):
		_addon.parse('addon.xml')

		id = _addon.getroot().attrib['id']
		if not read_settings(os.path.join(_special['userdata'], 'addon_data', id, 'settings.xml')):
			read_settings(os.path.join('resources', 'settings.xml'))
		print "Settings:", _settings

		f = os.path.join('resources', 'language', 'English', 'strings.xml')
		if os.path.isfile(f):
			xml = parse(f)
			for tag in xml.getElementsByTagName('string'):
				frags = []
				for node in tag.childNodes:
					frags.append(node.data)
				_addonstrings[tag.getAttribute('id')] = ''.join(frags)

