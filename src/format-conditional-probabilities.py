import json

from pprint import pprint

t_unconditional = {word:freq for word,freq in json.load(open('t_unconditional.json','rb'))['distribution']}

for key in t_unconditional:
	if 'i' == key:
		print key