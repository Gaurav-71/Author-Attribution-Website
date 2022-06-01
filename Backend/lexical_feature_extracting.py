import collections as coll
import math
import pickle
import string
import numpy as np
from nltk.corpus import cmudict
import pandas as pd
import seaborn as sns

from nltk.tokenize import word_tokenize, sent_tokenize
cmuDictionary = None
import os 
from os import path
path_of_Stopword="Dataset\stopwords.txt"
file_path = path.relpath(path_of_Stopword);
file = open(file_path, encoding="utf8")
stop_words=file.read()
from nltk.tokenize import sent_tokenize
import nltk
#nltk.download('averaged_perceptron_tagger')
from sklearn.preprocessing import StandardScaler
# removing stop words plus punctuation.



def Avg_wordLength(str):
    norm=[]
    str.translate(string.punctuation)
    tokens = word_tokenize(str)
    st = [",", ".", "'", "!", '"', "#", "$", "%", "&", "(", ")", "*", "+", "-", ".", "/", ":", ";", "<", "=", '>', "?",
          "@", "[", "\\", "]", "^", "_", '`', "{", "|", "}", '~', '\t', '\n']
    stop = list(stop_words)
    words = [word for word in tokens if word not in stop and word not in st]
#     print(" words",words)
#     print([len(word) for word in words])
#     print(np.average([len(word) for word in words]))
    return np.average([len(word) for word in words])


# ----------------------------------------------------------------------------


# returns avg number of characters in a sentence
def Avg_SentLenghtByCh(text):
    tokens = sent_tokenize(text)
#     print(tokens)
#     print(np.average([len(token) for token in tokens]))
    return np.average([len(token) for token in tokens])


# ----------------------------------------------------------------------------

# returns avg number of words in a sentence
def Avg_SentLenghtByWord(text):
    tokens = sent_tokenize(text)
#     print(tokens)
#     print("Avg_SentLenghtByWord ",np.average([len(token.split()) for token in tokens]))
    return np.average([len(token.split()) for token in tokens])


# -----------------------------------------------------------------------------

# COUNTS SPECIAL CHARACTERS NORMALIZED OVER LENGTH OF CHUNK
def CountSpecialCharacter(text):
    st = ["#", "$", "%", "&", "(", ")", "*", "+", "-", "/", "<", "=", '>',
          "@", "[", "\\", "]", "^", "_", '`', "{", "|", "}", '~', '\t', '\n']
    count = 0
    for i in text:
        if (i in st):
            count = count + 1
    return count / len(text)


# ----------------------------------------------------------------------------

def CountPuncuation(text):
    st = [",", ".", "'", "!", '"', ";", "?", ":", ";"]
    count = 0
    for i in text:
        if (i in st):
            count = count + 1
    return float(count) / float(len(text))


# ---------------------------------------------------------------------------

def hapaxDisLegemena(text):
    words = RemoveSpecialCHs(text)
    count = 0
    # Collections as coll Counter takes an iterable collapse duplicate and counts as
    # a dictionary how many equivelant items has been entered
    freqs = coll.Counter()
    freqs.update(words)
    for word in freqs:
        if freqs[word] == 2:
            count += 1

    h = count / float(len(words))
    S = count / float(len(set(words)))
    return S, h


# ---------------------------------------------------------------------------

# c(w)  = ceil (log2 (f(w*)/f(w))) f(w*) frequency of most commonly used words f(w) frequency of word w
# measure of vocabulary richness and connected to zipfs law, f(w*) const rak kay zips law say rank nikal rahay hein
def AvgWordFrequencyClass(text):
    words = RemoveSpecialCHs(text)
    # dictionary comprehension . har word kay against value 0 kardi
    freqs = {key: 0 for key in words}
    for word in words:
        freqs[word] += 1
    maximum = float(max(list(freqs.values())))
    return np.average([math.floor(math.log((maximum + 1) / (freqs[word]) + 1, 2)) for word in words])


# --------------------------------------------------------------------------
# TYPE TOKEN RATIO NO OF DIFFERENT WORDS / NO OF WORDS
def typeTokenRatio(text):
    words = word_tokenize(text)
    return len(set(words)) / len(words)


# we can convert into log because we are only comparing different texts
def BrunetsMeasureW(text):
    words = RemoveSpecialCHs(text)
    a = 0.17
    V = float(len(set(words)))
    N = len(words)
    B = (V - a) / (math.log(N))
    return B


# ------------------------------------------------------------------------
def RemoveSpecialCHs(text):
    text = word_tokenize(text)
    st = [",", ".", "'", "!", '"', "#", "$", "%", "&", "(", ")", "*", "+", "-", ".", "/", ":", ";", "<", "=", '>', "?",
          "@", "[", "\\", "]", "^", "_", '`', "{", "|", "}", '~', '\t', '\n']

    words = [word for word in text if word not in st]
    return words


# Shannon and sympsons index are basically diversity indices for any community
def ShannonEntropy(text):
    words = RemoveSpecialCHs(text)
    lenght = len(words)
    freqs = coll.Counter()
    freqs.update(words)
    arr = np.array(list(freqs.values()))
    distribution = 1. * arr
    distribution /= max(1, lenght)
    import scipy as sc
    H = sc.stats.entropy(distribution, base=2)
    return H


