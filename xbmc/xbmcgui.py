from UserDict import DictMixin
import xbmcinit

def getCurrentWindowId():
	"""Returns the id for the current 'active' window as an integer."""
	return 0

def getCurrentWindowDialogId():
	"""Returns the id for the current 'active' dialog as an integer."""
	return 0

# constants

ACTION_ANALOG_FORWARD = 113
ACTION_ANALOG_MOVE = 49
ACTION_ANALOG_MOVE_X = 601
ACTION_ANALOG_MOVE_Y = 602
ACTION_ANALOG_REWIND = 114
ACTION_ANALOG_SEEK_BACK = 125
ACTION_ANALOG_SEEK_FORWARD = 124
ACTION_ASPECT_RATIO = 19
ACTION_AUDIO_DELAY = 161
ACTION_AUDIO_DELAY_MIN = 54
ACTION_AUDIO_DELAY_PLUS = 55
ACTION_AUDIO_NEXT_LANGUAGE = 56
ACTION_BACKSPACE = 110
ACTION_BIG_STEP_BACK = 23
ACTION_BIG_STEP_FORWARD = 22
ACTION_BUILT_IN_FUNCTION = 122
ACTION_CALIBRATE_RESET = 48
ACTION_CALIBRATE_SWAP_ARROWS = 47
ACTION_CHANGE_RESOLUTION = 57
ACTION_CHANNEL_DOWN = 185
ACTION_CHANNEL_SWITCH = 183
ACTION_CHANNEL_UP = 184
ACTION_CHAPTER_OR_BIG_STEP_BACK = 98
ACTION_CHAPTER_OR_BIG_STEP_FORWARD = 97
ACTION_CONTEXT_MENU = 117
ACTION_COPY_ITEM = 81
ACTION_CREATE_BOOKMARK = 96
ACTION_CREATE_EPISODE_BOOKMARK = 95
ACTION_CURSOR_LEFT = 120
ACTION_CURSOR_RIGHT = 121
ACTION_CYCLE_SUBTITLE = 99
ACTION_DECREASE_PAR = 220
ACTION_DECREASE_RATING = 137
ACTION_DELETE_ITEM = 80
ACTION_ENTER = 135
ACTION_ERROR = 998
ACTION_FILTER = 233
ACTION_FILTER_CLEAR = 150
ACTION_FILTER_SMS2 = 151
ACTION_FILTER_SMS3 = 152
ACTION_FILTER_SMS4 = 153
ACTION_FILTER_SMS5 = 154
ACTION_FILTER_SMS6 = 155
ACTION_FILTER_SMS7 = 156
ACTION_FILTER_SMS8 = 157
ACTION_FILTER_SMS9 = 158
ACTION_FIRST_PAGE = 159
ACTION_FORWARD = 16
ACTION_GESTURE_BEGIN = 501
ACTION_GESTURE_END = 599
ACTION_GESTURE_NOTIFY = 500
ACTION_GESTURE_PAN = 504
ACTION_GESTURE_ROTATE = 503
ACTION_GESTURE_SWIPE_DOWN = 541
ACTION_GESTURE_SWIPE_DOWN_TEN = 550
ACTION_GESTURE_SWIPE_LEFT = 511
ACTION_GESTURE_SWIPE_LEFT_TEN = 520
ACTION_GESTURE_SWIPE_RIGHT = 521
ACTION_GESTURE_SWIPE_RIGHT_TEN = 530
ACTION_GESTURE_SWIPE_UP = 531
ACTION_GESTURE_SWIPE_UP_TEN = 540
ACTION_GESTURE_ZOOM = 502
ACTION_GUIPROFILE_BEGIN = 204
ACTION_HIGHLIGHT_ITEM = 8
ACTION_INCREASE_PAR = 219
ACTION_INCREASE_RATING = 136
ACTION_INPUT_TEXT = 244
ACTION_JUMP_SMS2 = 142
ACTION_JUMP_SMS3 = 143
ACTION_JUMP_SMS4 = 144
ACTION_JUMP_SMS5 = 145
ACTION_JUMP_SMS6 = 146
ACTION_JUMP_SMS7 = 147
ACTION_JUMP_SMS8 = 148
ACTION_JUMP_SMS9 = 149
ACTION_LAST_PAGE = 160
ACTION_MOUSE_DOUBLE_CLICK = 103
ACTION_MOUSE_DRAG = 106
ACTION_MOUSE_END = 109
ACTION_MOUSE_LEFT_CLICK = 100
ACTION_MOUSE_LONG_CLICK = 108
ACTION_MOUSE_MIDDLE_CLICK = 102
ACTION_MOUSE_MOVE = 107
ACTION_MOUSE_RIGHT_CLICK = 101
ACTION_MOUSE_START = 100
ACTION_MOUSE_WHEEL_DOWN = 105
ACTION_MOUSE_WHEEL_UP = 104
ACTION_MOVE_DOWN = 4
ACTION_MOVE_ITEM = 82
ACTION_MOVE_ITEM_DOWN = 116
ACTION_MOVE_ITEM_UP = 115
ACTION_MOVE_LEFT = 1
ACTION_MOVE_RIGHT = 2
ACTION_MOVE_UP = 3
ACTION_MUTE = 91
ACTION_NAV_BACK = 92
ACTION_NEXT_CHANNELGROUP = 186
ACTION_NEXT_CONTROL = 181
ACTION_NEXT_ITEM = 14
ACTION_NEXT_LETTER = 140
ACTION_NEXT_PICTURE = 28
ACTION_NEXT_SCENE = 138
ACTION_NEXT_SUBTITLE = 26
ACTION_NONE = 0
ACTION_NOOP = 999
ACTION_OSD_HIDESUBMENU = 84
ACTION_OSD_SHOW_DOWN = 72
ACTION_OSD_SHOW_LEFT = 69
ACTION_OSD_SHOW_RIGHT = 70
ACTION_OSD_SHOW_SELECT = 73
ACTION_OSD_SHOW_UP = 71
ACTION_OSD_SHOW_VALUE_MIN = 75
ACTION_OSD_SHOW_VALUE_PLUS = 74
ACTION_PAGE_DOWN = 6
ACTION_PAGE_UP = 5
ACTION_PARENT_DIR = 9
ACTION_PASTE = 180
ACTION_PAUSE = 12
ACTION_PLAY = 68
ACTION_PLAYER_FORWARD = 77
ACTION_PLAYER_PLAY = 79
ACTION_PLAYER_PLAYPAUSE = 229
ACTION_PLAYER_REWIND = 78
ACTION_PREVIOUS_CHANNELGROUP = 187
ACTION_PREVIOUS_MENU = 10
ACTION_PREV_CONTROL = 182
ACTION_PREV_ITEM = 15
ACTION_PREV_LETTER = 141
ACTION_PREV_PICTURE = 29
ACTION_PREV_SCENE = 139
ACTION_PVR_PLAY = 188
ACTION_PVR_PLAY_RADIO = 190
ACTION_PVR_PLAY_TV = 189
ACTION_QUEUE_ITEM = 34
ACTION_RECORD = 170
ACTION_RELOAD_KEYMAPS = 203
ACTION_REMOVE_ITEM = 35
ACTION_RENAME_ITEM = 87
ACTION_REWIND = 17
ACTION_ROTATE_PICTURE_CCW = 51
ACTION_ROTATE_PICTURE_CW = 50
ACTION_SCAN_ITEM = 201
ACTION_SCROLL_DOWN = 112
ACTION_SCROLL_UP = 111
ACTION_SELECT_ITEM = 7
ACTION_SETTINGS_LEVEL_CHANGE = 242
ACTION_SETTINGS_RESET = 241
ACTION_SHIFT = 118
ACTION_SHOW_CODEC = 27
ACTION_SHOW_FULLSCREEN = 36
ACTION_SHOW_GUI = 18
ACTION_SHOW_INFO = 11
ACTION_SHOW_MPLAYER_OSD = 83
ACTION_SHOW_OSD = 24
ACTION_SHOW_OSD_TIME = 123
ACTION_SHOW_PLAYLIST = 33
ACTION_SHOW_SUBTITLES = 25
ACTION_SHOW_VIDEOMENU = 134
ACTION_SMALL_STEP_BACK = 76
ACTION_STEP_BACK = 21
ACTION_STEP_FORWARD = 20
ACTION_STEREOMODE_NEXT = 235
ACTION_STEREOMODE_PREVIOUS = 236
ACTION_STEREOMODE_SELECT = 238
ACTION_STEREOMODE_SET = 240
ACTION_STEREOMODE_TOGGLE = 237
ACTION_STEREOMODE_TOMONO = 239
ACTION_STOP = 13
ACTION_SUBTITLE_ALIGN = 232
ACTION_SUBTITLE_DELAY = 162
ACTION_SUBTITLE_DELAY_MIN = 52
ACTION_SUBTITLE_DELAY_PLUS = 53
ACTION_SUBTITLE_VSHIFT_DOWN = 231
ACTION_SUBTITLE_VSHIFT_UP = 230
ACTION_SWITCH_PLAYER = 234
ACTION_SYMBOLS = 119
ACTION_TAKE_SCREENSHOT = 85
ACTION_TELETEXT_BLUE = 218
ACTION_TELETEXT_GREEN = 216
ACTION_TELETEXT_RED = 215
ACTION_TELETEXT_YELLOW = 217
ACTION_TOGGLE_DIGITAL_ANALOG = 202
ACTION_TOGGLE_FULLSCREEN = 199
ACTION_TOGGLE_SOURCE_DEST = 32
ACTION_TOGGLE_WATCHED = 200
ACTION_TOUCH_LONGPRESS = 411
ACTION_TOUCH_LONGPRESS_TEN = 420
ACTION_TOUCH_TAP = 401
ACTION_TOUCH_TAP_TEN = 410
ACTION_TRIGGER_OSD = 243
ACTION_VIS_PRESET_LOCK = 130
ACTION_VIS_PRESET_NEXT = 128
ACTION_VIS_PRESET_PREV = 129
ACTION_VIS_PRESET_RANDOM = 131
ACTION_VIS_PRESET_SHOW = 126
ACTION_VIS_RATE_PRESET_MINUS = 133
ACTION_VIS_RATE_PRESET_PLUS = 132
ACTION_VOLAMP = 90
ACTION_VOLAMP_DOWN = 94
ACTION_VOLAMP_UP = 93
ACTION_VOLUME_DOWN = 89
ACTION_VOLUME_SET = 245
ACTION_VOLUME_UP = 88
ACTION_VSHIFT_DOWN = 228
ACTION_VSHIFT_UP = 227
ACTION_ZOOM_IN = 31
ACTION_ZOOM_LEVEL_1 = 38
ACTION_ZOOM_LEVEL_2 = 39
ACTION_ZOOM_LEVEL_3 = 40
ACTION_ZOOM_LEVEL_4 = 41
ACTION_ZOOM_LEVEL_5 = 42
ACTION_ZOOM_LEVEL_6 = 43
ACTION_ZOOM_LEVEL_7 = 44
ACTION_ZOOM_LEVEL_8 = 45
ACTION_ZOOM_LEVEL_9 = 46
ACTION_ZOOM_LEVEL_NORMAL = 37
ACTION_ZOOM_OUT = 30
ALPHANUM_HIDE_INPUT = 2
CONTROL_TEXT_OFFSET_X = 10
CONTROL_TEXT_OFFSET_Y = 2
ICON_OVERLAY_HD = 6
ICON_OVERLAY_LOCKED = 3
ICON_OVERLAY_HAS_TRAINER = 4 # obsolete
ICON_OVERLAY_TRAINED = 5 # obsolete
ICON_OVERLAY_NONE = 0
ICON_OVERLAY_RAR = 1
ICON_OVERLAY_UNWATCHED = 4
ICON_OVERLAY_WATCHED = 5
ICON_OVERLAY_ZIP = 2
ICON_TYPE_FILES = 106
ICON_TYPE_MUSIC = 103
ICON_TYPE_NONE = 101
ICON_TYPE_PICTURES = 104
ICON_TYPE_PROGRAMS = 102
ICON_TYPE_SETTINGS = 109
ICON_TYPE_VIDEOS = 105
ICON_TYPE_WEATHER = 107
INPUT_ALPHANUM = 0
INPUT_DATE = 2
INPUT_IPADDRESS = 4
INPUT_NUMERIC = 1
INPUT_PASSWORD = 5
INPUT_TIME = 3
KEY_APPCOMMAND = 53248
KEY_ASCII = 61696
KEY_BUTTON_A = 256
KEY_BUTTON_B = 257
KEY_BUTTON_BACK = 275
KEY_BUTTON_BLACK = 260
KEY_BUTTON_DPAD_DOWN = 271
KEY_BUTTON_DPAD_LEFT = 272
KEY_BUTTON_DPAD_RIGHT = 273
KEY_BUTTON_DPAD_UP = 270
KEY_BUTTON_LEFT_ANALOG_TRIGGER = 278
KEY_BUTTON_LEFT_THUMB_BUTTON = 276
KEY_BUTTON_LEFT_THUMB_STICK = 264
KEY_BUTTON_LEFT_THUMB_STICK_DOWN = 281
KEY_BUTTON_LEFT_THUMB_STICK_LEFT = 282
KEY_BUTTON_LEFT_THUMB_STICK_RIGHT = 283
KEY_BUTTON_LEFT_THUMB_STICK_UP = 280
KEY_BUTTON_LEFT_TRIGGER = 262
KEY_BUTTON_RIGHT_ANALOG_TRIGGER = 279
KEY_BUTTON_RIGHT_THUMB_BUTTON = 277
KEY_BUTTON_RIGHT_THUMB_STICK = 265
KEY_BUTTON_RIGHT_THUMB_STICK_DOWN = 267
KEY_BUTTON_RIGHT_THUMB_STICK_LEFT = 268
KEY_BUTTON_RIGHT_THUMB_STICK_RIGHT = 269
KEY_BUTTON_RIGHT_THUMB_STICK_UP = 266
KEY_BUTTON_RIGHT_TRIGGER = 263
KEY_BUTTON_START = 274
KEY_BUTTON_WHITE = 261
KEY_BUTTON_X = 258
KEY_BUTTON_Y = 259
KEY_INVALID = 65535
KEY_MOUSE_CLICK = 57344
KEY_MOUSE_DOUBLE_CLICK = 57360
KEY_MOUSE_DRAG = 57604
KEY_MOUSE_DRAG_END = 57606
KEY_MOUSE_DRAG_START = 57605
KEY_MOUSE_END = 61439
KEY_MOUSE_LONG_CLICK = 57376
KEY_MOUSE_MIDDLECLICK = 57346
KEY_MOUSE_MOVE = 57603
KEY_MOUSE_NOOP = 61439
KEY_MOUSE_RDRAG = 57607
KEY_MOUSE_RDRAG_END = 57609
KEY_MOUSE_RDRAG_START = 57608
KEY_MOUSE_RIGHTCLICK = 57345
KEY_MOUSE_START = 57344
KEY_MOUSE_WHEEL_DOWN = 57602
KEY_MOUSE_WHEEL_UP = 57601
KEY_TOUCH = 61440
KEY_UNICODE = 61952
KEY_VKEY = 61440
KEY_VMOUSE = 61439
NOTIFICATION_ERROR = 'error'
NOTIFICATION_INFO = 'info'
NOTIFICATION_WARNING = 'warning'
PASSWORD_VERIFY = 1
REMOTE_0 = 58
REMOTE_1 = 59
REMOTE_2 = 60
REMOTE_3 = 61
REMOTE_4 = 62
REMOTE_5 = 63
REMOTE_6 = 64
REMOTE_7 = 65
REMOTE_8 = 66
REMOTE_9 = 67

