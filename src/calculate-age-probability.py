from __future__ import division 
import nltk, json, cPickle, itertools, string

import numpy as np
import twokenize as Tokenizer

from nltk.tokenize import word_tokenize
from pprint import pprint  
from operator import mul

class EstimateAge(object):

	def __init__(self,tweet):		
		self.t_given_a = json.load(open('../final-accuracy/conditional_probability.json','rb'))
		self.a_unconditional = json.load(open('../final-accuracy/age.json','rb'))
		self.t_unconditional = cPickle.load(open('../data/t_unconditional.pkl','rb'))
        
		self.denominator = sum(self.t_unconditional.values())
        #test_sentence = "i in the library"

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

	def regression_coefficient_to_probability(self,coefficient):
		odds = np.exp(coefficient)
		return odds/float(odds+1)
    
	def token_tag(self,token):
		#Crude approximation that any piece of text that contains punctuation marks is an emoticon        
		return (token,'EMOTICON' if any([mark in token for mark in string.punctuation]) else 'TEXT')
    
	def estimate_age(self, ngram=3,verbose=False):
		p = {age:np.nan for age in self.t_given_a}
		tokens = Tokenizer.tokenizeRawTweetText(self.tweet)

		CONTENT = 0
		TYPE = 1
		#Semantically meaningful indices for accessing ngrams
		ngrams = [' '.join(token) for n in range(1,ngram+1) for token in itertools.combinations(tokens,n)]
		ngrams = [self.token_tag(ngram) for ngram in ngrams if any(ngram in self.t_given_a[age] for age in self.t_given_a)]
		
		if verbose:
			print ngrams

		for age in self.t_given_a:
			print 'Calculating conditional probability for %s'%age
			for ngram in ngrams:
				if ngram[CONTENT] in self.t_given_a[age]:
					if ngram[CONTENT] in self.t_unconditional:
						print '\t token %s in %s, p(t|a) = %.02f'%(ngram[CONTENT],age,self.regression_coefficient_to_probability(self.t_given_a[age][ngram[CONTENT]]))
						if p[age] != np.nan:
							tmp = p[age]
							tmp *= self.regression_coefficient_to_probability(self.t_given_a[age][ngram[CONTENT]])*float(self.denominator/self.t_unconditional[ngram[CONTENT]])
						else:
							p[age]  = self.regression_coefficient_to_probability(self.t_given_a[age][ngram[CONTENT]])*float(self.denominator/self.t_unconditional[ngram[CONTENT]])
						print p[age]
					else:
						print '\t token %s not in %s, calculating p(t|a) by composition'%(ngram,age)
						calculated_t_unconditional = [self.t_unconditional[word] for word in ngram[CONTENT].split() if word in self.t_unconditional and ngram[TYPE] !='EMOTICON']
						calculated_denominator = self.denominator**len(calculated_t_unconditional)
						if verbose:
							if ngram[TYPE] == 'EMOTICON':
								print "\t\t Cannot calculate probabliity of %s by composition. It's an emoticon"%(ngram[CONTENT])
							else:
								for word in ngram[CONTENT].split():
									if word in self.t_unconditional and word in self.t_given_a[age]:
										print '\t\t\t Calculating probability for %s'%(word)
										print '\t\t\t\t %s:  t=%.07f'%(word, self.t_unconditional[word]/calculated_denominator)
										print '\t\t\t\t p(%s|%s)=%.04f'%(word,age,self.regression_coefficient_to_probability(self.t_given_a[age][word]))
									else:
										print '\t\t\t Missing t or p(t|a), cannot calculate probability for %s'%word
						if len(calculated_t_unconditional) > 0:
							token_length = len(calculated_t_unconditional)
							calculated_t_unconditional= reduce(mul,calculated_t_unconditional,1)
							print '\t p(%s) t | a = %.02f, a = %.02f, t=%.07f'%(ngram[CONTENT],self.regression_coefficient_to_probability(self.t_given_a[age][ngram[CONTENT]]),self.a_unconditional[age]**token_length,calculated_t_unconditional/calculated_denominator)
							p[age] = self.regression_coefficient_to_probability(self.t_given_a[age][ngram[CONTENT]])*self.a_unconditional[age]**token_length*calculated_denominator/calculated_t_unconditional
							print '\t After calculating composition t uncondition p[%s|%s]=%.02f'%(age,ngram,p[age])
		return p

if __name__ == '__main__':
	test_sentence = 'my husband : o'
	test = EstimateAge(test_sentence)
	print test.estimate_age(verbose=True)
#Need larger sample of unconditional token distribution