# ------------------------------------------------------------------
def SimpsonsIndex(text):
    words = RemoveSpecialCHs(text)
    freqs = coll.Counter()
    freqs.update(words)
    N = len(words)
    n = sum([1.0 * i * (i - 1) for i in freqs.values()])
    D = 1 - (n / (N * (N - 1)))
    return D


# -----------------------------------------------------------------
def dale_chall_readability_formula(text, NoOfSectences):
    words = RemoveSpecialCHs(text)
    difficult = 0
    adjusted = 0
    NoOfWords = len(words)
    with open('dale-chall.pkl', 'rb') as f:
        fimiliarWords = pickle.load(f)
    for word in words:
        if word not in fimiliarWords:
            difficult += 1
    percent = (difficult / NoOfWords) * 100
    if (percent > 5):
        adjusted = 3.6365
    D = 0.1579 * (percent) + 0.0496 * (NoOfWords / NoOfSectences) + adjusted
    return D


# ------------------------------------------------------------------


def Each_sentence(sequence):
    sequence = sent_tokenize(sequence)
    return sequence
def FeatureExtration(text):
    # cmu dictionary for syllables
    global cmuDictionary
    cmuDictionary = cmudict.dict()
    All_sentences_per_instance = Each_sentence(text)
    vector = []
    for line in All_sentences_per_instance:
        feature = []
        meanwl = (Avg_wordLength(line))
        feature.append(meanwl)
        meansl = (Avg_SentLenghtByCh(line))
        feature.append(meansl)
        mean = (Avg_SentLenghtByWord(line))
        feature.append(mean)
        means = CountSpecialCharacter(line)
        feature.append(means)
        p = CountPuncuation(line)
        feature.append(p)
        TTratio = typeTokenRatio(line)
        feature.append(TTratio)
        vector.append(feature)
    return vector

Profile_Auth_File={}
instanc_Auth_file = {}
count  = 0
script_dir = os.path.dirname(__file__)
rel_path = "Data_text_files"
abs_file_path = os.path.join(script_dir, rel_path)
basepath = abs_file_path #"C:/Users/RAVIKUMAR/Desktop/Data_text_files"
for dir_name in os.listdir(basepath):
    dir_path = os.path.join(basepath, dir_name)
    if not os.path.isdir(dir_path):
        continue
    with open(os.path.join(dir_path, dir_name+'.txt') , 'w', encoding='utf-8') as outfile:
        files = []
        instance = []
        for file_name in os.listdir(dir_path):
            count +=1
            if file_name.endswith('.txt'):
                instance.clear()
                with open(os.path.join(dir_path, file_name), encoding='utf-8') as readfile:
                    #files.append(file_name)
                    instance.append(readfile.read())
                    files.append(readfile.read())
                    buffer = instance
                instanc_Auth_file[dir_name+str(count)] = str(list(set(buffer)))
                with open(os.path.join(dir_path, file_name), encoding='utf-8') as readfile:
                    files.append(readfile.read())
    Profile_Auth_File[dir_name] = files


df_instance = pd.DataFrame()
df_profile = pd.DataFrame()

df_instance['authors'] = instanc_Auth_file.keys()
df_instance['instance'] = instanc_Auth_file.values()
# print(df_instance)
script_dir = os.path.dirname(__file__)
rel_path = "Dataset/stopwords.txt"
abs_file_path = os.path.join(script_dir, rel_path)
stopword=[]

with open(abs_file_path, encoding='utf-8') as file:
    reader=file.read()
    reader = [reader.split()]
    stopword = sum(reader, [])

pp = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~0123456789a-z'
def text_process(text):
    nopunct = "".join([char for char in text if char not in pp])
    tokens = nltk.word_tokenize(nopunct)
    nopunct = " ".join([word for word in tokens if word not in stopword])
    return nopunct
instance_with_author = {}
for  i, j in zip(df_instance['authors'], df_instance['instance']):
    instance_with_author[i]=text_process(j)
new_df = pd.DataFrame()
new_df['authors'] = instance_with_author.keys()
new_df['instances'] = instance_with_author.values()


ep_row = new_df.index[new_df['instances']==""].tolist()
new_df=new_df.drop(new_df.index[ep_row])

clean_authors = list(new_df['authors'])
result = []
for list_authors in clean_authors:
    list_authors = list_authors.replace("zz_", '')
    result.append(''.join([i for i in list_authors if not i.isdigit() ]))
new_df['clean_authors'] = result
df_temp = new_df
del df_temp['authors']
df_temp.to_csv("Dataset/Dataset.csv")
y = df_temp['clean_authors']
X = df_temp['instances']
print(len(set(y)),len(set(new_df['clean_authors'])))


author_fvs={}
feature_vectors=[]
# def feature_return():
#     for (text,author) in zip(X, y):
#         # author_fvs[author]=FeatureExtration(text)
#         feature_vectors.append(FeatureExtration(text))
#     return feature_vectors,y

print("successfully extracted all the features\n \n ")
def creat_bin_file():
    for (text,author) in zip(X, y):
        # author_fvs[author]=FeatureExtration(text)
        feature_vectors.append(FeatureExtration(text))
    pickle.dump(feature_vectors,open('lexical_features.pkl', 'wb'))
    return feature_vectors,y