class case_insensitive_dict(DictMixin):
	def __init__(self):
		self.data = {}

	def __getitem__(self, key):
		return self.data[key.lower()]

	def __setitem__(self, key, item):
		self.data[key.lower()] = item

	def __delitem__(self, key):
		if key.lower() in self.data:
			del self.data[key.lower()]
		else:
			raise KeyError(key)

	def keys(self):
		return self.data.keys()


# xbmc/interfaces/python/xbmcmodule/listitem.cpp
class ListItem:

	def __init__(self, label=None, label2=None, iconImage=None, thumbnailImage=None, path=None):
		self.data = case_insensitive_dict()
		self.data['label'] = label
		self.data['label2'] = label2
		self.data['iconImage'] = iconImage
		self.data['thumbnailImage'] = thumbnailImage
		self.data['path'] = path
		self.data['type'] = 'VIDEO'
		self.data['streams'] = []
		return

	def getLabel(self):
		"""Returns the listitem label."""
		return self.data['label']

	def getLabel2(self):
		"""Returns the listitem's second label."""
		return self.data['label2']

	def setLabel(self, label):
		"""Sets the listitem's label."""
		self.data['label'] = label

	def setLabel2(self, label2):
		"""Sets the listitem's second label."""
		self.data['label2'] = label2

	def setIconImage(self, icon):
		"""Sets the listitem's icon image."""
		self.data['iconImage'] = icon

	def setThumbnailImage(self, thumb):
		"""Sets the listitem's thumbnail image."""
		self.data['thumbnailImage'] = thumb

	def select(self, selected):
		"""Sets the listitem's selected status."""
		pass

	def setInfo(self, type, infoLabels):
		"""Sets the listitem's infoLabels."""
		self.data['type'] = type
		self.data.update(infoLabels)

	def setProperty(self, key, value):
		"""Sets a listitem property, similar to an infolabel."""
		self.data[key] = value

	def getProperty(self, key):
		"""Returns a listitem property as a string, similar to an infolabel."""
		return (self.data[key] if key in self.data else None)

	def addContextMenuItems(self, items, replaceItems=None):
		"""Adds item to the context menu for media lists."""
		pass

	def setPath(self, path):
		"""Sets the listitem's path."""
		self.data['path'] = path

	def addStreamInfo(self, type, values):
		"""Add a stream with details."""
		print "*** addStreamInfo ***", [type, values]
		values['type'] = type
		self.data['streams'].append({k.lower():values[k] for k in values.keys()})

	def getMusicInfoTag(self):
		"""returns the MusicInfoTag for this item."""
		return None

	def getVideoInfoTag(self):
		"""returns the VideoInfoTag for this item."""
		return None

	def getdescription(self):
		"""Returns the description of this PlayListItem."""
		return None

	def getduration(self):
		"""Returns the duration of this PlayListItem"""
		return 0

	def getfilename(self):
		"""Returns the filename of this PlayListItem."""
		return None

	def isSelected(self):
		"""Returns the listitem's selected status."""
		return False

	def setArt(self, values):
		"""Sets the listitem's art"""
		self.data['art'] = values

	def setMimeType(self, mimetype):
		"""Sets the listitem's mimetype if known."""
		self.data['mimetype'] = mimetype

	def setSubtitles(self, subtitles):
		"""Sets subtitles for this listitem."""
		self.data['subtitles'] = subtitles


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
		return self.choose('numeric', heading, [], default)

	def yesno(self, heading, line1, line2=None, line3=None, nolabel='no', yeslabel='yes'):
		"""Show a dialog 'YES/NO'."""
		query = '%s%s%s%s' % (heading or '', line1 or '', line2 or '', line3 or '')
		sel = self.choose('YES/NO', query, [yeslabel, nolabel])
		return (True if sel == 0 else False)

	def select(self, heading, list, autoclose=None):
		"""Show a select dialog."""
		return self.choose('select', heading, list)

	def choose(self, type, query, list, default=0):
		try: _dialogs
		except: xbmcinit.read_dialogs()
		dlg = '%s %s %s' % (repr(query), list, _mainid)
		sel = (_dialogs[dlg] if dlg in _dialogs else default)
		print "*** dialog %s ***\n%s <<< %s" % (type, sel, dlg)
		return sel

	def notification(self, heading, message, icon=NOTIFICATION_INFO, time=5000, sound=True):
		"""Show a Notification alert."""
		print "*** dialog notification ***\n%s" % [heading, message, icon, time, sound]

	def input(self, heading, default='', type=INPUT_ALPHANUM, option=0, autoclose=False):
		"""Show an Input dialog."""
		print "*** dialog input ***\n%s" % [heading, default, type, option, autoclose]
		return default

