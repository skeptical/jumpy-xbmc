import os, os.path, sys
import xbmcinit

# xbmc/interfaces/python/xbmcmodule/pyutil.h
__author__ = "J. Mulder <darkie@xbmc.org>" # PY_XBMC_AUTHOR
__date__ = "1 May 2010"
__version__ = "1.0"
__credits__ = "XBMC TEAM." # PY_XBMC_CREDITS
__platform__ = "XBOX" # PY_XBMC_PLATFORM

# xbmc/interfaces/python/xbmcmodule/PythonAddon.cpp
# (with a little help from xbmcswift)
class Addon:
	
	def __init__(self, id):
		self._id = id
		self.info = {}
		self.info['path'] = os.path.join(_special['home'], 'addons', self._id)
		self.info['profile'] = os.path.join(_special['profile'], 'addon_data', self._id)
		# TODO read addon.xml

	def getLocalizedString(self, id):
		"""Returns an addon's localized 'unicode string'."""
		key = str(id)
		assert key in _addonstrings, 'ID not found in English/strings.xml.'
		return _addonstrings[key]

	def getSetting(self, id):
		"""Returns the value of a setting as a unicode string."""
		try:
			return _settings[id]
		except KeyError:
			return ''

	def setSetting(self, id, value):
		"""Sets a script setting."""
		pass

	# sometimes called with an arg, e.g veehd
	def openSettings(self, arg=None):
		"""Opens this scripts _settings dialog."""
		print "*** openSettings ***"
		pass

	def getAddonInfo(self, id):
		"""Returns the value of an addon property as a string."""
		properties = ['author', 'changelog', 'description', 'disclaimer',
			'fanart', 'icon', 'id', 'name', 'path', 'profile', 'stars', 'summary',
			'type', 'version']
		assert id in properties, '%s is not a valid property.' % id
		return self.info[id] if id in self.info else ''


