import json,os

import numpy as np
import matplotlib.pyplot as plt

data = json.load(open('../final-accuracy/t_unconditional_2.json','rb'))


print len(data)
cutoff = 100
truncated = {key:value for key,value in data.items() if value > cutoff}

truncated_filename = '../data/truncated_t_unconditional.json'
if not os.path.exists(truncated_filename):
    json.dump(truncated,open(truncated_filename,'wb'))
    
visualize = False
if visualize:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(np.log(truncated.values()),color='k')
    ax.set_ylabel('No. of words with that frequency')
    ax.set_xlabel('Word frequency')
    plt.tight_layout()
    plt.savefig('../results/t_unconditional_word_distribution_truncated.png',dpi=300)