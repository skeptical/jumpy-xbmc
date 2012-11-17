import sys, os, jumpy

if len(sys.argv) == 1:

	import traceback #, imp
	import sqlite3 #, itertools
	from cStringIO import StringIO
	from ConfigParser import ConfigParser

	xbmc_home = pms.getProperty('xbmc.path')
	if xbmc_home != "" and xbmc_home is not None:
		pms.setEnv('xbmc_home', xbmc_home)
		os.environ['xbmc_home'] = xbmc_home
	xbmc_main = pms.getProperty('xbmc.main.path')
	if xbmc_main != "" and xbmc_main is not None:
		pms.setEnv('xbmc_main', xbmc_main)
		os.environ['xbmc_main'] = xbmc_main

	import xbmc.xbmcinit
	print '\njumpy-xbmc version %s\n' % xbmc.xbmcinit.version
	print 'special://xbmc=%s' % _special['xbmc']
	print 'special://home=%s' % _special['home']

	home = os.path.join(os.path.abspath(os.path.split(sys.argv[0])[0]), 'xbmc')
	print "home=%s\n" % home
	addonsdb = os.path.join(_special['home'], 'userdata', 'Database', 'Addons15.db')
	addonsdir = os.path.join(_special['home'], 'addons')

	disabled = []
	if os.path.isfile(addonsdb):
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
			id = xbmc.xbmcinit.read_addon(dir=dir, full=False)
			if id in disabled:
				continue
#			print 'found %s addon.' % name
			info = _info[id]
			pms.addPath(None)
			pms.addPath(home)
			pms.addPath(info['_pythonpath'])
			script = os.path.join(info['path'], info['_script'])
			thumb = os.path.join(info['path'], info['icon'])
			pms.addItem(PMS_FOLDER, "[xbmc]   %s" % info['name'], [sys.argv[0], script, 'plugin://' + id + '/'], thumb)
		except KeyError:
			pass
		except:
			traceback.print_exc(file=sys.stdout)

else:
	# the only purpose here is to ensure os,sys,jumpy,xbmcinit
	# are loaded at addon startup
	del sys.argv[0]
	addondir = os.path.dirname(sys.argv[0])
	os.chdir(addondir)
	sys.path[0] = addondir
	import xbmcinit
	execfile(sys.argv[0])

