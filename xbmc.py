import sys, os, jumpy

if len(sys.argv) == 1:

	import traceback, re
	import sqlite3
	from cStringIO import StringIO
	from ConfigParser import ConfigParser

	# set up

	import xbmc.xbmcinit as xbmcinit
	pms.setEnv('xbmc_main', _special['xbmc'])
	pms.setEnv('xbmc_home', _special['home'])

	print '\njumpy-xbmc version %s\n' % xbmcinit.version
	print 'special://xbmc=%s' % _special['xbmc']
	print 'special://home=%s' % _special['home']

	home = os.path.join(os.path.abspath(os.path.split(sys.argv[0])[0]), 'xbmc')
	print "home=%s\n" % home
	addonsdb = os.path.join(_special['home'], 'userdata', 'Database', 'Addons15.db')
	addonsdir = os.path.join(_special['home'], 'addons')

	# read the xbmc Addons db

	disabled = []
	services = []

	if os.path.isfile(addonsdb):
		try:
			conn = sqlite3.connect(addonsdb)
			cursor = conn.cursor()
			cursor.execute('SELECT addonID FROM disabled')
			for row in cursor:
				disabled.append(row[0])
#				print "disabled: %s" % row[0]
			cursor.execute('SELECT addonID FROM addon WHERE type = "xbmc.service"')
			for row in cursor:
				if not row[0] in disabled:
					services.append(row[0])
#					print "service: %s" % row[0]
			conn.close()
		except sqlite3.Error, e:
			print "%s: %s" % (addonsdb, e.args[0])

	if not os.path.isdir(addonsdir):
		print "Error: can't find xbmc addons dir at '%s'." % addonsdir
		sys.exit(-1)
	else:
		print "found xbmc addons dir at '%s'.\n" % addonsdir

	# scan the xbmc addons dir

	addons = []
	ignore = re.compile(r'(xbmc|repository|skin|visualization)\.')

	for dir in sorted(os.listdir(addonsdir), reverse=True):
		id = xbmcinit.read_addon(dir=os.path.join(addonsdir, dir), full=False)
		if not id : continue;
		if id in disabled or ignore.match(id):
			del _info[id]
			continue
		try:
			if '_script' in _info[id]:
				addons.append(id)
		except KeyError: pass
		except:
			traceback.print_exc(file=sys.stdout)

	# add active addons in alphabetic order

	for id in sorted(addons, \
			cmp=lambda a,b:cmp(_info[a]['name'].lower(), _info[b]['name'].lower())):
		try:
			info = _info[id]
			pms.addPath(None)
			pms.addPath(home)
			pms.addPath(os.path.pathsep.join(info['_pythonpath']))
			script = os.path.join(info['path'], info['_script'])
			thumb = os.path.join(info['path'], info['icon'])
			pms.addItem(PMS_FOLDER, "[xbmc]   %s" % pms.esc(info['name']), \
				[sys.argv[0], script, 'plugin://' + id + '/'], thumb)
		except KeyError: pass
		except:
			traceback.print_exc(file=sys.stdout)

	# set up reference vars

	paths, jdata = _info.digest()
	pms.setVar('xbmc_paths', paths)
	pms.setVar('xbmc_info', jdata)

	# start services

	for id in services:
		if id in _info:
			info = _info[id]
			for ext in info['extension']:
				if ext['point'] == 'xbmc.service' and 'start' in ext and ext['start'] == 'startup':
					print "\nstarting service: %s" % id
					pms.addPath(None)
					pms.addPath(home)
					pms.addPath(os.path.pathsep.join(info['_pythonpath']))
					pms.run([os.path.join(info['path'], ext['library']), '&'], id)
#					pms.run('xterm -e "python %s; bash"' % os.path.join(info['path'], ext['library']))
					break

else:
	# the only purpose here is to ensure os,sys,jumpy,xbmcinit
	# are loaded at addon startup
	del sys.argv[0]
	addondir = os.path.dirname(sys.argv[0])
	os.chdir(addondir)
	sys.path[0] = addondir
	__file__ = sys.argv[0]
	import xbmcinit
	execfile(__file__)

