epidemiology
============

Tools for estimating epidemiological quantities from social media

Central calculation
===========

  Let _r_ be the regression coefficient for a word _w_ with respect to some age group _a_. We convert this regression coefficient to an odds ratio by noting that the exponential of the regression coefficient in logistic regresion is the odds ratio, _OR_.  We convert the odds ratio to a probability, _p_, by noting that _p_ = _OR_/(_OR_+1).

  We assume each word occurs independently in a piece of text _t_. This assumption allows us to calculate the probability of a tweet _t_ with _n_ words occurring as the joint probability of _n_ events. [CAN WE CALCULATE THE BOUNDS OF THE ERROR THIS APPPROXIMATION INTRODUCES?]
  
Notes
===========
Forget words that occur less than 100 times