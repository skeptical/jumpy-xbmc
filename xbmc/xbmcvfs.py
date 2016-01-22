import os, shutil
from stat import *
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
	try:
		os.mkdir(translatePath(path))
	except:
		pass

def mkdirs(path):
	"""mkdirs(path) -- Create folder(s) - it will create all folders in the path."""
	try:
		os.makedirs(translatePath(path))
	except:
		pass

def rmdir(path):
	"""Remove a folder."""
	shutil.rmtree(translatePath(path))

def listdir(path):
	"""listdir(path) -- lists content of a folder."""
	return os.listdir(translatePath(path))

class File(object):

	def __init__(self, path, mode='r'):
		self.path = translatePath(path);
		self.file = open(self.path, mode)

	def read(self, n=-1):
		return self.file.read(n)

	def readBytes(numbytes):
		return self.read(numbytes)

	def write(self, b):
		return self.file.write(b)

	def size(self):
		return os.path.getsize(self.path)

	def seek(self, offset, whence=0):
		return self.file.seek(offset, whence)

	def close(self):
		self.file.close()

class Stat(object):
	def __init__(path):
		"""Get file or file system status."""
		self.stat = os.stat(path)

	def st_atime():
		return self.stat[ST_ATIME]

	def st_ctime():
		return self.stat[ST_CTIME]

	def st_dev():
		return self.stat[ST_DEV]

	def st_gid():
		return self.stat[ST_GID]

	def st_ino():
		return self.stat[ST_INO]

	def st_mode():
		return self.stat[ST_MODE]

	def st_mtime():
		return self.stat[ST_MTIME]

	def st_nlink():
		return self.stat[ST_NLINK]

	def st_size():
		return self.stat[ST_SIZE]

	def st_uid():
		return self.stat[ST_UID]

