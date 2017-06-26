import os, json 

import pandas as pd 
import pyopendata as pyod

from pprint import pprint 

store = pyod.DataStore('http://catalog.data.gov/')
packages = store.search('Alcohol Licensing')

pprint(packages)
