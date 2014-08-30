import json

import numpy as np

from calculate_age_probability import EstimateAge

def compare_accuracy(tup,verbose=False):
	age,predicted_dict = tup
	ans = np.zeros((len(age_ranges),len(age_ranges)))

	if not all([age_guess==0 for age_guess in predicted_dict.values()]):
		try:
			print age			
			age = int(age)
			if verbose:
				print tup, age
			i = [i for i,(lower_bound,upper_bound) in enumerate(age_ranges) if age >= lower_bound and age <= upper_bound].pop()
			j = json_age_ranges.index(max(predicted_dict.iterkeys(), key=(lambda key: predicted_dict[key])))
			j = 0 if j ==1 or j==0 else j-1
			if verbose:
				print i,j    
			ans[i,j] = 1

		except ValueError:
			pass    
	return (tup,ans)

filename = '../data/tweets_with_ages.json'
READ = 'rb'

rated_tweets = json.load(open(filename,READ))
#load tweets

#calculate age 

age_ranges = [(1,22),(23,29),(30,100)] #There are some tweets with ages < 13!
#age_ranges = [(1,18),(19,22),(23,29),(30,100)] #There are some tweets with ages < 13!
json_age_ranges = ['a1318','a1922','a2329','a30']

assessed = [compare_accuracy((tweet['Age'],EstimateAge(tweet['Text']).estimate_age()),verbose=True) for tweet in rated_tweets]
    
#assess accuracy

contingency_table = np.sum(entry[-1] for entry in assessed)
print contingency_table
print np.trace(contingency_table)/np.sum(contingency_table)
'''
   Confusion table structured as
        Predicted
     ------------->
	 |
 Act |
     |
     |
     V
'''