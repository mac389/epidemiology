import tweepy,json, os
import numpy as np

from textwrap import TextWrapper
from string import replace

MAX_COUNT = 200
WRITE ='wb'
READ = 'rb'
APPEND = 'a'
passwords = json.load(open('passwords.json',READ))
auth = tweepy.auth.OAuthHandler(passwords['consumer_key'], passwords['consumer_secret'])
auth.set_access_token(passwords['access_token'], passwords['access_token_secret'])

api = tweepy.API(auth)

#user_names = open('../data/usernames',READ).read().splitlines()
NAME = "Person whose age we surmised"
user_names = set(['@'+record[NAME] for record in json.load(open('../data/tweets_with_ages.json',READ))])
deleted_users = []
for user_name in user_names:
	try:
		tweets = api.user_timeline(screen_name = user_name, include_rts=False,count=MAX_COUNT)
		filename = '../data/%s/tweets'%(replace(user_name,'@',''))
		if not os.path.exists(filename):
			os.makedirs('../data/%s/'%(replace(user_name,'@','')))
		#Will get most recent 200 tweets, which samples unevenly in time
		with open(filename,APPEND) as f:
			for tweet in tweets:
				print>>f, tweet.text.encode('ascii','ignore')
	except tweepy.error.TweepError:
		print 'User %s does not exist anymore'%user_name
		deleted_users.append(user_name)

with open('../data/deleted_users','a') as f:
	for deleted_user in deleted_users:
		try:
			print>>f,deleted_user.encode('ascii','replace')
		except:
			pass
print '%.02f of the users still existed'%(1-len(deleted_users)/float(len(user_names)))