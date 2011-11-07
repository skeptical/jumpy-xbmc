import sys, os, imp

import jumpy
import xbmc.xbmcinit

if len(sys.argv) == 1:
	
	print 'jumpy-xbmc version %s\n' % xbmc.xbmcinit.version
	
	home = os.path.join(os.path.split(sys.argv[0])[0], 'xbmc')
	addonsdir = os.path.join(_special['home'], 'addons')
	
	if not os.path.isdir(addonsdir):
		print "Error: can't find xbmc addons dir at '%s'." % addonsdir
		sys.exit(-1)
	
	for dir in os.listdir(addonsdir):
		dir = os.path.join(addonsdir, dir)
		try:
			id, name, script, thumb, path = xbmc.xbmcinit.read_addon(dir)
			pms.setPath(None)
			pms.setPath(home)
			if path != "":
				pms.setPath(path)
			pms.addItem(PMS_FOLDER, "[xbmc]   %s" % name, [script, 'plugin://' + id + '/'], thumb)
			print 'found %s addon.' % name
		except:
			pass

