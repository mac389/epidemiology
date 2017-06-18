import json, datetime, os
from TwitterAPI import TwitterAPI

TWITTER_PATH = os.path.join('..','data','twitter')
directory = json.load(open(os.path.join('..','data','credentials.json'),'rb'))
keys = directory['twitter']

timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
api = TwitterAPI(keys['consumer_key'], keys['consumer_secret'], 
				keys['access_token'], keys['access_token_secret'])

def query(query):
	outfile = os.path.join(TWITTER_PATH,'%s-%s'%(query,timestamp))
	r = api.request('statuses/filter', {'track':query})
	with open(outfile,'wb') as outfile:
		for item in r:
			print>>outfile,json.dumps(item)