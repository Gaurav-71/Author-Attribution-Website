import warnings
import nltk
import pandas as pd
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

nltk.download('punkt')

warnings.filterwarnings("ignore")


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

df_profile['authors'] = Profile_Auth_File.keys()
df_profile['instance'] = Profile_Auth_File.values()

#stop_words_list = "C://Users/RAVIKUMAR/PycharmProjects/Authorship_Attribution_Instance/Data_2/new_stop_words.txt"

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
#print(len(set(y)),len(set(new_df['clean_authors'])))
# 80-20 splitting the dataset (80%->Training and 20%->Validation)
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2, random_state=123)

#feature extracting from clean text
one_word=TfidfVectorizer(analyzer="word", ngram_range=(1,1),max_features=2000, binary=False).fit(X_train)
one_char=TfidfVectorizer(analyzer="char", ngram_range=(1,1),max_features=2000, binary=False).fit(X_train)
two_word=TfidfVectorizer(analyzer="word", ngram_range=(2,2),max_features=2000, binary=False).fit(X_train)
two_char=TfidfVectorizer(analyzer="char", ngram_range=(2,2),max_features=2000, binary=False).fit(X_train)
three_word=TfidfVectorizer(analyzer="word", ngram_range=(3,3),max_features=2000, binary=False).fit(X_train)
three_char=TfidfVectorizer(analyzer="char", ngram_range=(3,3),max_features=2000, binary=False).fit(X_train)
four_word=TfidfVectorizer(analyzer="word", ngram_range=(4,4),max_features=2000, binary=False).fit(X_train)
four_char=TfidfVectorizer(analyzer="char", ngram_range=(4,4),max_features=2000, binary=False).fit(X_train)
five_word=TfidfVectorizer(analyzer="word", ngram_range=(5,5),max_features=2000, binary=False).fit(X_train)
five_char=TfidfVectorizer(analyzer="char", ngram_range=(5,5),max_features=2000, binary=False).fit(X_train)

#calling each tf-idf vectors and union
UnionFeater = FeatureUnion([
                        ("word_1",one_word),("word_2",two_word),("word_3",three_word),("word_4",four_word),
                           ("word_5",five_word),
     ("char_1",one_char),("char_2",two_char),("char_3",three_char),("char_4",four_char),
                           ("char_5",five_char)
                           ] )

#TF-IDF vectorizer
vector_train = UnionFeater.transform(X_train)
vector_test = UnionFeater.transform(X_test)

SVM =SVC(kernel='linear')
SVM = SVM.fit(vector_train, y_train)

#print("SVM Training Accuracy        :",SVM.score(vector_train, y_train))
#print("SVM Testing Acuuracy         : ",SVM.score(vector_test, y_test))
predictions = SVM.predict(vector_test)
ngram_accuracy = SVM.score(vector_test, y_test)
#print(classification_report(y_test, predictions))
# user_input = input("Enter the text")
# t = UnionFeater.transform([user_input])
# tst = SVM.predict(t)[0]
# print(tst)
vector = UnionFeater.fit(X_train)
pickle.dump(vector,open('ngram_vect.pkl', 'wb'))
pickle.dump(SVM, open('ngram_attribution.pkl','wb'))