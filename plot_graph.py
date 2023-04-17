# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import sys

import pickle
f = open('sentiment_vs_time.pickle', 'rb')
bins = pickle.load(f)
f.close()

plt.xlabel('timestamps')
plt.ylabel('ratio of negative sentiments')

# fig_size
fig = plt.figure(figsize =(20, 15))

# Creating plot
#print(bins['noscript'])
#sys.exit(1)
for extn in bins:
    if extn == 'no-script-suite-lite':
        continue
    #elif extn == 'adblock-plus-free-ad-bloc' or extn == 'ublock-origin' or extn == 'adguard-adblocker' or extn == 'ghostery-–-privacy-ad-blo': 
    elif extn == 'disconnect' or extn == 'privacy-badger' or extn == 'decentraleyes': 
        timestamp = []
        mean = []
        std = []
        #print(extn)
        numr = 0
        denr = 0
        for i in range(len(bins[extn][0])):
            if (i%2 == 0):
                numr = bins[extn][0][i][0]
                denr = bins[extn][0][i][1]
            else:
                numr += bins[extn][0][i][0]
                denr += bins[extn][0][i][1]
                if (denr > 0):
                    timestamp.append(bins[extn][1][i])
                    mean.append(-1*numr/denr)
                
        plt.plot(timestamp, mean, label = extn)
plt.title("sentiment_vs_time_antitrack")
plt.legend()
# show plot
# plt.savefig('plots/sentiment_vs_time_120_'+extn+'.png')
plt.savefig('plots/sentiment_vs_time_antitrack.png')
# plt.clf()
