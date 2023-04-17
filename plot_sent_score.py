# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns
import pandas as pd
import pickle
f = open('pickle_files/sentimentscore_vs_time.pickle', 'rb')
bins = pickle.load(f)
f.close()

#plt.xlabel('timestamps')
#plt.ylabel('ratio of negative sentiments')

# fig_size
fig = plt.figure(figsize =(20, 15))

# Creating plot
#print(bins['noscript'])
#sys.exit(1)
index = []
ts = []
sent = []
sent_pos = []
sent_neg = []

days = 120

def filter_sentiment(nr, dr):
    lnr = 0
    lnr_pos = 0
    lnr_neg = 0
    dnr = 0
    for i in nr:
        lnr += 1
        if i >= 0:
            lnr_pos += 1
        elif i <= 0:
            lnr_neg += 1 
        #lnr.append(i)
        dnr = 1
    return [lnr, lnr_pos, lnr_neg], dnr

for extn in bins:
    if extn == 'no-script-suite-lite':
        continue
    #elif extn == 'adblock-plus-free-ad-bloc' or extn == 'ublock-origin' or extn == 'adguard-adblocker' or extn == 'ghostery-–-privacy-ad-blo': 
    elif extn == 'ublock-origin':# or extn == 'adguard-adblocker' or extn == 'ghostery-–-privacy-ad-blo': 
    #elif extn == 'disconnect' or extn == 'privacy-badger' or extn == 'decentraleyes': 
        timestamp = []
        total_rev = []
        std = []
        #print(extn)
        sent_lst = []
        sent_posl = []
        sent_negl = []
        
        numr = 0
        denr = 0
        for i in range(len(bins[extn][0])):
            if days == 60:
                numr = bins[extn][0][i][0]
                denr = bins[extn][0][i][1]
                if (denr > 0):
                    timestamp.extend([bins[extn][1][i]] * len(numr))
                    total_rev.append(denr)
                    sent_lst.extend(numr)

            elif days == 120:
                if (i%2 == 0):
                    numr = bins[extn][0][i][0]
                    denr = bins[extn][0][i][1]
                else:
                    numr.extend(bins[extn][0][i][0])
                    denr += bins[extn][0][i][1]
                    if (denr > 0):
                        # numr, denr = filter_sentiment(numr, denr)
                        # numr_p = [numr[1]] 
                        # numr_n = [numr[2]]
                        # numr = [numr[0]]
                        numr = [sum(numr)/len(numr)]
                        timestamp.extend([bins[extn][1][i]] * len(numr))
                        total_rev.append(denr)
                        # sent_lst.extend(numr)
                        # sent_posl.extend(numr_p)
                        # sent_negl.extend(numr_n)

                        sent_lst.append(numr)
                        # sent_posl.append(numr_p)
                        # sent_negl.append(numr_n)

        index.extend([extn]*len(timestamp))
        ts.extend(timestamp)
        sent.extend(sent_lst)
        # sent_pos.extend(sent_posl)
        # sent_neg.extend(sent_negl)

        # total_rev = np.array(denr)
        # mean = np.sum(sent_lst, axis=1)/total_rev

        # plt.plot(timestamp, mean, label = extn)

import pymannkendall as mk
print(mk.original_test(np.array(sent)))
# print(mk.original_test(np.array(sent_pos)))
# print(mk.original_test(np.array(sent_neg)))
sys.exit(0)

print(len(index), len(ts), len(sent), len(sent_pos))
df = pd.DataFrame({'extn':index, 'x':ts, 'y':sent})
df_pos = pd.DataFrame({'extn':index, 'x':ts, 'y':sent_pos})
df_neg = pd.DataFrame({'extn':index, 'x':ts, 'y':sent_neg})
print(df.head())
#sys.exit(0)
sns.lineplot(x = 'x', y = 'y', hue = 'extn', data=df)
sns.lineplot(x = 'x', y = 'y', data=df_pos, color='red')
sns.lineplot(x = 'x', y = 'y', data=df_neg, color='green')
#plt.savefig('plots/antitracker_raw_ci.png')
plt.show()
#plt.savefig('plots/adblocker_raw_ci.png')

# plt.title("sentiment_vs_time_antitrack")
# plt.legend()
# # show plot
# # plt.savefig('plots/sentiment_vs_time_120_'+extn+'.png')
# plt.savefig('plots/sentiment_vs_time_antitrack.png')
# # plt.clf()
