from xml.etree.ElementTree import ElementTree
#import jumpy
import xbmcplugin #, xbmcinit

# xbmc/interfaces/python/xbmcmodule/pyutil.h
__author__ = "J. Mulder <darkie@xbmc.org>" # PY_XBMC_AUTHOR
__date__ = "15 November 2005"
__version__ = "1.3"
__credits__ = "XBMC TEAM." # PY_XBMC_CREDITS
__platform__ = "XBOX" # PY_XBMC_PLATFORM

# xbmc/PlayListPlayer.h
PLAYLIST_NONE = -1
PLAYLIST_MUSIC = 0
PLAYLIST_VIDEO = 1
PLAYLIST_PICTURE = 2

# xbmc/cores/playercorefactory/PlayerCoreFactory.h
PLAYER_CORE_AUTO = 0 # EPC_NONE
PLAYER_CORE_DVDPLAYER = 1 # EPC_DVDPLAYER
PLAYER_CORE_MPLAYER = 2 # EPC_MPLAYER
PLAYER_CORE_PAPLAYER = 3 # EPC_PAPLAYER

# xbmc/storage/IoSupport.h
TRAY_OPEN = 16
DRIVE_NOT_READY = 1
TRAY_CLOSED_NO_MEDIA = 64
TRAY_CLOSED_MEDIA_PRESENT = 96

# xbmc/utils/log.h
LOGDEBUG = 0
LOGINFO = 1
LOGNOTICE = 2
LOGWARNING = 3
LOGERROR = 4
LOGSEVERE = 5
LOGFATAL = 6
LOGNONE = 7

# xbmc/cores/VideoRenderers/RenderCapture.h
CAPTURE_STATE_WORKING = 0 # CAPTURESTATE_WORKING
CAPTURE_STATE_DONE = 3 # CAPTURESTATE_DONE
CAPTURE_STATE_FAILED = 4 # CAPTURESTATE_FAILED
CAPTURE_FLAG_CONTINUOUS = 1 # CAPTUREFLAG_CONTINUOUS
CAPTURE_FLAG_IMMEDIATELY = 2 # CAPTUREFLAG_IMMEDIATELY


def log(msg, level=None):
	"""Write a string to XBMC's log file."""
	pass

def shutdown():
	"""Shutdown the xbox."""
	pass

def restart():
	"""Restart the xbox."""
	pass

def executescript(script):
	"""Execute a python script."""
	pass

def executebuiltin(function):
	"""Execute a built in XBMC function."""
	pass

def executehttpapi(httpcommand):
	"""Execute an HTTP API command."""
	return ""

def executeJSONRPC(jsonrpccommand):
	"""Execute an JSONRPC command."""
	return ""

def sleep(time):
	"""Sleeps for 'time' msec."""
	pass

def getLocalizedString(id):
	"""Returns a localized 'unicode string'."""
	return u""

def getSkinDir():
	"""Returns the active skin directory as a string."""
	return ""

def getLanguage():
	"""Returns the active language as a string."""
	return ""

def getIPAddress():
	"""Returns the current ip address as a string."""
	return ""

def getDVDState():
	"""Returns the dvd state as an integer."""
	return 0

def getFreeMem():
	"""Returns the amount of free memory in MB as an integer."""
	return 0

def getCpuTemp():
	"""Returns the current cpu temperature as an integer."""
	return 0

def getInfoLabel(infotag):
	"""Returns an InfoLabel as a string."""
	return ""

def getInfoImage(infotag):
	"""Returns a filename including path to the InfoImage's"""
	return ""

def playSFX(filename):
	"""Plays a wav file by filename"""
	pass

def enableNavSounds(yesNo):
	"""Enables/Disables nav sounds"""
	pass

def getCondVisibility(condition):
	"""Returns True (1) or False (0) as a bool."""
	return False;

def getGlobalIdleTime():
	"""Returns the elapsed idle time in seconds as an integer."""
	return 0

def getCacheThumbName(path):
	"""Returns a thumb cache filename."""
	return ""

def makeLegalFilename(filename, fatX=None):
	"""Returns a legal filename or path as a string."""
	return ""

