import pickle
import nltk
import string
import sys
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer

from threading import Thread, Lock

from transformers import pipeline # for sentiment analysis

classifier = pipeline('sentiment-analysis', model="racro/sentiment-analysis-browser-extension") # classifier
ps = PorterStemmer()
#lemmatizer = WordNetLemmatizer()

def load_dict(filename):
    f = open(filename, 'rb')
    data = pickle.load(f)
    f.close()
    return data

def load_custom_stopwords():
    f = open('./../pes/nltk/stopwords/english', 'r')
    stopwords = f.read().split('\n')
    return stopwords

def remove_elements(lst, element):
    z = [i for i in lst if i!=element]
    return z 

keywords = {
    'block': ['block', 'prevent', 'protect', 'secure', 'detect', 'bypass'],
    'ads': ['popup', 'pop-up', 'malvertising', 'cdn', 'content delivery', 'spyware', 'adware', 'malware', 'paid', 'tabs', 'notification', 'annoy'],
    'fingerprinting': ['fingerprint'],
    'break':['break', 'broke', 'rendering', 'error', 'bug', 'stop', 'access', 'reload', 'load', 'unusable', 'crash', 'mess', 'cannot open', 'hang', 'fail', 'corrupt', 'fix'],
    'tracking': ['3rd', 'third', 'party', 'tracking', 'icons', 'javascript', 'private', 'redirect', 'vpn'],
    'manual': ['manual', 'off', 'features', 'turn off', 'disable', 'click'],
    'filter': ['remove', 'filter', 'list', 'whitelist', 'blocklist', 'blacklist', 'maintain'],
    'update': ['automatic', 'update', 'version', 'corrupt'],
    'config': ['default', 'config', 'configuration', 'sync'],
    'priv_policy': ['privacy', 'policy', 'consent', 'information', 'security', 'notification', 'anonymity', 'install', 'false', 'monetize'],
    'compatibility': ['browser', 'compatible', 'extension', 'chrome', 'firefox', 'disable'], # adblock -> remove sites
#    'remove': ['remove', 'button', 'rid off', 'icon', 'disable'],
    'data': ['permission', 'data', 'encrypt', 'history', 'memory', 'storage', 'leak', 'sell', 'prefetch'],
    'performance': ['efficient', 'inefficient', 'fast', 'light', 'slow', 'heavy', 'speed', 'memory', 'cpu', 'long', 'lag', 'delay', 'cost']
}

processed_keywords_stem = {}
super_classification = {} # without the positive sentiment reviews, only negative sentiments with f score > 0.7
positive_sentiment_set = {} # all positive sentiment reviews
freq_analysis_neg = {}
freq_analysis_pos = {}

review_dict = load_dict('threaded_output/review_t.pickle')
noscript_dict = load_dict('pickle_files/noscript_t.pickle')
# review_dict = load_dict('noscript_t.pickle')
stopwords = load_custom_stopwords()

total_negative_captured_reviews = []
total_positive_captured_reviews = []

for extn in review_dict:
    if extn == 'no-script-suite-lite' or extn == 'bitwarden-free-password-m': 
        continue
    else:
        super_classification[extn] = {}
        positive_sentiment_set[extn] = {}
        for key in keywords:
            super_classification[extn][key] = [[], 0]
            positive_sentiment_set[extn][key] = [[], 0]
            processed_keywords_stem[key] = []
            for i in keywords[key]:
                processed_keywords_stem[key].append(ps.stem(i.lower()))

for extn in noscript_dict:
    if extn == 'noscript':
        super_classification[extn] = {}
        positive_sentiment_set[extn] = {}
        for key in keywords:
            super_classification[extn][key] = [[], 0]
            positive_sentiment_set[extn][key] = [[], 0]
            processed_keywords_stem[key] = []
            for i in keywords[key]:
                processed_keywords_stem[key].append(ps.stem(i.lower()))

for keyword in keywords:
    freq_analysis_neg[keyword] = 0
    freq_analysis_pos[keyword] = 0

def pretty_print(filename, data_str): # data_str = {'extn': {'keyword_key': [[], 0]}}
    f = open(filename, "w")
    for extn in data_str:
        f.write(str(extn)+'\n')
        f.write('-'*5+'\n')
        for category in data_str[extn]:
            f.write(str(str(category) + " - " + str(data_str[extn][category][1]) + '\n'))
            for review in data_str[extn][category][0]:
                f.write(str(review) + '\n')
                f.write('-'*25 + '\n')
            f.write('-'*50 + '\n')
        f.write('-'*100 + '\n')
    f.close()

