#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import tweepy
import os
from ConfigParser import ConfigParser

parser = ConfigParser()
ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), \
'twitter.ini')
parser.read(ini_path)

def post_on_twitter(img_path, content):
	CONSUMER_KEY = parser.get('twitter', 'consumer_key')
	CONSUMER_SECRET = parser.get('twitter', 'consumer_secret')
	ACCESS_TOKEN = parser.get('twitter', 'access_token')
	ACCESS_TOKEN_SECRET = parser.get('twitter', 'access_token_secret')

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	
	api = tweepy.API(auth)

	api.update_with_media(filename = img_path, \
			status = content, source = 'Daily_random_image')

def main():
	CONSUMER_KEY = parser.get('twitter', 'consumer_key')
	CONSUMER_SECRET = parser.get('twitter', 'consumer_secret')

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

	try:
		redirect_url = auth.get_authorization_url()
	except tweepy.TweepError:
		print 'Error! Failed to get request token.'
		return

	print 'Get to this url :', redirect_url

	verifier = raw_input('Verifier :')

	try:
		auth.get_access_token(verifier)
	except tweepy.TweepError:
		print 'Error! Failed to get access token.'
	
	parser.set('twitter', 'access_token', auth.access_token)
	parser.set('twitter', 'access_token_secret', auth.access_token_secret)
	with open('twitter.ini', 'wb') as f:
		parser.write(f)

if __name__ == '__main__':
	main()

