import pickle
import nltk
import string
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

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

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('JJ'):
        return wordnet.ADJ
    elif treebank_tag.startswith('VB'):
        return wordnet.VERB
    elif treebank_tag.startswith('NN'):
        return wordnet.NOUN
    elif treebank_tag.startswith('RB'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

review_dict = load_dict('threaded_output/review_t.pickle')

text = review_dict['decentraleyes'][1]
remove_elements(text, [])
stopwords = load_custom_stopwords()
lemmatizer = WordNetLemmatizer()

for i in range(len(text)):
    text[i] = sent_tokenize(text[i])
    for j in range(len(text[i])):
        punc_remove = text[i][j].translate(str.maketrans('', '', string.punctuation))
        token_lst = word_tokenize(punc_remove)
        token_lst = [words for words in token_lst if words.casefold() not in stopwords]
        token_postag = nltk.pos_tag(token_lst)
        token_lemma = []
        for tuples in token_postag:
            if tuples[1] == "NNP" or tuples[1] == "NNPS":
                token_lemma.append(tuples[0].lower())
            else:
                token_lemma.append(lemmatizer.lemmatize(tuples[0].lower(), pos=get_wordnet_pos(tuples[1])))

        print(token_lemma)
        # lemmatized_words = [lemmatizer.lemmatize(word[0], pos=word[1]) for word in pos_token]
        text[i][j] = token_lemma