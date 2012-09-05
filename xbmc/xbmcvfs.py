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
	os.mkdir(translatePath(path))

def mkdirs(path):
	"""mkdirs(path) -- Create folder(s) - it will create all folders in the path."""
	os.makedirs(translatePath(path))

def rmdir(path):
	"""Remove a folder."""
	shutil.rmtree(translatePath(path))

def listdir(path):
	"""listdir(path) -- lists content of a folder."""
	return os.listdir(translatePath(path))

class File:

	def __init__(path, mode='r'):
		self.path = translatePath(path);
		self.file = open(self.path, mode)
		return self.file

	def read(n=-1):
		return self.file.read(n)

	def write(b):
		return self.file.write(b)

	def size():
		return os.path.getsize(self.path)

	def seek(offset, whence=0):
		return self.file.seek(offset, whence)

	def close():
		self.file.close()

