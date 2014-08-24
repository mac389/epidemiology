import csv,os

base = '/Volumes/My Book/Dropbox/ToxTweet/datasets/age_tweets'
READ = 'rU'

filenames = [os.path.join(base,filename) for filename in os.listdir(base)]
data = [record for record in csv.DictReader(open(filename,READ)) for filename in filenames if record['Age'] != '']

