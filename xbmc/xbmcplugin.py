import os, sys
import urllib, re
from urlparse import urlparse
from ast import literal_eval
#import pprint

import jumpy, xbmcinit, xbmc

# some plugins seem to expect these to be preloaded
# sys is already preloaded by jumpy
import __builtin__
__builtin__.os = os
__builtin__.xbmc = xbmc

# xbmc/SortFileItem.h
SORT_METHOD_NONE = 0
SORT_METHOD_LABEL = 1
SORT_METHOD_LABEL_IGNORE_THE = 2
SORT_METHOD_DATE = 3
SORT_METHOD_SIZE = 4
SORT_METHOD_FILE = 5
SORT_METHOD_DRIVE_TYPE = 6
SORT_METHOD_TRACKNUM = 7
SORT_METHOD_DURATION = 8
SORT_METHOD_TITLE = 9
SORT_METHOD_TITLE_IGNORE_THE = 10
SORT_METHOD_ARTIST = 11
SORT_METHOD_ARTIST_AND_YEAR = 12
SORT_METHOD_ARTIST_IGNORE_THE = 13
SORT_METHOD_ALBUM = 14
SORT_METHOD_ALBUM_IGNORE_THE = 15
SORT_METHOD_GENRE = 16
SORT_METHOD_COUNTRY = 17
SORT_METHOD_YEAR = 18
SORT_METHOD_VIDEO_YEAR = SORT_METHOD_YEAR
SORT_METHOD_VIDEO_RATING = 19
SORT_METHOD_VIDEO_USER_RATING = 20
SORT_METHOD_DATEADDED = 21
SORT_METHOD_PROGRAM_COUNT = 22
SORT_METHOD_PLAYLIST_ORDER = 23
SORT_METHOD_EPISODE = 24
SORT_METHOD_VIDEO_TITLE = 25
SORT_METHOD_VIDEO_SORT_TITLE = 26
SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE = 27
SORT_METHOD_PRODUCTIONCODE = 28
SORT_METHOD_SONG_RATING = 29
SORT_METHOD_MPAA_RATING = 30
SORT_METHOD_VIDEO_RUNTIME = 31
SORT_METHOD_STUDIO = 32
SORT_METHOD_STUDIO_IGNORE_THE = 33
SORT_METHOD_FULLPATH = 34
SORT_METHOD_LABEL_IGNORE_FOLDERS = 35
SORT_METHOD_LASTPLAYED = 36
SORT_METHOD_PLAYCOUNT = 37
SORT_METHOD_LISTENERS = 38
SORT_METHOD_UNSORTED = 39
SORT_METHOD_CHANNEL = 40
SORT_METHOD_CHANNEL_NUMBER = 41
SORT_METHOD_BITRATE = 42
SORT_METHOD_DATE_TAKEN = 43
SORT_METHOD_MAX = 44

SORT_ORDER_NONE = 0
SORT_ORDER_ASC = 1
SORT_ORDER_DESC = 2

SORT_NORMALLY = 0
SORT_ON_TOP = 1
SORT_ON_BOTTOM = 2

librtmp_checked = False
librtmp = False

argv0 = sys.argv[0]

# added functions

def setargv(argv):
	global argv0
	argv0 = sys.argv[0]
	# restructure args to xbmc command format, i.e.
	#   [plugin:// url, window_id, query_string]
	if len(argv) > 1:
		args = argv[1].split('?')
		sys.argv = []
		sys.argv.append(args[0])
		sys.argv.append('0')
		sys.argv.append("" if len(args) == 1 else "?" + args[1])

setargv(sys.argv)

def fullPath(base, path):
#	print 'fullPath %s' % [base, path]
	if path == None:
		return None
	if urlparse(path).scheme == "" and not os.path.isabs(path):
		url = urlparse(base)
		path = '%s://%s/%s' % (url.scheme, url.netloc, path) if url.scheme != ""  \
			else os.path.join(os.path.dirname(base), path)
	return xbmc.translatePath(path, False)

# see xbmc/guilib/GUITextLayout.cpp::ParseText

ltags = re.compile(r'\[/?(COLOR.*?|B|I)\]')

def striptags(label):
	global ltags
	if label is not None:
		return ltags.sub('', label)
	return label

def getMediaType(listitem):
	mediatype = listitem.getProperty('type').strip().upper()
	if mediatype is None and _info[_mainid]['provides'] is not None:
		# try the addon's primary media type
		mediatype = _info[_mainid]['provides'].strip().split(' ')[0].upper()
