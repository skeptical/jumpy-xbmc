import os.path, csv, traceback
from urlparse import urlparse
from cStringIO import StringIO
import xbmcplugin, xbmcgui, xbmcinit

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

SERVER_AIRPLAYSERVER = 2
SERVER_EVENTSERVER = 6
SERVER_JSONRPCSERVER = 3
SERVER_UPNPRENDERER = 4
SERVER_UPNPSERVER = 5
SERVER_WEBSERVER = 1
SERVER_ZEROCONF = 7

abortRequested = False

def log(msg, level=None):
	"""Write a string to XBMC's log file."""
	print msg

output = log # alias for backward compatility

def shutdown():
	"""Shutdown the xbox."""
	pass

def restart():
	"""Restart the xbox."""
	pass

def executescript(script):
	"""Execute a python script."""
	runScript(script)

def executebuiltin(function):
	"""Execute a built in XBMC function."""
	print "**** executebuiltin ****",function

	func,params = function.rsplit(')',2)[0].split('(',2)
	args = []
	for row in csv.reader(StringIO(params)):
		for arg in row:
			try:
				# filter numbers and booleans
				float(arg) or bool(arg)
				args.append(arg)
			except:
				# it must be a string
				args.append(repr(arg))
		break
	code = '%s(%s)' % (func, ','.join(args))
	print "calling %s\n" % code

	try:
		exec code
	except NameError, e:
#		print e
		pass
	except:
		traceback.print_exc(file=sys.stderr)

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
	return _settings['xbmc']['language']

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

# xbmc/GUIInfoManager.cpp
def getInfoLabel(infotag):
	"""Returns an InfoLabel as a string."""
	if infotag == 'System.BuildVersion':
		return "12.0"
	# string/number
	return "0"

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

def translatePath(url, asURL=False):
	"""Returns the translated path."""
	try:
		scheme, loc, path, x, x, x = urlparse(url)
#		print "scheme=%s loc=%s path=%s\nspecial[loc]=%s" % (scheme, loc, path,_special[loc])
		if scheme == 'special' and loc in _special:
			return ('file://' if asURL else '') \
				+ os.path.join(_special[loc], os.path.normpath(path.lstrip('\\/')))
		if scheme == 'plugin':
			dir = os.path.join(_special['home'], 'addons', loc)
			if os.path.isdir(dir):
				return ('file://' if asURL else '') \
					+ os.path.join(dir, os.path.normpath(path.lstrip('\\/')))
	except:
		pass
	return url

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
		self.playlist = None
		self.playing = True;

	def play(self, item=None, listitem=None, windowed=None):
		"""Play this item."""
		print "**** play ****",item, listitem
		if item is not None:
			self.index = 0
			if isinstance(item, PlayList):
				self.playlist = item
			else:
				self.playlist = PlayList(PLAYLIST_VIDEO)
				self.playlist.add(item, listitem)
		elif self.playlist is not None:
			self.index += 1
		# pretend we played something in case 'self' is actually a derived class
		try: self.onPlayBackEnded()
		except: pass

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
		return self.playing

	def isPlayingAudio(self):
		"""returns True is xbmc is playing an audio file."""
		return True

	def isPlayingVideo(self):
		"""returns True if xbmc is playing a video."""
		return True

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
		return 0

	def getTime(self):
		"""Returns the current time of the current playing media as fractional seconds."""
		# pretend to have played for 1 second
		if self.playing:
			self.playing = False
			return 1
		else:
			self.playing = True
			raise Exception("fake playback ended!")

	def seekTime(self):
		"""Seeks the specified amount of time as fractional seconds."""
		pass

	def setSubtitles(self, path):
		"""set subtitle file and enable subtitles"""
		pass

	def getSubtitles(self):
		"""get subtitle stream name."""
		pass

	def showSubtitles(self, visible):
		"""enable/disable subtitles"""
		pass

	def DisableSubtitles(self):
		"""disable subtitles."""
		pass

	def getAvailableAudioStreams(self):
		"""get Audio stream names."""
		pass

	def setAudioStream(self, stream):
		"""set Audio Stream."""
		pass

	def getAvailableSubtitleStreams(self):
		"""get Subtitle stream names."""
		pass

	def setSubtitleStream(self, stream):
		"""set Subtitle Stream."""
		pass

