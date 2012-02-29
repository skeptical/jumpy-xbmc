import os, shutil

def copy(source, destination):
	"""Copy file to destination, returns true/false."""
	try:
		shutil.copyfile(source, destination)
		return True
	except:
		return False

def delete(file):
	"""Delete file"""
	os.remove(file)
#	shutil.rmtree(file)

def rename(file, newFileName):
	"""Rename file, returns true/false."""
	try:
		os.rename(file, newFileName)
#		shutil.move(file, newFileName)
		return True
	except:
		return False

def exists(path):
	"""Check if file exists, returns true/false."""
	return os.path.exists(path)

def mkdir(path):
	"""Create a folder."""
	os.mkdirs(path)

def rmdir(path):
	"""Remove a folder."""
	shutil.rmtree(path)

