import os,json

import numpy as np

from calculate_age_probability import EstimateAge
from progressbar import Bar, ProgressBar, Percentage

base = '../data/tweets_from_verified_users'
users = [os.path.join(base,filename) for filename in os.listdir(base)]
READ ='rb'
WRITE = 'wb'
categories = ['a1318','a1922','a2329','a30']

def age_likelihoods(tweet):
	estimates = EstimateAge(tweet).estimate_age()
	return [estimates[category] for category in estimates]

def iqr(mat): #assume each column is a variable, find the iqr of the columns
	return 0.5*(np.percentile(mat,75,axis=0)-np.percentile(mat,25,axis=0))

def all_age_estimates_users(tweets,user):
	ages = np.array([age_likelihoods(tweet) for tweet in tweets])
	try:
		iqrs = iqr(ages)
		ages = ages.sum(axis=0)                 
		ages /= ages.sum()
		ans={'medians':dict(zip(categories,ages)),'iqrs':dict(zip(categories,iqrs))}
	except ValueError:
		ans={'medians':dict(zip(categories,ages))}
	return ans
age_estimates = {user.split('/')[-1]:all_age_estimates_users(open(os.path.join(user,'tweets'),READ).read().splitlines(),user) for user in users
                if os.path.isdir(user)}    
json.dump(age_estimates,open(os.path.join('../data/rated-tweets','age_estimates_from_many_tweets.json'),WRITE))
#must cleanse tweets
