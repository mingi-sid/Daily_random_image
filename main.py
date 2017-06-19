#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob, os, sys
import time
import hashlib

IMAGES_DIR = u"/mnt/d/Personal/KAIST/PASSION/170619_daily_random_image/Daily_random_image"#u"/home/hamster/열변"
TARGET_EXT = [u'jpg', u'bmp', u'png']
IMAGE_LIST = u"imglist.txt"
HELP_MESSAGE = """  -h	Print this help message
  -f	Print image file list
  -H	Print hash and timestamp of files
  -i	Initial run."""
TIMESTAMP = int(time.time())

def images_list(root, extensions):
	images = []
	for rootpath, dirnames, filenames in os.walk(root):
		for filename in filenames:
			if filename.split('.')[-1] in extensions:
				images += [os.path.join(rootpath, filename)]
#		for directory in dirnames:
#			images += images_list(directory, extensions)
	return images

def main():
#	if argument is empty or -h, print help message
	if (len(sys.argv) is 1) or ('-h' in sys.argv):
		print HELP_MESSAGE
		return


	file_list = []
	file_list = images_list(IMAGES_DIR, TARGET_EXT)
#	if argument contains -f, print target images
	if '-f' in sys.argv:
		for filepath in file_list:
			print filepath
	
	file_data = {}
	for filepath in file_list:
		sha256 = hashlib.sha256()
		f = open(filepath, 'rb')
		for block in iter(lambda: f.read(65536), b''):
			sha256.update(block)
		file_data[sha256.hexdigest()] = [filepath, TIMESTAMP]
	if ('-v' in sys.argv) or ('-H' in sys.argv):
		for filehash in file_data.keys():
			print filehash + '\t' + str(file_data[filehash])
		if '-H' in sys.argv:
			return

		

main()