# xbmc/interfaces/python/xbmcmodule/playlist.cpp
class PlayListItem(xbmcgui.ListItem):

	def __init__(self, url=None, listitem=None):
		"""Creates a new PlaylistItem which can be added to a PlayList."""
		xbmcgui.ListItem.__init__(self)
		if listitem is not None:
			self.__dict__.update(listitem.__dict__)
		# url is sometimes 'False'
		if url is not None and url:
			self.__dict__['path'] = url

	def getdescription(self):
		"""Returns the description of this PlayListItem."""
		return getLabel()

	def getduration(self):
		"""Returns the duration of this PlayListItem."""
		return 0

	def getfilename(self):
		"""Returns the filename of this PlayListItem."""
		return self.__dict__['path']

class PlayList:

	def __init__(self, type):
		self.items = []
		self.type = type

	def PlayList(self, playlist):
		"""retrieve a reference from a valid xbmc playlist."""
		pass

	def add(self, url, listitem=None, index=None):
		"""Adds a new file to the playlist."""
		print "**** PlayList.add ****", url, '' if listitem is None else listitem.__dict__
		if not isinstance(url, list):
			url = [url]
		for u in url:
			item = PlayListItem(u, listitem)
			if index is not None:
				self.items.insert(index, item)
				index += 1
			else:
				self.items.append(PlayListItem(u, item))
			xbmcplugin.setResolvedUrl(0, True, item)

	def load(self, filename):
		"""Load a playlist."""
		pass

	def remove(self, filename):
		"""remove an item with this filename from the playlist."""
		print "**** PlayList.remove ****"
		self.items.remove(filename)

	def clear(self):
		"""clear all items in the playlist."""
		self.items = []

	def shuffle(self):
		"""shuffle the playlist."""
		pass

	def unshuffle(self):
		"""unshuffle the playlist."""
		pass

	def size(self):
		"""returns the total number of PlayListItems in this playlist."""
		return len(self.items)

	def getposition(self):
		"""returns the position of the current song in this playlist."""
		pass


# mock everything else

from xbmcinit import mock

InfoTagMusic = \
InfoTagVideo = \
Keyboard = \
Monitor = \
RenderCapture = mock()



# xbmc/interfaces/Builtins.cpp
# http://wiki.xbmc.org/index.php?title=List_of_Built_In_Functions

def PlayMedia(media, isdir=False, preview=1, playoffset=0):
	"""Play the specified media file (or playlist)"""
	#TODO: implement this properly
	Player().play(media)

def RunScript(script, *args):
	"""Run the specified script"""
	cmd = [translatePath(script)]
	cmd.extend(args)
	cmd.append('&')
	pms.run(cmd)

#def StopScript(*args):
#	"""Stop the script by ID or path, if running"""
#	pass

##if defined(TARGET_DARWIN)
#def RunAppleScript(*args):
#	"""Run the specified AppleScript command"""
#	pass
##endif

#def RunPlugin(*args):
#	"""Run the specified plugin"""
#	pass

#def RunAddon(*args):
#	"""Run the specified plugin/script"""
#	pass

#def Extract(*args):
#	"""Extracts the specified archive"""
#	pass


#def System_Exec(*args):
#	"""Execute shell commands"""
#	pass

#def System_ExecWait(*args):
#	"""Execute shell commands and freezes XBMC until shell is closed"""
#	pass

#System = mock()
#System.Exec = System_Exec
#System.ExecWait = System_ExecWait

#def Help():
#	"""This help message"""
#	pass

#def Reboot():
#	"""Reboot the system"""
#	pass

#def Restart():
#	"""Restart the system (same as reboot)"""
#	pass

#def ShutDown():
#	"""Shutdown the system"""
#	pass

#def Powerdown():
#	"""Powerdown system"""
#	pass

#def Quit():
#	"""Quit XBMC"""
#	pass

#def Hibernate():
#	"""Hibernates the system"""
#	pass

#def Suspend():
#	"""Suspends the system"""
#	pass

