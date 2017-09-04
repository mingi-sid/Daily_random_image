#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import glob, os, sys
import time
import hashlib
import random
import shutil
from ConfigParser import SafeConfigParser
import codecs
from PIL import Image

import twitter

parser = SafeConfigParser()

setting_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),\
'setting.ini')
with codecs.open(setting_path, 'r', encoding='utf-8') as f:
	parser.readfp(f)

IMAGES_DIR = parser.get('filesystem', 'image_dir')
TARGET_DIR = parser.get('filesystem', 'target_dir')
TARGET_FILE = parser.get('filesystem', 'target_file')

TWEET_CONTENT = parser.get('tweet', 'tweet_content')

TARGET_EXT = [u'jpg', u'bmp', u'png']
IMAGE_LIST = os.path.join(os.path.dirname(os.path.abspath(__file__)),\
"imglist.txt")
HELP_MESSAGE = """  -h	Print this help message
  -f	Print hash and timestamp of image files
  -r	Read text file and print result
  -n	Print merged list of images
  -N	Print merged imglist.txt, not actually modifying it
  -v	Verbose run
  -i	Initial run.
  --no-twitter	Does not access twitter account"""
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

def time_based_sort(data):
	"""Return dictionary having time as key of image file data"""
	result = {}
	for key in data.keys():
		if result.has_key(data[key][1]):
			result[data[key][1]].append( (key, data[key][0]) )
		else:
			result[data[key][1]] = [(key, data[key][0])]
	return result

def write_list(data):
	f = open(IMAGE_LIST, 'w')
	sorted_keys = sorted(data.keys(), key = int, reverse = True)
	for timestamp in sorted_keys:
		f.write((unicode(timestamp) + '\n').encode('utf-8'))
		for hash_path in data[timestamp]:
			f.write(u'\t'.join((hash_path[0], hash_path[1] + '\n')).encode('utf-8'))
	f.close()

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
	if not '-i' in sys.argv:
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

	new_sorted = []
	new_sorted = time_based_sort(new_data)
	sorted_keys = sorted(new_sorted.keys(), key = int, reverse = True)

	if ('-v' in sys.argv) or ('-N' in sys.argv):
		if '-v' in sys.argv:
			print '\nIntermediate file contents:'
		for newtime in sorted_keys:
			print newtime
			for newtuple in new_sorted[newtime]:
				print newtuple[0] + '\t' + newtuple[1]
		if '-N' in sys.argv:
			return

	#Choose one image, randomly
	target_img_name = ''
	random.seed(TIMESTAMP)
	if len(sorted_keys) == 1:
		target_img = random.choice(new_sorted[sorted_keys[0]])
		target_img_name = target_img[1]
		new_sorted[sorted_keys[0]].remove(target_img)
		new_sorted[str(int(sorted_keys[0])-1)] = [target_img, ]
		if len(new_sorted[sorted_keys[0]]) == 0:
			del new_sorted[sorted_keys[0]]
	elif len(sorted_keys) == 0:
		pass
	else:
		if len(new_sorted[sorted_keys[-2]]) == 1:
			target_img = new_sorted[sorted_keys[-2]][0]
			target_img_name = target_img[1]
			del new_sorted[sorted_keys[-2]]
		else:
			target_img = random.choice(new_sorted[sorted_keys[-2]])
			target_img_name = target_img[1]
			new_sorted[sorted_keys[-2]].remove(target_img)
			new_sorted[sorted_keys[-1]].append(target_img)
	sorted_keys = []		#To prevent referring legacy data
	if '-v' in sys.argv:
		print 'result'
		print target_img_name

	#Resize and copy the chosen image to target dir.
	new_img_name = ''

	img = Image.open(target_img_name)
	basewidth = 1000
	ratio = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(ratio)))
	img_new = img.resize((basewidth, hsize), Image.ANTIALIAS)
	
	if not target_img_name == '':
		if os.path.isfile(TARGET_DIR + '/'+TARGET_FILE+'.png'):
			try:
				os.remove(TARGET_DIR+'/'+TARGET_FILE+'.png')
			except OSError as e:
				print e
		if os.path.isfile(TARGET_DIR + '/'+TARGET_FILE+'.jpg'):
			try:
				os.remove(TARGET_DIR+'/'+TARGET_FILE+'.jpg')
			except OSError as e:
				print e
		if target_img_name[-4:] == '.png':
			new_img_name = TARGET_DIR + '/'+TARGET_FILE+'.png'
			img_new.save(new_img_name)
		else:
			new_img_name = TARGET_DIR + '/'+TARGET_FILE+'.jpg'
			img_new.save(new_img_name)

	#Update the imglist.txt file
	write_list(new_sorted)

	#Post on twitter
	if '--no-twitter' in sys.argv:
		return

	if '-i' in sys.argv:
		twitter.main()

	twitter.post_on_twitter(new_img_name, TWEET_CONTENT)
	return
#End of main()
main()
