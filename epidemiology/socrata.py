#From socrata

import json
from pprint import pprint 

d = json.load(open('./socrata.json','rb'))
#pprint(d)

print len(d)
print d[0].keys()

zipcodes = []
for farmer in d:
	if 'zipcode' in farmer.keys():
		zipcodes.append(farmer["zipcode"])
	else:
		zipcodes.append(None)
print zipcodes

"""
#List comprehension

zipcodes = [farmer["zipcode"] if zipcode in farmer.keys()
							   else None
							   for farmer in d]

"""