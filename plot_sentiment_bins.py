# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import sys

import pickle
f = open('sentimentscore_vs_time.pickle', 'rb')
bins = pickle.load(f)
f.close()

plt.xlabel('timestamps')
plt.ylabel('ratio of negative sentiments')

# fig_size
fig = plt.figure()

x_axis = np.around(np.arange(-1,1.1, 0.1), 1)
dist = {}
for extn in bins:
    dist[extn] = {}
print(x_axis)
# Creating plot
#print(bins['noscript'])
#sys.exit(1)
width = 0.02
j=-2
for extn in bins:
    if extn == 'no-script-suite-lite':
        continue
    #elif extn == 'adblock-plus-free-ad-bloc' or extn == 'ublock-origin' or extn == 'adguard-adblocker' or extn == 'ghostery-–-privacy-ad-blo': 
    elif extn == 'disconnect' or extn == 'privacy-badger' or extn == 'decentraleyes': 
        for i in x_axis:
            dist[extn][i] = 0
        sentiment = []
        for i in range(len(bins[extn][0])):
            sentiment.extend(bins[extn][0][i][0])

        sentiment = np.array(sentiment)
        sentiment = np.around(sentiment, 1)
        for i in sentiment:
            dist[extn][i] = dist[extn][i] + 1
        print(dist[extn].values())
        plt.bar(x_axis+j*width, list(dist[extn].values()), width, label = extn)
        j=j+1
plt.title("score_vs_sentiment")
plt.legend()
# show plot
# plt.savefig('plots/sentiment_vs_time_120_'+extn+'.png')
#plt.savefig('plots/score_vs_sentiment_raw_adblocker_new.png')
plt.savefig('plots/score_vs_sentiment_raw_antitracker_new.png')
# plt.clf()
