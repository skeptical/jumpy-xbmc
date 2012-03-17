import os, shutil
from xbmc import translatePath

def copy(source, destination):
	"""Copy file to destination, returns true/false."""
	try:
		shutil.copyfile(translatePath(source), translatePath(destination))
		return True
	except:
		return False

def delete(file):
	"""Delete file"""
	os.remove(translatePath(file))
#	shutil.rmtree(file)

def rename(file, newFileName):
	"""Rename file, returns true/false."""
	try:
		os.rename(translatePath(file), translatePath(newFileName))
#		shutil.move(file, newFileName)
		return True
	except:
		return False

def exists(path):
	"""Check if file exists, returns true/false."""
	return os.path.exists(translatePath(path))

def mkdir(path):
	"""Create a folder."""
	os.mkdirs(translatePath(path))

def rmdir(path):
	"""Remove a folder."""
	shutil.rmtree(translatePath(path))

