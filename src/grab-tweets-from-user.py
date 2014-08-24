import tweepy
import numpy as np

from textwrap import TextWrapper
from string import replace

consumer_key = '0gU0QlrtKLlcidfyfVdH7R1qz'
consumer_secret = '2GQ8jCjP58xu7gENWwmCTy4vVLRFsvzM2VJL1u7fHcumMqP4qA'
access_token = '2585785981-kfCNAtFtgESI8sT3jw0AhH7qQ6UCdgk4HsWp2If'
access_token_secret = 'PdATAHsTcnjX9gCgoCVMFcMuffTf3648JHHWC8vhSRQ7z'

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

MAX_COUNT = 200
WRITE ='wb'
READ = 'rb'

user_names = open('../data/usernames',READ).read().splitlines()

for user_name in user_names:
	tweets = api.user_timeline(screen_name = user_name, include_rts=False,count=MAX_COUNT)
	filename = '%s-tweets'%(replace(user_name,'@',''))

	#Will get most recent 200 tweets, which samples unevenly in time
	with open(filename,WRITE) as f:
		for tweet in tweets:
			print>>f, tweet.text.encode('ascii','ignore')