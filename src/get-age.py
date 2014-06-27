import re

import twokenize as Tokenizer

from pprint import pprint

test = ["Happy Bday @ImTheFrancescaC You're 10 years old! I wish you have amazing day LYSM pretty #birthday #of #a #princess pic.twitter.com/1s4DiF7TOn"]

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

	
find_age(test)

def find_age_recipient(text_tweet):
	tokenized = Tokenizer.tokenizeRawTweetText(text_tweet)
	print tokenized
	return {'age':find_age(tokenized),'recipient':find_recipient(tokenized)}

for tweet in test:
	pprint(find_age_recipient(tweet))