def translatePath(path, asURL=False):
	"""Returns the translated path."""
	try:
		protocol, nil, loc, path = path.split('/', 3)
		if protocol == 'special:' and loc in _special:
			return 'file://' if asURL else '' + os.path.join(_special[loc], path)
		if protocol == 'plugin:':
			dir = os.path.join(_special['home'], 'addons', loc)
			if os.path.isdir(dir):
				return 'file://' if asURL else '' + os.path.join(dir, path)
#			xml = os.path.join(dir, 'addon.xml')
#			if os.path.isfile(xml):
#				addon = ElementTree()
#				addon.parse(xml)
#				script = addon.find('.//extension[@point="xbmc.python.pluginsource"]').attrib['library']
#				return os.path.join(dir, script)
	except:
		pass	
	return path

def getCleanMovieTitle(path, usefoldername=None):
	"""Returns a clean movie title and year string if available."""
	return ""

def validatePath(path):
	"""Returns the validated path."""
	return path

def getRegion(id):
	"""Returns your regions setting as a string for the specified id."""
	return ""

def getSupportedMedia(media):
	"""Returns the supported file types for the specific media as a string."""
	return ""

def skinHasImage(image):
	"""Returns True if the image file exists in the skin."""
	return False;

def subHashAndFileSize(file):
	"""Calculate subtitle hash and size."""
	return ("0", "0")

# xbmc/interfaces/python/xbmcmodule/player.cpp
class Player:

	def __init__(self, core=None):
		"""Creates a new Player with as default the xbmc music playlist."""
		pass

	def play(self, item=None, listitem=None, windowed=None):
		"""Play this item."""
		listitem.setProperty('path', item)
		xbmcplugin.setResolvedUrl(0, True, listitem)

	def stop(self):
		"""Stop playing."""
		pass

	def pause(self):
		"""Pause playing."""
		pass

	def playnext(self):
		"""Play next item in playlist."""
		pass

	def playprevious(self):
		"""Play previous item in playlist."""
		pass

	def playselected(self):
		"""Play a certain item from the current playlist."""
		pass

	def onPlayBackStarted(self):
		"""onPlayBackStarted method."""
		pass

	def onPlayBackEnded(self):
		"""onPlayBackEnded method."""
		pass

	def onPlayBackStopped(self):
		"""onPlayBackStopped method."""
		pass

	def onPlayBackPaused(self):
		"""onPlayBackPaused method."""
		pass

	def onPlayBackResumed(self):
		"""onPlayBackResumed method."""
		pass

	def isPlaying(self):
		"""returns True is xbmc is playing a file."""
		pass

	def isPlayingAudio(self):
		"""returns True is xbmc is playing an audio file."""
		pass

	def isPlayingVideo(self):
		"""returns True if xbmc is playing a video."""
		pass

	def getPlayingFile(self):
		"""returns the current playing file as a string."""
		pass

	def getVideoInfoTag(self):
		"""returns the VideoInfoTag of the current playing Movie."""
		pass

	def getMusicInfoTag(self):
		"""returns the MusicInfoTag of the current playing 'Song'."""
		pass

	def getTotalTime(self):
		"""Returns the total time of the current playing media in"""
		pass

	def getTime(self):
		"""Returns the current time of the current playing media as fractional seconds."""
		pass

	def seekTime(self):
		"""Seeks the specified amount of time as fractional seconds."""
		pass

	def setSubtitles(self, path):
		"""set subtitle file and enable subtitles"""
		pass

	def getSubtitles(self):
		"""get subtitle stream name\n"""
		pass

	def showSubtitles(self, visible):
		"""enable/disable subtitles"""
		pass

	def DisableSubtitles(self):
		"""disable subtitles\n"""
		pass

	def getAvailableAudioStreams(self):
		"""get Audio stream names\n"""
		pass

	def setAudioStream(self, stream):
		"""set Audio Stream """
		pass

	def getAvailableSubtitleStreams(self):
		"""get Subtitle stream names\n"""
		pass

	def setSubtitleStream(self, stream):
		"""set Subtitle Stream """
		pass

