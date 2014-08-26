epidemiology
============

Tools for estimating epidemiological quantities from social media

Central calculation
===========

  Let _r_ be the regression coefficient for a word _w_ with respect to some age group _a_. We convert this regression coefficient to an odds ratio by noting that the exponential of the regression coefficient in logistic regresion is the odds ratio, _OR_.  We convert the odds ratio to a probability, _p_, by noting that _p_ = _OR_/(_OR_+1).

  We make the naive assumption that each word occurs independently of all other words in a piece of text _t_. This assumptions allows us to calculate the probability of a tweet _t_ occuring as the product of the probaility of each of its words occuring.