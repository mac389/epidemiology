import json,os,cPickle

from collections import Counter
#concert Simpsons dictionary to text (using this as a proxy of modern spoken English), cite Wiktionary



if not os.path.isfile('simpsons-dictionary'):
	txts = open('anKcMdvk.txt','rb').read().splitlines()

	dictionary = {}

	for entry in txts:
		_,word,frequency = entry.split()
		frequency = int(frequency.strip('()'))
		dictionary[word] = frequency

	json.dump(dictionary,open('simpsons-dictionary','wb'))
else:
	dictionary = json.load(open('simpsons-dictionary','rb'))

new_entries = Counter(dictionary)



merge = True
t_unconditional = Counter(cPickle.load(open('t_unconditional.pkl','rb')))
print max(t_unconditional.values())

if merge:
	merged = t_unconditional + new_entries

	json.dump(merged,open('t_unconditional_2.json','wb'))

with open('t_unconditional','wb') as f:
	for word,frequency in merged.iteritems():
		if all([ord(ch)<128 for ch in word]):
			print>>f,'%s \t %d'%(word,frequency)