#	print 'mediatype=%s' % mediatype
	if mediatype == "VIDEO":
		return PMS_VIDEO
	elif mediatype == "MUSIC" or mediatype == "AUDIO":
		return PMS_AUDIO
	elif mediatype == "PICTURE" or mediatype == "IMAGE":
		return PMS_IMAGE
	else:
		return PMS_UNKNOWN

#	see xbmc/interfaces/legacy/ListItem.h

def mediaInfo(listitem):
	m = {k:listitem.data[k] for k in ['duration', 'streams'] if k in listitem.data}
	# duration is given either as minutes or hh:mm:ss
	if 'duration' in m:
		m['duration'] = str(m['duration']) + ('' if ':' in str(m['duration']) else ':00')
	return m if m else None
#	return m

def resolve(url, listitem, isFolder=False):
#	pprint.pprint(listitem.data.data)
	name = striptags(listitem.getLabel())
	if not name: name = striptags(listitem.getProperty('title'))
	if not name: name = pms.getFolderName()
	if not name: name = "Item"
	return (PMS_FOLDER if isFolder else getMediaType(listitem), name, \
		fullPath(url, listitem.getProperty('thumbnailImage')), \
		None if isFolder else mediaInfo(listitem))

def using_librtmp():
	global librtmp_checked, librtmp
	if not librtmp_checked:
		librtmp = pms.getVar('using_librtmp') == 'true'
		librtmp_checked = True
	return librtmp

def rtmpsplit(url, listitem):
	sargs = []
	args = []
	tups = re.findall(r' ([-\w]+)=(".*?"|\S+)', ' -r=' + url)
	# see xbmc/cores/dvdplayer/DVDInputStreams/DVDInputStreamRTMP.cpp:120
	for key,tag in [
			( "SWFPlayer", "swfUrl"),
			( "PageURL",   "pageUrl"),
			( "PlayPath",  "playpath"),
			( "TcUrl",     "tcUrl"),
			( "IsLive",    "live")
		]:
			try:
				tups.append((tag, listitem.getProperty(key)))
			except KeyError:
				pass
	swfVfy = True if url.lower().replace('=1', '=true').find(" swfvfy=true") > -1 else False
	opts = {
		'swfurl'    : '-W' if swfVfy else '-s',
		'playpath'  : '-y',
		'app'       : '-a',
		'pageurl'   : '-p',
		'tcurl'     : '-t',
		'subscribe' : '-d',
		'live'      : '-v',
		'playlist'  : '-Y',
		'socks'     : '-S',
		'flashver'  : '-f',
		'conn'      : '-C',
		'jtv'       : '-j',
		'token'     : '-T',
		'swfage'    : '-X',
		'start'     : '-A',
		'stop'      : '-B',
		'buffer'    : '-b',
		'timeout'   : '-m',
		'auth'      : '-u'
	}
	for key,val in tups:
		if val is None:
			continue
#		# convert some '\hh' hex escapes
#		val = val.replace('\\5c','\\').replace('\\20',' ') \
#			.replace('\\22','\\"' if sys.platform.startswith('win32') else '"')
		# convert all '\hh' hex escapes
		val = literal_eval("'%s'" % val.replace('\\','\\x'))
		if sys.platform.startswith('win32'):
			val = val.replace('"', '\\"')
		if key.lower() in opts:
			key = opts[key.lower()]
		if val == '1' or val.lower() == 'true':
			if key.lower() != 'swfvfy':
				sargs.append(key)
		else:
			args.append((key, val))
	cmd = "rtmpdump " + ' '.join('%s "%s"' % arg for arg in args) + ' ' + ' '.join(sargs)
	print "test cmd: %s\n" %  cmd
	return (args, sargs)

def librtmpify(url, listitem):
	newurl = [url]
	# see xbmc/cores/dvdplayer/DVDInputStreams/DVDInputStreamRTMP.cpp:120
	for key,tag in [
			( "SWFPlayer", "swfUrl"),
			( "PageURL",   "pageUrl"),
			( "PlayPath",  "playpath"),
			( "TcUrl",     "tcUrl"),
			( "IsLive",    "live")
		]:
			try:
				val = listitem.getProperty(key)
				if val:
					newurl.append('%s=%s' % (tag, val))
			except KeyError:
				pass
	newurl = ' '.join(newurl)
	print 'test cmd: ffmpeg -y -i "%s" -target ntsc-dvd - \n' %  newurl
	return newurl

# native xbmc functions

