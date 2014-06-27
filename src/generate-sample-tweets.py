#picking any 4 cells in one age group
#do that 100 times (generate 100 strings)
#save the strings
#4 cells: 3 from one age group; the other 1 from another age group
#4 cells: each cell from one age group; 4 cells from 4 different age groups
#a total of 11 files
#random.sample

import json,random 

t_given_a = json.load(open('conditional_probability.json','rb'))
n_samples = 1000
WRITE = 'wb'

pure = False
if pure:
	#-- Pure sample
	for age_group in t_given_a:
		filename = 'samples-%s'%age_group
		with open(filename,WRITE) as f:
			for _ in xrange(n_samples):
				print>>f,' '.join(random.sample(t_given_a[age_group],4))

mixed = True
if mixed:
	for major_age_group in t_given_a: #Choose 3 from this
		for minor_age_group in t_given_a: #Choose 1 from this
			filename = 'mixed-samples-%s-%s'%(major_age_group,minor_age_group)
			with open(filename,WRITE) as f:
				for _ in xrange(n_samples):
					print>>f,' '.join(random.sample(t_given_a[major_age_group],3)+ 
									random.sample(t_given_a[minor_age_group],1))
	#-- Mixed sample (3 parts intended, 1 part unintended)