# mock everything else, mostly

from xbmcinit import mock

Action = \
Control = \
ControlButton = \
ControlCheckMark = \
ControlEdit = \
ControlFadeLabel = \
ControlGroup = \
ControlImage = \
ControlLabel = \
ControlList = \
ControlProgress = \
ControlRadioButton = \
ControlSlider = \
ControlSpin = \
ControlTextBox = \
DialogProgress = \
DialogProgressBG = \
Window = \
WindowDialog = \
WindowXML = \
WindowXMLDialog = mock()

Window.getResolution = lambda:5 # NTSC 16:9 (720x480)
Window.getWidth = lambda:720
Window.getHeight = lambda:480

import xbmcplugin

#class DialogProgress:

#	def create(self, heading, line1=None, line2=None, line3=None):
#		"""Create and show a progress dialog."""
#		pass

#	def update(self, percent, line1=None, line2=None, line3=None):
#		"""Update's the progress dialog."""
#		pass

#	def iscanceled(self):
#		"""Returns True if the user pressed cancel."""
#		return False

#	def close(self):
#		"""Close the progress dialog."""
#		pass

#class Window:

#	def __init__(self, windowId):
#		self.properties = {}
#		self.properties['windowId'] = windowId;

#	def addControl(self, control):
#		"""Add a Control to this window."""
#		pass

