import __builtin__, os, sys, platform, traceback
from xml.etree.ElementTree import ElementTree, fromstring
#from xml.dom.minidom import parse
from xml.dom.minidom import parseString
from xml.sax.saxutils import unescape

version = '0.3.1'

# see http://wiki.xbmc.org/index.php?title=Special_protocol
try: _special
except NameError:
	__builtin__._special = {}
	home = os.getenv('xbmc_home') if 'xbmc_home' in os.environ else None
	if sys.platform.startswith('linux'):
		# FIXME: this won't find xbmc if it's installed to another prefix
		_special['xbmc'] = ('/usr/local/share/xbmc' if os.path.exists('/usr/local/share/xbmc') \
			else '/usr/share/xbmc')
		_special['home'] = home if home else os.getenv('HOME') + '/.xbmc'
		_special['temp'] = _special['home'] + '/temp'
	elif sys.platform.startswith('win32'):
		_special['xbmc'] = (os.getenv('ProgramFiles') if platform.release() == 'XP' \
			else os.getenv('ProgramFiles(x86)')) + '\\XBMC'
		_special['home'] = home if home else os.getenv('APPDATA') + '\\XBMC'
		_special['temp'] = _special['home'] + '\\temp'
	elif sys.platform.startswith('darwin'):
		_special['xbmc'] = '/Applications/XBMC.app/Contents/Resources/XBMC'
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
				val = tag.getAttribute('value') if tag.hasAttribute('value') else tag.getAttribute('default')
				_settings[id][tag.getAttribute('id')] = val

def read_strings(id, lang):
	_strings[id] = {}
	for i in range(2):
		f = os.path.join(_info[id]['path'], 'resources', 'language', lang, 'strings.xml')
		if os.path.isfile(f):
			print "Reading", f
			xml = parseString(quickesc(f))
			for tag in xml.getElementsByTagName('string'):
				frags = []
				for node in tag.childNodes:
					frags.append(node.data)
				_strings[id][tag.getAttribute('id')] = ''.join(frags)
			return
		# sometimes it's 'english' instead of 'English'
		lang = lang.lower()

def read_addon(id=None, dir=None, full=True):

	addonsdir = os.path.join(_special['home'], 'addons')
	xbmcaddonsdir = os.path.join(_special['xbmc'], 'addons')
	xml = os.path.join(dir or ('.' if id is None else os.path.join(addonsdir, id)), 'addon.xml')

	if os.path.isfile(xml):
		addon = ElementTree(fromstring(quickesc(xml)))
		id = addon.getroot().attrib['id']
		if not id in _info:
			_info[id] = {}
			_info[id]['name'] = addon.getroot().attrib['name']
			_info[id]['path'] = os.path.dirname(xml)
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
				except AttributeError:
					return None
			try:
				# recurse through dep tree to gather PYTHONPATH
				for mod in addon.findall('.//requires/import'):
					dep = mod.attrib['addon']
					if dep != 'xbmc.python' and not dep in paths:
						addondir = os.path.join(addonsdir, dep)
						if not os.path.exists(addondir):
							addondir = os.path.join(xbmcaddonsdir, dep)
						read_addon(dir=addondir, full=full)
						paths.extend(_info[dep]['_pythonpath'].split(os.path.pathsep))
				_info[id]['_pythonpath'] = os.path.pathsep.join(set(paths))
			except:
				traceback.print_exc(file=sys.stdout)

		if full and not id in _settings:
			read_settings(id)
			read_strings(id, 'English')

		return id
	return None

try: _settings
except NameError:
	__builtin__._settings = {}
	__builtin__._strings = {}
	__builtin__._info = {}
	__builtin__._mainid = read_addon()

	_settings['xbmc'] = {u'theme':u'0'}

	if _mainid:
		print ""
		print "Settings:", _settings[_mainid]

