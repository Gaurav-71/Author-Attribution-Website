import io, os, sys, types
import pandas as pd
# import seaborn as sns
import nltk
import warnings
warnings.filterwarnings("ignore")
import pickle
import bz2
import sys
from sklearn.model_selection import train_test_split

# from sklearn.metrics import classification_report

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

# df_profile['authors'] = Profile_Auth_File.keys()
# df_profile['instance'] = Profile_Auth_File.values()
# print(df_instance.head())
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
    #result.append(''.join([i for i in list_authors if not i.isdigit() ]))
    result.append(list_authors)
new_df['clean_authors'] = result
df_temp = new_df
del df_temp['authors']
df_temp.to_csv("compression_data/Dataset.csv")
y = df_temp['clean_authors']
X = df_temp['instances']
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2, random_state=42)
A=list(X_test) #files
B=list(y_test)#author names
#--------------------------------------------------------------#
comp_accuracy =0.91
#accuracy tested in testing enviroment, please refer report for accuracy 
def compression(singleFile):
   
    bzip_pred = []
    bzip_compress_train={}
    bzip_concat={}
    compressionLevel=9
    for author, data in zip(y, X):
        bzip_compress_train[author] = bz2.compress(bytes(data, 'utf-8'), compressionLevel)
        bzip_concat[author] = data+str(singleFile)
    bzip_concat_comp={}
    bzip_singleFileComp = bz2.compress(bytes(singleFile, 'utf-8'))
        #compress concatinated file 
    for i,j in bzip_concat.items():
        bzip_concat_comp[i] = bz2.compress(bytes(j, "utf-8"))
        #calculate ncd values
    bzip_ncd_values={}
    for i,j in bzip_compress_train.items():
        bzip_ncd_values[i] = (len(bzip_concat_comp[i]) - min(len(bzip_compress_train[i]), len(bzip_singleFileComp)))/max(len(bzip_compress_train[i]), len(bzip_singleFileComp))

    tp=next(iter(dict(sorted(bzip_ncd_values.items(), key=lambda item: item[1]))))
    pred = ''.join([i for i in tp if not i.isdigit()])
    bzip_pred.append(pred)
    #print(bzip_pred)
    return bzip_pred[0]
#pickle.dump(compression(singleFile),open('compression.pkl', 'wb'))
#cmp = compression(*args)
# print(compression(str))