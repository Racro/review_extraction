import pickle
import string
import sys
import random

from threading import Thread, Lock

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
    'ads': ['popup', 'pop-up', 'malvertising', 'cdn', 'content delivery', 'spyware', 'adware'],
    'fingerprinting': ['fingerprint'],
    'break':['break', 'broke', 'rendering', 'error', 'bug', 'stop', 'access', 'reload', 'load'],
    'tracking': ['3rd', 'third', 'party', 'tracking', 'icons', 'javascript', 'private'],
    'manual': ['manual', 'off', 'features', 'turn off'],
    'filter': ['remove', 'filter', 'list', 'allowlist', 'snippet', 'xpath', 'whitelist', 'blocklist', 'blacklist'],
    'update': ['automatic', 'update'],
    'config': ['default', 'config', 'configuration'],
    'priv_policy': ['csp', 'memory', 'storage', 'privacy', 'policy', 'consent', 'pii', 'information', 'compliance', 'security', 'notification', 'content security policy'],
    'compatibility': ['browser', 'compatible', 'extension', 'sites'], # adblock -> remove sites
#    'remove': ['remove', 'button', 'rid off', 'icon', 'disable'],
    'data': ['permission', 'protection', 'data', 'encrypt'],
    'performance': ['efficient', 'fast', 'lite', 'light', 'slow', 'heavy', 'speed', 'memory', 'cpu']
}

topic_classification = {} # without the positive sentiment reviews, only negative sentiments with f score > 0.7

review_dict = load_dict('threaded_output/review_t.pickle')
noscript_review_dict = load_dict('noscript_t.pickle')

review_number = {}
# review_number['adblock-plus-free-ad-bloc']=100
# review_number['ublock-origin']=100
# review_number['ghostery-–-privacy-ad-blo']=100
# review_number['https-everywhere']=50
# review_number['disconnect']=50
# review_number['privacy-badger']=50
# review_number['canvas-fingerprint-defend']=20
# review_number['user-agent-switcher-for-c']=30
# review_number['scriptsafe']=20
# review_number['decentraleyes']=20
# review_number['adguard-adblocker']=100
# review_number['bitwarden-free-password-m']=0
# review_number['no-script-suite-lite']=0
# review_number['noscript']=20

review_number['adblock-plus-free-ad-bloc']=20
review_number['ublock-origin']=20
review_number['ghostery-–-privacy-ad-blo']=20
review_number['https-everywhere']=10
review_number['disconnect']=10
review_number['privacy-badger']=10
review_number['canvas-fingerprint-defend']=4
review_number['user-agent-switcher-for-c']=5
review_number['scriptsafe']=4
review_number['decentraleyes']=4
review_number['adguard-adblocker']=20
review_number['bitwarden-free-password-m']=0
review_number['no-script-suite-lite']=0
review_number['noscript']=4

for extn in review_dict:
    topic_classification[extn] = []
topic_classification['noscript'] = []
    #positive_sentiment_set[extn] = {}

def pretty_print(filename, data_str): # data_str = {'extn': {'keyword_key': [[], 0]}}
    f = open(filename, "w")
    for extn in data_str:
        f.write(str(extn)+'\n')
        f.write(str(len(data_str[extn]))+'\n')
        f.write('-'*5+'\n')
        for review in data_str[extn]:
            f.write(str(review) + '\n')
            f.write('\n')
            f.write('-'*25 + '\n')
        f.write('-'*50 + '\n')
    f.close()

def run(extn, lock):
    if review_number[extn] == 0:
        return 0
    text = review_dict[extn][1]
    text = remove_elements(text, '')
    num_reviews = len(text)
    # print('extn: ', extn)
    # print('num_reviews: ', num_reviews)
    # print('review_number: ', review_number[extn])
    random_lst = random.sample(range(1, num_reviews), review_number[extn])
    for i in random_lst: #iterating over the review set
        lower_text = text[i].lower()
        if 'support@' in lower_text or 'hi ' in lower_text or 'hello' in lower_text or '@eff.org' in lower_text: #to eleminate answers to support queries by the extn team
            lower_text = text[i+1].lower()
        while len(lower_text.split(' ')) > 5:
            lower_text = text[random.randint(1, num_reviews)].lower()
        lock.acquire()
        topic_classification[extn].append(lower_text)
        lock.release()

def run2(extn, lock):
    if extn == 'noscript':
        print(extn)
        text = noscript_review_dict[extn][1]
        remove_elements(text, [])
        num_reviews = len(text)
        random_lst = random.sample(range(1, num_reviews), review_number[extn])
        for i in random_lst: #iterating over the review set
            lower_text = text[i].lower()
            if 'support@' in lower_text or 'hi ' in lower_text or 'hello' in lower_text or '@eff.org' in lower_text: #to eleminate answers to support queries by the extn team
                lower_text = text[random.randint(1, num_reviews)].lower()
            while len(lower_text.split(' ')) > 5:
                lower_text = text[random.randint(1, num_reviews)].lower()
            lock.acquire()
            topic_classification[extn].append(lower_text)
            lock.release()

threads = []
dict_lock = Lock()

for extn in review_dict:
    print(extn)
    threads.append(Thread(target=run, args=(extn, dict_lock)))
for extn in noscript_review_dict:
    #print(extn)
    threads.append(Thread(target=run2, args=(extn, dict_lock)))

for t in threads:
    print("starting threads")
    t.start()

for t in threads:
    print("joining threads back in")
    t.join()

pretty_print("topic_classification_less_5.txt", topic_classification)
# pretty_print("usability_classification.txt", super_classification)
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

