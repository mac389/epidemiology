from __future__ import unicode_literals

from nltk.corpus import stopwords
from optparse import OptionParser
from progress.bar import Bar
from textwrap import TextWrapper
from string import replace

import json, os, tweepy

import words_to_nums as wordnumber

READ = 'rU'
WRITE = 'wb'
USER = 0
TEXT = 1

consumer_key = '0gU0QlrtKLlcidfyfVdH7R1qz'
consumer_secret = '2GQ8jCjP58xu7gENWwmCTy4vVLRFsvzM2VJL1u7fHcumMqP4qA'
access_token = '2585785981-kfCNAtFtgESI8sT3jw0AhH7qQ6UCdgk4HsWp2If'
access_token_secret = 'PdATAHsTcnjX9gCgoCVMFcMuffTf3648JHHWC8vhSRQ7z'

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

wordnumber_parser = wordnumber.WordsToNumbers()

#--Command  line parsing
op = OptionParser()
op.add_option('--i', dest='source', type='str', 
	help='File or directory of files to convert. If no argument is passed, uses current directory.')
op.add_option('--k',dest='filter',type='str',
	help='Keywords that filenames must include')
op.add_option('--o',dest='output',type='str',
	help='Name of file to write text of tweets to.')
op.print_help()


opts,args = op.parse_args()
if len(args) > 0:
	op.error('This script only takes arguments preceded by command line options.')
	sys.exit(1)


filenames = [filename for filename in os.listdir(opts.source if opts.source else os.getcwd())
				if filename.endswith('.json')]

if opts.filter:
	inclusions = opts.filter.split()
	filenames = filter(lambda text: any([inclusion in text for inclusion in inclusions]),filenames)

def extract_text(tweet_object):
	return (tweet_object['user']['screen_name'],' '.join(tweet_object['text'].split()))	

#COULD ALSO FISH OUT RECIPIENT FROM METADATA

tweets = []
bar = Bar('Extracting text from tweets',max=len(filenames))
for filename in filenames:
	try:
		tweets.extend([extract_text(tweet_object) 
				for tweet_object in json.load(open(os.path.join(opts.source,filename),READ))])
	except ValueError:
		print 'Could not open %s'%filename
	bar.next()
bar.finish()

writename = os.path.join(opts.source,opts.output if opts.output else 'jtt')
bar = Bar('Writing text of tweets to %s'%writename,max=len(tweets))
with open(writename,WRITE) as f:
	print>>f,'From \t Text \t '
	for tweet in list(set(tweets)):
		if tweet[TEXT] and tweet[TEXT].encode('ascii','ignore') and '@' in tweet[TEXT]:
				numeric = [word for word in tweet[TEXT].split() 
								if any([letter.isdigit() for letter in word]) 
								and not any([verboten in word for verboten in ['@','http']])]
				numeric = [filter(lambda char: char.isdigit(),x) for x in numeric]				
				nonnumeric = filter(None,map(wordnumber_parser.parse,([word for word in list(set(tweet[TEXT].split()) - set(numeric))
								if not any([verboten in word for verboten in ['@','http']])])))
				if numeric != [] or nonnumeric != []:
					print>>f,' \t '.join((str(tweet[USER]) if tweet[USER] else ' ',tweet[TEXT].encode('ascii','ignore')))
		bar.next()
bar.finish()
