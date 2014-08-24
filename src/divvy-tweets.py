import csv, random
import numpy as np

filename = '../data/birthday-tweets-fuller.csv'

data = [row for row in csv.reader(open(filename,'rU'))]
random.shuffle(data)

recipients = ['Nick','Carrie','Linus','Andy','Mike']

splits = np.array_split(data, len(recipients))

for recipient,part in zip(recipients,splits):
	with open('../data/%s.csv'%recipient,'wb') as f:
		writer = csv.writer(f)
		writer.writerows(part)