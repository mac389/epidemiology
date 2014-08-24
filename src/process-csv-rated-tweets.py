import csv,os, json, itertools

from pprint import pprint

base = '/Volumes/My Book/Dropbox/ToxTweet/datasets/age_tweets'
READ = 'rU'
WRITE = 'wb'
filenames = [os.path.join(base,filename) for filename in os.listdir(base)]

verboten = ['1','-1','']
data = list(itertools.chain(*[[record for record in csv.DictReader(open(filename,READ)) if record['Age'] not in verboten] for filename in filenames]))

savename = 'tweets_with_ages.json'
full_savename = os.path.join('../data',savename)


if not os.path.isfile(full_savename):
	json.dump(data,open(full_savename,WRITE))