#def InhibitIdleShutdown():
#	"""Inhibit idle shutdown"""
#	pass

#def AllowIdleShutdown():
#	"""Allow idle shutdown"""
#	pass

#def RestartApp():
#	"""Restart XBMC"""
#	pass

#def Minimize():
#	"""Minimize XBMC"""
#	pass

#def Reset():
#	"""Reset the system (same as reboot)"""
#	pass

#def Mastermode():
#	"""Control master mode"""
#	pass

#def ActivateWindow(*args):
#	"""Activate the specified window"""
#	pass

#def ActivateWindowAndFocus(*args):
#	"""Activate the specified window and sets focus to the specified id"""
#	pass

#def ReplaceWindow(*args):
#	"""Replaces the current window with the new one"""
#	pass

#def TakeScreenshot():
#	"""Takes a Screenshot"""
#	pass

#def SlideShow(*args):
#	"""Run a slideshow from the specified directory"""
#	pass

#def RecursiveSlideShow(*args):
#	"""Run a slideshow from the specified directory, including all subdirs"""
#	pass

#def ReloadSkin():
#	"""Reload XBMC's skin"""
#	pass

#def UnloadSkin():
#	"""Unload XBMC's skin"""
#	pass

#def RefreshRSS():
#	"""Reload RSS feeds from RSSFeeds.xml"""
#	pass

#def PlayerControl(*args):
#	"""Control the music or video player"""
#	pass

#def Playlist.PlayOffset(*args):
#	"""Start playing from a particular offset in the playlist"""
#	pass

#def Playlist.Clear():
#	"""Clear the current playlist"""
#	pass

#def EjectTray():
#	"""Close or open the DVD tray"""
#	pass

#def AlarmClock(*args):
#	"""Prompt for a length of time and start an alarm clock"""
#	pass

#def CancelAlarm(*args):
#	"""Cancels an alarm"""
#	pass

#def Action(*args):
#	"""Executes an action for the active window (same as in keymap)"""
#	pass

#def Notification(*args):
#	"""Shows a notification on screen, specify header, then message, and optionally time in milliseconds and a icon."""
#	pass

#def PlayDVD():
#	"""Plays the inserted CD or DVD media from the DVD-ROM Drive!"""
#	pass

#def RipCD():
#	"""Rip the currently inserted audio CD"""
#	pass

#def Skin.ToggleSetting(*args):
#	"""Toggles a skin setting on or off"""
#	pass

#def Skin.SetString(*args):
#	"""Prompts and sets skin string"""
#	pass

#def Skin.SetNumeric(*args):
#	"""Prompts and sets numeric input"""
#	pass

#def Skin.SetPath(*args):
#	"""Prompts and sets a skin path"""
#	pass

#def Skin.Theme(*args):
#	"""Control skin theme"""
#	pass

#def Skin.SetImage(*args):
#	"""Prompts and sets a skin image"""
#	pass

#def Skin.SetLargeImage(*args):
#	"""Prompts and sets a large skin images"""
#	pass

#def Skin.SetFile(*args):
#	"""Prompts and sets a file"""
#	pass

#def Skin.SetAddon(*args):
#	"""Prompts and set an addon"""
#	pass

#def Skin.SetBool(*args):
#	"""Sets a skin setting on"""
#	pass

#def Skin.Reset(*args):
#	"""Resets a skin setting to default"""
#	pass

#def Skin.ResetSettings():
#	"""Resets all skin settings"""
#	pass

#def Mute():
#	"""Mute the player"""
#	pass

#def SetVolume(*args):
#	"""Set the current volume"""
#	pass

#def Dialog.Close(*args):
#	"""Close a dialog"""
#	pass

#def System.LogOff():
#	"""Log off current user"""
#	pass

#def Resolution(*args):
#	"""Change XBMC's Resolution"""
#	pass

#def SetFocus(*args):
#	"""Change current focus to a different control id"""
#	pass

#def UpdateLibrary(*args):
#	"""Update the selected library (music or video)"""
#	pass

#def CleanLibrary(*args):
#	"""Clean the video/music library"""
#	pass

#def ExportLibrary(*args):
#	"""Export the video/music library"""
#	pass

