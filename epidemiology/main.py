import ast, json
from pprint import pprint
from collections import Counter

fname = "bob"
tweets = open(fname,'rb').read().splitlines()
#tweets = map(ast.literal_eval,tweets)

processed_tweets = []
for tweet in tweets:
	try:
		processed_tweets.append(json.loads(tweet))
	except:
		pass

#pprint(processed_tweets[0].keys())
print processed_tweets[0]['coordinates'],'Coordinates'
print processed_tweets[0]['geo'],'Geo'
'''
#Loop
langs = []
for tweet in processed_tweets:
	langs.append(tweet["lang"])

#List Comprehension
langs = [tweet["lang"] for tweet in processed_tweets]

#print langs
pprint(sorted(dict(Counter(langs)).items(), 
	key=lambda item:item[-1])[::-1])
'''