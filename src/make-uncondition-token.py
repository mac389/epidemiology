import nltk, os, json, csv, string, cPickle, re
from scipy.stats import scoreatpercentile

from pprint import pprint
from progress.bar import Bar

READ = 'rb'
WRITE = 'wb'
stopwords = set(open('stopwords',READ).read().splitlines())
exclude = set(string.punctuation)

#lemmatizer
lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
base = '/Volumes/My Book/carrie-controls/'
#get the names of the files in a list
json_list = [os.path.join(base,datafile) 
			 for datafile in 
			 filter(lambda string: string.endswith('json'),os.listdir(base))]

def sanitize(wordList):
	#Lemmatize
	answer = [lmtzr.lemmatize(word.lower()) for word in wordList]

	#Remove stopwords
	#answer = list(set(answer)-stopwords)

	#Remove non-english words
	answer = [word for word in answer if all([ord(letter)<128 for letter in word])]

	#Remove links
	answer = [word for word in answer if not any([filler in word for filler in ['http://','t.co/']])]
	return answer

words = []
bar = Bar('Converting JSON files to proper text',max=len(json_list))
for filename in json_list:
	words.extend([sanitize(nltk.word_tokenize(' '.join([tweet['text'] 
			for tweet in json.load(open(filename,READ))])))])
	bar.next()
bar.finish()

words = [item for sublist in words for item in sublist]
freq = dict(nltk.FreqDist(words).items())
#cutoff = scoreatpercentile(freq.values(),15)
#vocab = [word for word,f in freq.items() if f > cutoff] 
#cPickle.dump({'distribution':freq,'cutoff':cutoff},open('freqdist_2.pkl',WRITE))
cPickle.dump(freq,open('t_unconditional.pkl','wb')) #This could be saved in a more transparent way.