import json,os
import numpy as np 
base = '../data/rated-tweets'
READ = 'rU'
filename = 'tweets_with_ages.json'

ages_from_tweets = {record['Person whose age we surmised']: record['Age'] for record in json.load(open(os.path.join(base,filename),READ))}

ages_from_raters = json.load(open(os.path.join(base,'age_estimates_from_many_tweets.json')))
users = set(ages_from_tweets.iterkeys()) & set(ages_from_raters.keys())

age_ranges = [(1,22),(23,29),(30,100)] #There are some tweets with ages < 13!
#age_ranges = [(1,18),(19,22),(23,29),(30,100)] #There are some tweets with ages < 13!
json_age_ranges = ['a1318','a1922','a2329','a30']

def compare_accuracy(tup,verbose=False):
	print tup
	age,predicted_dict = tup
	ans = np.zeros((len(age_ranges),len(age_ranges)))
	if sum(predicted_dict.values())>0:
		try:
			age = int(age)
			if verbose:
				print tup
			i = [i for i,(lower_bound,upper_bound) in enumerate(age_ranges) if age >= lower_bound and age <= upper_bound][0]
			j = json_age_ranges.index(max(predicted_dict.iterkeys(), key=(lambda key: predicted_dict[key])))
			j = 0 if j ==1 or j==0 else j-1
			if verbose:
				print i,j       
			ans[i,j] = 1

		except ValueError:
			pass    
	return (tup,ans)

assessed = [compare_accuracy((ages_from_tweets[user],ages_from_raters[user]['medians'])) for user in users]
    
#assess accuracy

contingency_table = np.sum(entry[-1] for entry in assessed)
print contingency_table
print np.trace(contingency_table)/np.sum(contingency_table)
