import tweepy
import numpy as np

from textwrap import TextWrapper
from string import replace

MAX_COUNT = 200
WRITE ='wb'
READ = 'rb'

passwords = json.load(open('passwords',READ))
auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#user_names = open('../data/usernames',READ).read().splitlines()
NAME = "Person whose age we surmised"
user_names = ['@'+record[NAME] for record in json.load(open('tweets_with_ages.json',READ))]
for user_name in user_names:
	tweets = api.user_timeline(screen_name = user_name, include_rts=False,count=MAX_COUNT)
	filename = '%stweets'%(replace(user_name,'@',''))

	#Will get most recent 200 tweets, which samples unevenly in time
	with open(filename,WRITE) as f:
		for tweet in tweets:
			print>>f, tweet.text.encode('ascii','ignore')
