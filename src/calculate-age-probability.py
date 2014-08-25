from __future__ import division 
import nltk, json, cPickle, itertools

import numpy as np
import twokenize as Tokenizer

from nltk.tokenize import word_tokenize
from pprint import pprint
from operator import mul


class EstimateAge(object):

	def __init__(self,tweet):		
		self.t_given_a = json.load(open('../final-accuracy/conditional_probability.json','rb'))
		self.a_unconditional = json.load(open('../final-accuracy/age.json','rb'))

		self.t_unconditional = json.load(open('../final-accuracy/t_unconditional_2.json','rb'))
		self.denominator = sum(self.t_unconditional.values())
		#test_sentence = "i in the library"

		print self.denominator

		self.positive_controls = {
			'a1318':['there is no school tomorrow','there is =/=','no school tomorrow',
										'there is first impression','first impression','there are braces','braces'],
			'a1922':['i on campus','on campus'],
			'a2329':['i to work today','to work today'],
			'a30':['i a conscious decision', 'a conscious decision','i for a lifetime']}

		self.test_sentence = self.positive_controls['a30'][0] + ' ' + self.positive_controls['a1318'][-4]
		self.tweet = tweet if tweet != '' else self.test_sentence

	def normalize(self,probabilities):
		#-- Assumes that probabilities is a dictionary of form key = term, value = probability

		normalization_factor = np.nansum(np.absolute(probabilities.values()))
		if normalization_factor >0:
			for term in probabilities:
				tmp = probabilities[term]
				probabilities[term] = np.nan_to_num(tmp)/normalization_factor
		else: 
			return {key:0 for key in probabilities} #Shouldn't put every number to zero, it's more rigorous to use masked arrays
		return probabilities

	def estimate_age(self, ngram=3,verbose=False):
		p = {age:np.nan for age in self.t_given_a}
		tokens = Tokenizer.tokenizeRawTweetText(self.tweet)

		ngrams = [' '.join(token) for n in range(1,ngram+1) for token in itertools.combinations(tokens,n)]
		ngrams = [ngram for ngram in ngrams if any(ngram in self.t_given_a[age] for age in self.t_given_a)]

		if verbose:
			print ngrams

		for ngram in ngrams:
			for age in self.t_given_a:
				if ngram in self.t_given_a[age]:
					if ngram in self.t_unconditional:
						p[age]= self.t_given_a[age][ngram]*float(self.a_unconditional[age]*self.denominator/self.t_unconditional[ngram])
					else:
						#Which words of ngram are in t_unconditional?
						calculated_t_unconditional = [self.t_unconditional[word] for word in ngram.split() if word in self.t_unconditional]
						if len(calculated_t_unconditional) == 0:
							pass

						else:
							calculated_denominator = self.denominator**len(calculated_t_unconditional)			
							calculated_t_unconditional= sum(calculated_t_unconditional)
							p[age] = self.t_given_a[age][ngram]*self.a_unconditional[age]*calculated_denominator/calculated_t_unconditional


		return self.normalize(p)

if __name__ == '__main__':
	test_sentence = 'my husband : o'
	test = EstimateAge(test_sentence)
	print test.estimate_age()
#Doesn't account for bigrams