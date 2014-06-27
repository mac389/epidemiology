from __future__ import division 

EstimateAge = __import__("calculate-age-probability").EstimateAge

import numpy as np
from pprint import pprint
from progress.bar import Bar

def age_from_probabilities(probabilities):
	#Algorithm is finding key associated with maximum value
	 return max(probabilities.iterkeys(),key=lambda key:probabilities[key])

age_groups = ['a1318','a1922','a2329','a30']
READ = 'rb'
TAB = '\t'

confusion_table = np.zeros((len(age_groups),len(age_groups))).astype(int)
index = dict(zip(age_groups,range(len(age_groups))))

verbose = False


lifts = {age_group:[] for age_group in age_groups}

reps = 10
bar = Bar('Calculating accuracy',max=12000*reps)
for rep in xrange(reps):
	for major_age_group in age_groups:
		for minor_age_group in age_groups:
			if major_age_group == minor_age_group:
				filename = 'mixed-samples-%s-%s'%(major_age_group,minor_age_group)
				sentences = open(filename,READ).read().splitlines()
				for test_sentence in sentences:
					estimator = EstimateAge(test_sentence)
					age_groups = estimator.estimate_age()
					age_group = age_from_probabilities(age_groups)
					
					#Augment confusion table
					if age_group: 
						actual = index[major_age_group] if age_groups[major_age_group] > 0 else index[age_group]
						estimated = index[age_group]
					
						if actual != estimated and verbose:
							print '--------------'
							print 'Actual :  %d || Guessed : %s'%(actual,estimated)
							print test_sentence
							estimator = EstimateAge(test_sentence)
							print estimator.estimate_age(verbose=True)
							print '--------------'
						confusion_table[actual][estimated] += 1
					del estimator
					bar.next()
		print 
		pprint(confusion_table)
	bar.finish()
	'''
	for major_age_group in age_groups:
		filename = '%s.txt'%(major_age_group)
		sentences = open(filename,READ).read().splitlines()
		for test_sentence in sentences:
			age_group = age_from_probabilities(EstimateAge(test_sentence).estimate_age())
			
			#Augment confusion table
			if age_group:
				actual = index[major_age_group]
				estimated = index[age_group]
			
				confusion_table[actual][estimated] += 1
	'''
	np.savetxt('confusion-table-pure-emoticontokenizer_1-trial-%d.tsv'%rep,confusion_table,fmt='%d',delimiter=TAB, footer='(Actual,Estimated)')
	print np.trace(confusion_table)/confusion_table.sum()
	#print np.diag(confusion_table)/confusion_table.sum(axis=1)
	pprint(confusion_table)
