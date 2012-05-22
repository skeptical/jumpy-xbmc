# xbmc/interfaces/python/xbmcmodule/pyutil.h
__author__ = "J. Mulder <darkie@xbmc.org>" # PY_XBMC_AUTHOR
__date__ = "14 July 2006"
__version__ = "1.2"
__credits__ = "XBMC TEAM." # PY_XBMC_CREDITS
__platform__ = "XBOX" # PY_XBMC_PLATFORM

def getCurrentWindowId():
	"""Returns the id for the current 'active' window as an integer."""
	return 0

def getCurrentWindowDialogId():
	"""Returns the id for the current 'active' dialog as an integer."""
	return 0

# xbmc/guilib/GUIListItem.h
ICON_OVERLAY_NONE = 0
ICON_OVERLAY_RAR = 1
ICON_OVERLAY_ZIP = 2
ICON_OVERLAY_LOCKED = 3
ICON_OVERLAY_HAS_TRAINER = 4
ICON_OVERLAY_TRAINED = 5
ICON_OVERLAY_UNWATCHED = 6
ICON_OVERLAY_WATCHED = 7
ICON_OVERLAY_HD = 8

# xbmc/interfaces/python/xbmcmodule/listitem.cpp
class ListItem:

	def __init__(self, label=None, label2=None, iconImage=None, thumbnailImage=None, path=None):
		self.__dict__['label'] = label
		self.__dict__['label2'] = label2
		self.__dict__['iconImage'] = iconImage
		self.__dict__['thumbnailImage'] = thumbnailImage
		self.__dict__['path'] = path
		self.__dict__['type'] = 'VIDEO'
		return

	def getLabel(self):
		"""Returns the listitem label."""
		return self.__dict__['label']

	def getLabel2(self):
		"""Returns the listitem's second label."""
		return self.__dict__['label2']

	def setLabel(self, label):
		"""Sets the listitem's label."""
		self.__dict__['label'] = label

	def setLabel2(self, label2):
		"""Sets the listitem's second label."""
		self.__dict__['label2'] = label2

	def setIconImage(self, icon):
		"""Sets the listitem's icon image."""
		self.__dict__['iconImage'] = icon

	def setThumbnailImage(self, thumb):
		"""Sets the listitem's thumbnail image."""
		self.__dict__['thumbnailImage'] = thumb

	def select(self, selected):
		"""Sets the listitem's selected status."""
		pass

	def isSelected(self):
		"""Returns the listitem's selected status."""
		return False

	def setInfo(self, type, infoLabels):
		"""Sets the listitem's infoLabels."""
		self.__dict__['type'] = type
		self.__dict__.update(infoLabels)
		pass

	def setProperty(self, key, value):
		"""Sets a listitem property, similar to an infolabel."""
		self.__dict__[key] = value

	def getProperty(self, key):
		"""Returns a listitem property as a string, similar to an infolabel."""
		return (self.__dict__[key] if key in self.__dict__ else None)

	def addContextMenuItems(self, items, replaceItems=None):
		"""Adds item to the context menu for media lists."""
		pass

	def setPath(self, path):
		"""Sets the listitem's path."""
		self.__dict__['path'] = path

# xbmc/interfaces/python/xbmcmodule/dialog.cpp
class Dialog:

	def ok(self, heading, line1, line2=None, line3=None):
		"""Show a dialog 'OK'."""
		print "*** dialog OK ***\n%s" % [heading, line1, line2, line3]
		return True

	def browse(self, type, heading, shares, mask=None, useThumbs=None, treatAsFolder=None, default=None, enableMultiple=None):
		"""Show a 'Browse' dialog."""
		print "*** dialog browse ***\n%s" % [heading, shares, default]
		return default

	def numeric(self, type, heading, default=0):
		"""Show a 'Numeric' dialog."""
		print "*** dialog numeric ***\n%s" % [type, heading, default]
		return default

	def yesno(self, heading, line1, line2=None, line3=None, nolabel=None, yeslabel=None):
		"""Show a dialog 'YES/NO'."""
		print "*** dialog YES/NO ***\n%s" % [heading, line1, line2, line3]
		return False

	def select(self, heading, list, autoclose=None):
		"""Show a select dialog."""
		print "*** dialog select ***\n%s%s" % (heading, list)
		return 0

class DialogProgress:

	def create(self, heading, line1=None, line2=None, line3=None):
		"""Create and show a progress dialog."""
		pass

	def update(self, percent, line1=None, line2=None, line3=None):
		"""Update's the progress dialog."""
		pass

	def iscanceled(self):
		"""Returns True if the user pressed cancel."""
		return False

	def close(self):
		"""Close the progress dialog."""
		pass

# xbmc/interfaces/python/xbmcmodule/winxmldialog.cpp
class WindowXMLDialog:
	
	def __init__(self, xmlFilename, scriptPath=None, defaultSkin=None, defaultRes=None):
		"""Create a new WindowXMLDialog script."""
		pass

