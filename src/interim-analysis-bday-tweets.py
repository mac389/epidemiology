import csv

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rcParams
rcParams['text.usetex'] = True

filename = '../data/better-birthday-frequencies.csv'

format = lambda text: r'\Large \textbf{\textsc{%s}}'%text
def simpleaxis(ax,remove=['top','right']):
	for spine in remove:
		ax.spines[spine].set_visible(False)
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()

with open(filename,'rb') as f:
	reader = csv.reader(f)
	reader.next()
	data = np.array([row[-1] for row in reader if row[-1] != '']).astype(int)

print len(data[(data<18) & (data>=13)])
print len(data[(data>=18) & (data <=22)])
print len(data[(data>22) & (data <30)])
print len(data[data>=30])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(data, bins=20,color='#252525',alpha=0.8,range=(10,50))
simpleaxis(ax)
ax.set_xlabel(format('Age'))
ax.set_ylabel(format('Occurences'))



plt.tight_layout()
plt.show()