#def PageDown(*args):
#	"""Send a page down event to the pagecontrol with given id"""
#	pass

#def PageUp(*args):
#	"""Send a page up event to the pagecontrol with given id"""
#	pass

#def LastFM.Love():
#	"""Add the current playing last.fm radio track to the last.fm loved tracks"""
#	pass

#def LastFM.Ban():
#	"""Ban the current playing last.fm radio track"""
#	pass

#def Container.Refresh():
#	"""Refresh current listing"""
#	pass

#def Container.Update():
#	"""Update current listing. Send Container.Update(path,replace) to reset the path history"""
#	pass

#def Container.NextViewMode():
#	"""Move to the next view type (and refresh the listing)"""
#	pass

#def Container.PreviousViewMode():
#	"""Move to the previous view type (and refresh the listing)"""
#	pass

#def Container.SetViewMode(*args):
#	"""Move to the view with the given id"""
#	pass

#def Container.NextSortMethod():
#	"""Change to the next sort method"""
#	pass

#def Container.PreviousSortMethod():
#	"""Change to the previous sort method"""
#	pass

#def Container.SetSortMethod(*args):
#	"""Change to the specified sort method"""
#	pass

#def Container.SortDirection():
#	"""Toggle the sort direction"""
#	pass

#def Control.Move(*args):
#	"""Tells the specified control to 'move' to another entry specified by offset"""
#	pass

#def Control.SetFocus(*args):
#	"""Change current focus to a different control id"""
#	pass

#def Control.Message(*args):
#	"""Send a given message to a control within a given window"""
#	pass

#def SendClick(*args):
#	"""Send a click message from the given control to the given window"""
#	pass

#def LoadProfile(*args):
#	"""Load the specified profile (note; if locks are active it won't work)"""
#	pass

#def SetProperty(*args):
#	"""Sets a window property for the current focused window/dialog (key,value)"""
#	pass

#def ClearProperty(*args):
#	"""Clears a window property for the current focused window/dialog (key,value)"""
#	pass

#def PlayWith(*args):
#	"""Play the selected item with the specified core"""
#	pass

#def WakeOnLan(*args):
#	"""Sends the wake-up packet to the broadcast address for the specified MAC address"""
#	pass

#def Addon.Default.OpenSettings(*args):
#	"""Open a settings dialog for the default addon of the given type"""
#	pass

#def Addon.Default.Set(*args):
#	"""Open a select dialog to allow choosing the default addon of the given type"""
#	pass

#def Addon.OpenSettings(*args):
#	"""Open a settings dialog for the addon of the given id"""
#	pass

#def UpdateAddonRepos():
#	"""Check add-on repositories for updates"""
#	pass

#def UpdateLocalAddons():
#	"""Check for local add-on changes"""
#	pass

#def ToggleDPMS():
#	"""Toggle DPMS mode manually"""
#	pass

#def Weather.Refresh():
#	"""Force weather data refresh"""
#	pass

#def Weather.LocationNext():
#	"""Switch to next weather location"""
#	pass

#def Weather.LocationPrevious():
#	"""Switch to previous weather location"""
#	pass

#def Weather.LocationSet(*args):
#	"""Switch to given weather location (parameter can be 1-3)"""
#	pass

##if defined(HAS_LIRC) || defined(HAS_IRSERVERSUITE)
#def LIRC.Stop():
#	"""Removes XBMC as LIRC client"""
#	pass

#def LIRC.Start():
#	"""Adds XBMC as LIRC client"""
#	pass

#def LIRC.Send(*args):
#	"""Sends a command to LIRC"""
#	pass
##endif

##ifdef HAS_LCD
#def LCD.Suspend():
#	"""Suspends LCDproc"""
#	pass

#def LCD.Resume():
#	"""Resumes LCDproc"""
#	pass
##endif

#def VideoLibrary.Search():
#	"""Brings up a search dialog which will search the library"""
#	pass

#def ToggleDebug():
#	"""Enables/disables debug mode"""
#	pass

#def StartPVRManager():
#	"""(Re)Starts the PVR manager"""
#	pass

#def StopPVRManager():
#	"""Stops the PVR manager"""
#	pass

