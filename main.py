#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob, os, sys
import time
import hashlib

IMAGES_DIR = u"/mnt/d/Personal/KAIST/PASSION/170619_daily_random_image/Daily_random_image"#u"/home/hamster/열변"
TARGET_EXT = [u'jpg', u'bmp', u'png']
IMAGE_LIST = u"imglist.txt"
HELP_MESSAGE = """  -h	Print this help message
  -f	Print hash and timestamp of image files
  -r	Read text file and print result
  -n	Print merged imglist.txt, not actually modifying it
  -v	Verbose run
  -i	Initial run."""
TIMESTAMP = int(time.time())

def images_list(root, extensions):
	"""Return list of file path of the images."""
	images = []
	for rootpath, dirnames, filenames in os.walk(root):
		for filename in filenames:
			if filename.split('.')[-1] in extensions:
				images += [os.path.join(rootpath, filename)]
	return images

def read_list():
	"""Read text and retrun dict of hash to path and timestamp"""
	f = open(IMAGE_LIST, 'r')
	data = {}
	timestamp = '0'
	for line in f:
		if '\t' in line:
			filehash = line.split('\t')[0]
			path = (line.split('\t')[1]).strip()
			data[filehash] = ((path), timestamp)
		else:
			timestamp = (line[:]).strip()
	f.close()
	return data

def main():
	"""main function. Called after run."""
#	if argument is empty or -h, print help message
	if (len(sys.argv) is 1) or ('-h' in sys.argv):
		print HELP_MESSAGE
		return

#	if argument contains -r, print the list of contents in text file.
	if '-r' in sys.argv:
	 	prev_data = read_list()
		for prevhash in prev_data.keys():
			print prevhash
			print '\t.' + prev_data[prevhash][0][len(IMAGES_DIR):]+\
					'\t' + str(prev_data[prevhash][1])
		return

	prev_data = {}
	prev_data = read_list()

	if '-v' in sys.argv:
		print '\nPrevious file list:'
		for prevhash in prev_data.keys():
			print prevhash
			print '\t.' + prev_data[prevhash][0][len(IMAGES_DIR):] +\
					'\t' + str(prev_data[prevhash][1])



	file_list = []
	file_list = images_list(IMAGES_DIR, TARGET_EXT)
	
	file_data = {}
	for filepath in file_list:
		sha256 = hashlib.sha256()
		f = open(filepath, 'rb')
		for block in iter(lambda: f.read(65536), b''):
			sha256.update(block)
		f.close()
		file_data[sha256.hexdigest()] = (filepath, TIMESTAMP)
#	if argument contains -f, print the list of current files.
	if ('-v' in sys.argv) or ('-f' in sys.argv):
		if '-v' in sys.argv:
			print '\nCurrent file list:'
		for filehash in file_data.keys():
			print filehash
			print '\t.' + file_data[filehash][0][len(IMAGES_DIR):] +\
					'\t' + str(file_data[filehash][1])
		if '-f' in sys.argv:
			return

#	prev_data : Data from previous run or empty data
#	file_data : Data from the current file system
#	new_data  : Data that will be saved after the run

	"""
Possible cases
In prev_data & In file_data
	if path are same
		prevhash : (prevpath, prevtime)
	if not same
		*Maybe file is moved. Doesn't affect program.
		prevhash : (prevpath, prevtime)
In prev_data & Not in file_data
	*File is erased or modified. Add its path to search it later.
	append to missing_prevhash
Not in prev_data & In file_data
	*New file is found. Add it to new_data.
	filehash : (filepath, filetime)
In file_data & file path is matched
	filehash : (filepath, prevtime)
"""
	new_data = {}
	missing_prevhash = {}
	for prevhash in prev_data.keys():
		if file_data.has_key(prevhash):
			new_data[prevhash] = (file_data[prevhash][0], prev_data[prevhash][1])
			del file_data[prevhash]
		else:
			missing_prevhash[prev_data[prevhash][0]] = prev_data[prevhash][1]
	for filehash in file_data.keys():
		filepath = file_data[filehash][0]
		if missing_prevhash.has_key(filepath):
			new_data[filehash] = (filepath, missing_prevhash[filepath])
		else:
			new_data[filehash] = (filepath, file_data[filehash][1])
	
	if ('-v' in sys.argv) or ('-n' in sys.argv):
		print '\nUpdated file list:'
		for newhash in new_data.keys():
			print newhash
			print '\t.' + new_data[newhash][0][len(IMAGES_DIR):] +\
					'\t' + str(new_data[newhash][1])
		if '-n' in sys.argv:
			return

	#TODO : Modifying new_data to saving form
	#TODO : Adding choicing feature
	#TODO : Upload on Twitter
#End of main()
main()