def addDirectoryItem(handle, url, listitem, isFolder=False, totalItems=None):
	"""Callback function to pass directory contents back to XBMC."""
	if not url:
		return False
	script = argv0
	state = 0
	id = None
	if not isFolder:
		if url.startswith('plugin://'):
			id = xbmcinit.read_addon(urlparse(url).netloc)
			script = os.path.join(_info[id]['path'], _info[id]['_script'])
			state = PMS_UNRESOLVED
		else:
			listitem.setProperty('path', url)
			setResolvedUrl(handle, True, listitem, 0)
			return True
	print "*** addDirectoryItem ***"
	mediatype, name, thumb, mediainfo = resolve(url, listitem, isFolder)
	if id and id in force_resolve:
		mediatype = PMS_FOLDER
	pms.addItem(state|mediatype, pms.esc(name), [XBMC_RUN, script, url], thumb, mediainfo)
	return True

def addDirectoryItems(handle, items, totalItems=None):
	"""Callback function to pass directory contents back to XBMC as a list."""
	for (url, listitem, isFolder) in items:
		addDirectoryItem(handle, url, listitem, isFolder)
	return True

def setResolvedUrl(handle, succeeded, listitem, stack=-1):
	"""Callback function to tell XBMC that the file plugin has been resolved to a url"""
	url = listitem.getProperty('path')
	if not succeeded or url is None or not (type(url) == str or type(url) == unicode):
		return

	details = {}
	url,headers = xbmc.split_url_headers(url)
	if headers:
		details['headers'] = headers

	if url.startswith('rtmp'):
		if using_librtmp():
			url = librtmpify(url, listitem)
		else:
			args, sargs = rtmpsplit(url, listitem)
			url = "rtmpdump://rtmp2pms?" + urllib.urlencode(args) + (('&' + '&'.join(sargs)) if len(sargs) else '')

	elif url.startswith('plugin://'):
		xbmcinit.run_addon(url)
		return

	# see xbmc/filesystem/StackDirectory.cpp
	elif url.startswith('stack://'):
		ct = 0
		for url in url[8:].split(' , '):
			listitem.setProperty('path', url.replace(',,', ','))
			setResolvedUrl(handle, succeeded, listitem, ct)
			ct += 1
		return

	mediatype, name, thumb, mediainfo = resolve(url, listitem)

	if mediainfo:
		details['media'] = mediainfo

	name = name + "" if stack < 1 else " %d" % stack

	pms.addItem(mediatype, pms.esc(name), url, thumb, details=details)
	print "*** setResolvedUrl ***"
	print "raw : %s" % listitem.getProperty('path')
	print "name: %s" % name
	print "type: %d" % mediatype
	print "url :",url
	print "details : %s" % details

def endOfDirectory(handle, succeeded=None, updateListing=None, cacheToDisc=None):
	"""Callback function to tell XBMC that the end of the directory listing in a virtualPythonFolder is reached."""
	print "*** endOfDirectory ***"

def addSortMethod(handle, sortMethod, label2Mask=None):
	"""Adds a sorting method for the media list."""
	pass

# some plugins e.g Nickolodeon call getSetting(handle, id) instead of getSetting(id)
def getSetting(id, id2=None):
	"""Returns the value of a setting as a string."""
	try:
		return _settings[_mainid][id if id2 == None else id2]
	except KeyError:
		return ''

def setSetting(handle, id, value):
	"""Sets a plugin setting for the current running plugin."""
	_settings[_mainid][id] = value

def setContent(handle, content):
	"""Sets the plugins content."""
	pass

def setPluginCategory(handle, category):
	"""Sets the plugins name for skins to display."""
	pass

def setPluginFanart(handle, image, color1=None, color2=None, color3=None):
	"""Sets the plugins fanart and color for skins to display."""
	pass

def setProperty(handle, key, value):
	"""Sets a container property for this plugin."""
	pass

# protocols:
#	ftp
#	ftps
#	dav
#	davs
#	http
#	https
#	rtp
#	udp
#	rtmp
#	rtsp

#	filereader
#	shout
#	mms
#	musicdb
#	videodb
#	zip
#	file
#	playlistmusic
#	playlistvideo
#	special
#	upnp
#	plugin
#	musicsearch
#	lastfm
#	rss
#	smb
#	daap
#	hdhomerun
#	sling
#	rtv
#	htsp
#	vtp
#	myth
#	sap
#	sources
#	stack
#	tuxbox
#	multipath
#	rar
#	script
#	addons

