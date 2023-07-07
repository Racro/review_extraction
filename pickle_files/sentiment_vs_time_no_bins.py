import pickle
import string
import sys
import calendar
import datetime
from transformers import pipeline

#hook into the fine-tuned model
import os
import requests
# API_URL = "https://api-inference.huggingface.co/models/racro/sentiment-browser-extension"
# header_key = "Bearer " + os.environ.get("huggingface_model_read")
# headers = {"Authorization": header_key}
# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()

from threading import Thread, Lock
neutral_reviews = 0
total_reviews = 0

def load_dict(filename):
    f = open(filename, 'rb')
    data = pickle.load(f)
    f.close()
    return data

def remove_elements(lst, element):
    z = [i for i in lst if i!=element]
    return z 

def conv_datetime(date):
    try:
        if "ago" in date:
            return datetime.datetime(2022, 8, 8)
        elif "Modified" in date:
            element = date.split(" ")
            return datetime.datetime(int(element[3]), list(calendar.month_abbr).index(element[1]), int(element[2][:-1]))
        else:
            element = date.split(" ")
            try:
                if (len(element) == 2):
                    if (list(calendar.month_abbr).index(element[0]) >= 9):
                        year = 2021
                    else:
                        year = 2022
                    conv_date = datetime.datetime(year, list(calendar.month_abbr).index(element[0]), int(element[1]))
                    return conv_date
                elif (len(element) == 3):
                    conv_date = datetime.datetime(int(element[2]), list(calendar.month_abbr).index(element[0]), int(element[1][:-1]))
                    return conv_date
                else:
                    raise Exception("misformed date")
            except Exception as e:
                print("date without modified/ago")
                print(e)
                print(date)
                return datetime.datetime(2022, 8, 8)
    except Exception as e:
        print("date with modified/ago")
        print(e)
        print("date argument: ", date)

# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# tokenizer = AutoTokenizer.from_pretrained("racro/sentiment-analysis-browser-extension")
# model = AutoModelForSequenceClassification.from_pretrained("racro/sentiment-analysis-browser-extension")

classifier = pipeline('sentiment-analysis', model="racro/sentiment-analysis-browser-extension")

def get_sentiment(text): #text = lower_text
    sentiment = classifier(text, truncation=True)
    global total_reviews
    total_reviews += 1
    ret = sentiment[0]['score']
    # if (sentiment[0]['score'] > 0.65):
    if (sentiment[0]['score'] >= 0.5):
        if (sentiment[0]['label'] == 'LABEL_1'):    
        #    return 0 
            return ret 
        else:
        #    return -1
            return (-1*ret)
    # else:
    #     global neutral_reviews
    #     neutral_reviews += 1
    #     #print("Neutral classified text: ", text)
    #     return 0

def pretty_print(filename, data_str): # data_str = {'extn': [[[-ve sentiments],[total reviews]],[timestamps]]}
    f = open(filename, "w")
    global neutral_reviews
    global total_reviews
    f.write("Neutral Reviews: ")
    f.write(str(neutral_reviews))
    f.write("\nTotal Reviews: ")
    f.write(str(total_reviews))
    f.write("\n--------------------------------------\n")
    for extn in data_str:
        f.write(str(extn)+'\n')
        f.write(str(len(data_str[extn][0]))+'\n')
        f.write('-'*5+'\n')
        for i in range(len(data_str[extn][0])):
            f.write(str(data_str[extn][0][i][0]) + ', ' + str(data_str[extn][0][i][1]) + '\n')
            #f.write('-'*25 + '\n')
            if (data_str[extn][0][i][1] > 0):
                f.write(str(data_str[extn][0][i][0]/data_str[extn][0][i][1]) + '\n')
        f.write('-'*50 + '\n')
    f.close()

def run(extn, lock, data_str):
    text = data_str[extn][1]
    date = data_str[extn][0]

    text = remove_elements(text, '')
    date_str = remove_elements(date, '')
    
    date_datetime = []
    if (len(date_str) != len(text)):
        print("length of date_str and text not equal. PLZ CHECK!!!")
        print(len(date_str))
        print(len(text))
        sys.exit(1)
    for i in date_str:
        date_datetime.append(conv_datetime(i))
    for i in range(len(text)): #iterating over the review set
        lower_text = text[i].lower()
        if 'support@' in lower_text or 'hi ' in lower_text or 'hello' in lower_text or '@eff.org' in lower_text: #to eleminate answers to support queries by the extn team
            continue
        sentiment = get_sentiment(lower_text)
    
        try:
            lock.acquire()
            bins[extn][0].append(sentiment) #incrementing total number of reviews
            #bins[extn][0][bin_index][0] = bins[extn][0][bin_index][0] + sentiment #incrementing total number of reviews
            bins[extn][1] = date_datetime #incrementing total number of reviews
            lock.release()
        except Exception as e:
            print(e)
            print(extn)
            print(date_str[i])
            # print(i)

review_dict = load_dict('threaded_output/review_t.pickle')
noscript_review_dict = load_dict('pickle_files/noscript_t.pickle')

bins = {}
for extn in review_dict:
    if extn == "no-script-suite-lite":
        continue
    bins[extn] = [[], []] #1st lst -> % of negative sentiments, 2nd lst -> timestamp, \
                            #if number of -ve reviews between last timestamp and current timestamp is 0, % = 0  
bins['noscript'] = [[], []]

threads = []
dict_lock = Lock()

for extn in review_dict:
    if extn == 'no-script-suite-lite':
    #if extn != 'decentraleyes':
        continue
    else:
        print(extn)
        threads.append(Thread(target=run, args=(extn, dict_lock, review_dict)))
    
threads.append(Thread(target=run, args=('noscript', dict_lock, noscript_review_dict)))

for t in threads:
    print("starting threads")
    t.start()

for t in threads:
    print("joining threads back in")
    t.join()

import pickle
with open('sentimentscore_vs_time_no_bins.pickle', 'wb') as handle:
    pickle.dump(bins, handle, protocol=pickle.HIGHEST_PROTOCOL)

print(bins)

# pretty_print("sentimentscore_vs_time_no_bins.txt", bins)