def run(extn, r_dict, lock):
    text = r_dict[extn][1]
    text = remove_elements(text, '')
    global total_positive_captured_reviews
    global total_negative_captured_reviews
    for i in range(len(text)): #iterating over the review set
        lower_text = text[i].lower()
        if 'support@' in lower_text or 'hi ' in lower_text or 'hello' in lower_text or '@eff.org' in lower_text: #to eleminate answers to support queries by the extn team
            continue

        punc_remove = lower_text.translate(str.maketrans('', '', string.punctuation)) # stemming preparation
        token_lst = word_tokenize(punc_remove)
        #token_lst = [words for words in token_lst if words.casefold() not in stopwords]
        token_stem = []
        del1 = 0
        del2 = 0
        for token in token_lst: #stemming the review
            token_stem.append(ps.stem(token))

        try:
            sentiment = classifier(text[i], truncation=True)
            sentiment_label = sentiment[0]['label'] # storing sentiment values
            sentiment_score = sentiment[0]['score']
        except Exception as e:
            print(e)
            print(text[i])
            print(sentiment_label)
            print(sentiment_score)

        if sentiment_label == 'LABEL_0' and sentiment_score > 0.7:
            for key in keywords:
                for keyword in keywords[key]:
                    if keyword in token_stem:
                        dict_lock.acquire()
                        super_classification[extn][key][0].append(str(keyword + '\n' + text[i]))
                        super_classification[extn][key][1] = super_classification[extn][key][1] + 1
                        dict_lock.release()
                        del1 = 1
                        freq_analysis_neg[key] = freq_analysis_neg[key] + 1
                        break
        elif sentiment_label == 'LABEL_1':
            for key in keywords:
                for keyword in keywords[key]:
                    if keyword in token_stem:
                        dict_lock.acquire()
                        positive_sentiment_set[extn][key][0].append(str(keyword + '\n' + text[i]))
                        positive_sentiment_set[extn][key][1] = positive_sentiment_set[extn][key][1] + 1
                        dict_lock.release()
                        del2 = 1
                        freq_analysis_pos[key] = freq_analysis_pos[key] + 1
                        break
        if del1:
            total_negative_captured_reviews.append(text[i]) 
        if del2:
            total_positive_captured_reviews.append(text[i])
            #print(token_lemma)
            # lemmatized_words = [lemmatizer.lemmatize(word[0], pos=word[1]) for word in pos_token]
            #text[i][j] = token_lemma

threads = []
dict_lock = Lock()

for extn in review_dict:
    if extn == 'no-script-suite-lite' or extn == 'bitwarden-free-password-m': 
        continue
    else:
        print(extn)
        threads.append(Thread(target=run, args=(extn, review_dict, dict_lock)))

for extn in noscript_dict:
    if extn == 'noscript': 
        print(extn)
        threads.append(Thread(target=run, args=(extn, noscript_dict, dict_lock)))        

for t in threads:
    print("starting threads")
    t.start()

for t in threads:
    print("joining threads back in")
    t.join()

# print("total -ve reviews captured: ", total_negative_captured_reviews)
# print("total +ve reviews captured: ", total_positive_captured_reviews)

with open("freq_analysis.txt", "w") as f:
    f.write('negative:\n')
    f.write(str(freq_analysis_neg))
    f.write('\n')
    f.write('positive:\n')
    f.write(str(freq_analysis_pos))
f.close()

with open('negative_rev.pickle', 'wb') as f:
    pickle.dump(total_negative_captured_reviews, f)
f.close()

with open('positive_rev.pickle', 'wb') as f:
    pickle.dump(total_positive_captured_reviews, f)
f.close()

pretty_print("positive_sentiment_review_set.txt", positive_sentiment_set)
pretty_print("usability_classification_new.txt", super_classification)
# pretty_print("noscript_positive.txt", positive_sentiment_set)
# pretty_print("noscript_classification.txt", super_classification)











#########################################################################

# initial corpora of words
# keywords = {
#     'block': ['block', 'not block', 'prevent', 'protect', 'secure'],
#     'ads': ['ads', 'popup', 'pop-up', 'malvertising', 'CDN', 'content delivery', 'spyware', 'adware'],
#     'fingerprinting': ['fingerprint'],
#     'break':['break', 'website', 'webpage', 'slow', 'rendering', 'error', 'bug', 'stop', 'not work', 'slow rendering', 'stop work', 'dont work'],
#     'tracking': ['3rd', 'third', 'party', 'tracking', 'icons', 'javascript', 'private'],
#     'manual': ['turn', 'off', 'features', 'turn off'],
#     'filter': ['add', 'remove', 'filter', 'list', 'allowlist', 'snippet', 'xPath', 'whitelist', 'blocklist'],
#     'update': ['automatic', 'update'],
#     'config': ['default', 'config', 'configuration'],
#     'priv_policy': ['CSP', 'javascript', 'memory', 'storage', 'privacy', 'policy', 'privacy policy', 'consent', 'PII', 'right', 'information', 'compliance', 'security', 'notification', 'legal', 'content security policy', 'age'],
#     'compatibility': ['browser', 'compatible', 'extension', 'website'],
# #    'remove': ['remove', 'button', 'rid off', 'icon', 'disable'],
#     'data': ['permission', 'protection', 'data', 'encrypt'],
#     'performance': ['efficient', 'fast', 'lite', 'light']
# }