#	def addControls(self, controlList):
#		"""Add a list of Controls to this window."""
#		pass

#	def clearProperties(self):
#		"""Clears all window properties."""
#		self.properties = {}

#	def clearProperty(self, key):
#		"""Clears the specific window property."""
#		self.properties[key] = None

#	def close(self):
#		"""Closes this window."""
#		pass

#	def doModal(self):
#		"""Display this window until close() is called."""
#		pass

#	def getControl(self, controlId):
#		"""Get's the control from this window."""
#		pass

#	def getFocus(self, control):
#		"""returns the control which is focused."""
#		pass

#	def getFocusId(self):
#		"""returns the id of the control which is focused."""
#		return 0

#	def getHeight(self):
#		"""Returns the height of this screen."""
#		return 480

#	def getProperty(self, key):
#		"""Returns a window property as a string, similar to an infolabel."""
#		return self.properties[key] if key in self.properties else ''

#	def getResolution(self):
#		"""Returns the resolution of the screen. The returned value is one of the following:"""
#		return 5 # NTSC 16:9 (720x480)

#	def getWidth(self):
#		"""Returns the width of this screen."""
#		return 720

#	def onAction(self, action):
#		"""onAction method."""
#		pass

#	def onClick(self, control):
#		"""onClick method."""
#		pass

