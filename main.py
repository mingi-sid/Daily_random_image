#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob, os, sys

IMAGES_DIR = u"/home/hamster/열변"
TARGET_EXT = [u'jpg', u'bmp', u'png']
HELP_MESSAGE = """  -h	Print this help message
  -f	Print image file list
"""

if (len(sys.argv) is 1) or ('-h' in sys.argv):
	print HELP_MESSAGE

file_list = []
file_list = images_list(IMAGES_DIR, TARGET_EXT)

if '-f' in sys.argv:
	for filepath in file_list:
		print filepath
	return

def images_list(root, extensions):
	images = []
	for rootpath, dirnames, filenames in os.walk(root):
		for filename in filenames:
			images += [os.path.join(rootpath, filename)]
		for directory in dirnames:
			images += images_list(directory, extensions)
	return images
