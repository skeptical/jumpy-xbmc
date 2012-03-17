import sys, os #, imp
import sqlite3 #, itertools
from cStringIO import StringIO
from ConfigParser import ConfigParser

import jumpy

if len(sys.argv) == 1:
	
	conffile = os.path.join(pms.getProfileDir(),'jumpy-xbmc.conf')
	if not os.path.isfile(conffile):
		conffile = os.path.join(pms.getProfileDir(),'xbmc.conf') # (backwards compatibility)
	if os.path.isfile(conffile):
		conf = ConfigParser()
		conf.readfp(StringIO("[xbmc]\n" + open(conffile).read()))
		if conf.has_option('xbmc','xbmc_home'):
			xbmc_home = conf.get('xbmc','xbmc_home')
			pms.setEnv('xbmc_home', xbmc_home)
			os.environ['xbmc_home'] = xbmc_home
	
	import xbmc.xbmcinit
	print '\njumpy-xbmc version %s\n' % xbmc.xbmcinit.version
	
	home = os.path.join(os.path.split(sys.argv[0])[0], 'xbmc')
	addonsdb = os.path.join(_special['home'], 'userdata', 'Database', 'Addons.db')
	addonsdir = os.path.join(_special['home'], 'addons')
	
	disabled = []
	try:
		conn = sqlite3.connect(addonsdb)
		cursor = conn.cursor()
		cursor.execute('SELECT addonID FROM disabled')
		for row in cursor:
			disabled.append(row[0])
#			print "disabled: %s" % row[0]
		conn.close()
	except sqlite3.Error, e:
		print "%s: %s" % (addonsdb, e.args[0])

	if not os.path.isdir(addonsdir):
		print "Error: can't find xbmc addons dir at '%s'." % addonsdir
		sys.exit(-1)
	else:
		print "found xbmc addons dir at '%s'.\n" % addonsdir
	
	for dir in os.listdir(addonsdir):
		dir = os.path.join(addonsdir, dir)
		try:
			id, name, script, thumb, path = xbmc.xbmcinit.read_addon(dir)
			if id in disabled:
				continue
#			print 'found %s addon.' % name
			pms.setPath(None)
			pms.setPath(home)
			if path != "":
				pms.setPath(path)
			pms.addItem(PMS_FOLDER, "[xbmc]   %s" % name, [script, 'plugin://' + id + '/'], thumb)
		except:
			pass

