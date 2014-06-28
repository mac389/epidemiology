from __future__ import unicode_literals

from nltk.corpus import stopwords
from optparse import OptionParser
from progress.bar import Bar

import json, os

import words_to_nums as wordnumber

READ = 'rU'
WRITE = 'wb'
USER = 0
TEXT = 1

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
	return (tweet_object['in_reply_to_user_id'],tweet_object['text'])	

#COULD ALSO FISH OUT RECIPIENT FROM METADATA

tweets = []
bar = Bar('Extracting text from tweets',max=len(filenames))
for filename in filenames[:2]:
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
	print>>f,'Recipient \t Text'
	for tweet in list(set(tweets)):
		if tweet[TEXT] and tweet[TEXT].encode('ascii','ignore') and '@' in tweet[TEXT]:
				numeric = [word for word in tweet[TEXT].split() 
								if any([letter.isdigit() for letter in word]) 
								and not any([verboten in word for verboten in ['@','http']])]
				numeric = [filter(lambda char: char.isdigit(),x) for x in numeric]				
				nonnumeric = [word for word in list(set(tweet[TEXT].split()) - set(numeric))
								if not any([verboten in word for verboten in ['@','http']])]
				if numeric != [] or nonnumeric != []:
					print>>f,' \t '.join((str(tweet[USER]) if tweet[USER] else ' ',tweet[TEXT].encode('ascii','ignore')))
		bar.next()
bar.finish()
