import json, datetime, os
from TwitterAPI import TwitterAPI

directory = json.load(open(os.path.join('..','data','credentials.json'),'rb'))
keys = directory['twitter']
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
api = TwitterAPI(keys['consumer_key'], keys['consumer_secret'], 
				keys['access_token'], keys['access_token_secret'])

timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
TWITTER_PATH = os.path.join('..','data','twitter')

if not os.path.exists(TWITTER_PATH):
    os.makedirs(TWITTER_PATH)

def query(query): 
	if not type(query) == type(''):
		query = ' '.join(query)

	print 'Querying REST API for %s'%query
	outfile = os.path.join(TWITTER_PATH,'%s-%s'%(query,timestamp))
	r = api.request('search/tweets', {'q':query,'count':100})
	
	with open(outfile,'wb') as outfile:
		for item in r:
			print>>outfile,json.dumps(item)