#	def onFocus(self, control):
#		"""onFocus method."""
#		pass

#	def onInit(self):
#		"""onInit method."""
#		pass

#	def removeControl(self, control):
#		"""Removes the control from this window."""
#		pass

#	def removeControls(self, controlList):
#		"""Removes a list of controls from this window."""
#		pass

#	def setCoordinateResolution(self, resolution):
#		"""Sets the resolution"""
#		pass

#	def setFocus(self, control):
#		"""Give the supplied control focus."""
#		pass

#	def setFocusId(self):
#		"""Gives the control with the supplied focus."""
#		pass

#	def setProperty(self, key, value):
#		"""Sets a window property, similar to an infolabel."""
#		self.properties[key] = value;

#	def show(self):
#		"""Show this window."""
#		pass

#class WindowDialog(Window):

#	def __init__(self):
#		Window.__init__(self, 0)
#		pass

#class WindowXML(Window):

#	def __init__(self, xmlFilename, scriptPath=None, defaultSkin=None, forceFallback=False):
#		Window.__init__(self, 0)

#	def addItem(item, position=None):
#		"""addItem(item[, position]) -- Add a new item to this Window List."""
#		pass

#	def clearList():
#		"""clearList() -- Clear the Window List."""
#		pass

#	def getCurrentListPosition():
#		"""getCurrentListPosition() -- Gets the current position in the Window List."""
#		return 0

#	def getListItem(position):
#		"""getListItem(position) -- Returns a given ListItem in this Window List."""
#		return None

#	def getListSize():
#		"""getListSize() -- Returns the number of items in this Window List."""
#		return 0

#	def removeItem(position):
#		"""removeItem(position) -- Removes a specified item based on position, from the Window List."""
#		pass

#	def setCurrentListPosition(position):
#		"""setCurrentListPosition(position) -- Set the current position in the Window List."""
#		return 0

## xbmc/interfaces/python/xbmcmodule/winxmldialog.cpp
#class WindowXMLDialog(WindowXML):

#	def __init__(self, xmlFilename, scriptPath=None, defaultSkin=None, defaultRes=None):
#		"""Create a new WindowXMLDialog script."""
#		WindowXML.__init__(self, xmlFilename, scriptPath, defaultSkin)

