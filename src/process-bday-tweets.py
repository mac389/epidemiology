import nltk,os,json, re

import twokenize as Tokenizer
import matplotlib.pyplot as plt

from pprint import pprint
from matplotlib import rcParams

rcParams['text.usetex'] = True
base = '/Volumes/My Book'
READ = 'rU'
filenames  = [filename for filename in os.listdir(base) if 'birthday' in filename]

def extract_text(tweet_object):
	return tweet_object['text']	

def find_recipient(tokenized_tweet):
	if any(['@' in token for token in tokenized_tweet]):
		#--Name explicitly mentioned:
		recipients = filter(lambda token: '@' in token,tokenized_tweet)
	else:
		recipients = [] #- Once are pulling actual tweets, insert code here to look in metadata
	return recipients

def find_age(tokenized_tweet):
	ages = [int(token) for token in tokenized_tweet if token.isdigit()]
	return ages

def find_age_recipient(text_tweet):
	tokenized = Tokenizer.tokenizeRawTweetText(text_tweet)
	if 'birthday' in tokenized:
		age_recipient = {'age':find_age(tokenized),'recipient':find_recipient(tokenized)}
		return age_recipient if all(age_recipient.values()) else None
	else:
		return None

def adjust_spines(ax,spines=['bottom','left']):
	for loc, spine in ax.spines.items():
		if loc in spines:
			spine.set_position(('outward',10)) # outward by 10 points
			spine.set_smart_bounds(True)
		else:
			spine.set_color('none') # don't draw spine

	# turn off ticks where there is no spine
	if 'left' in spines:
		ax.yaxis.set_ticks_position('left')
	else:
		# no yaxis ticks
		ax.yaxis.set_ticks([])

	if 'bottom' in spines:
		ax.xaxis.set_ticks_position('bottom')
	else:
		# no xaxis ticks
		ax.xaxis.set_ticks([])

#-------------

flatten =  lambda lst: [item for sublist in lst for item in sublist]

tweets = []
for filename in filenames:
	try:
		tweets.extend([extract_text(tweet_object) 
				for tweet_object in json.load(open(os.path.join(base,filename),READ))])
	except ValueError:
		print 'Could not open %s'%filename

targets = filter(None,map(find_age_recipient,tweets))
print(len(targets))
visualize = True
if visualize:
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.hist([max(tweeter['age']) for tweeter in targets],color='k',range=(0,100))
	adjust_spines(ax)
	ax.yaxis.grid(color='w',which='major')
	ax.set_xlabel(r'\Large \textsc{Age (years)}')
	ax.set_ylabel(r'\Large \textsc{Frequency}')
	plt.show()
