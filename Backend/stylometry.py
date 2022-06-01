import pickle
from lexical_feature_extracting import creat_bin_file
import os.path

file_exists = os.path.exists('lexical_features.pkl')
# print(file_exists)

if(file_exists == True):
    extracted_features = pickle.load(open("lexical_features.pkl", "rb"))
    print(extracted_features.keys())

else:
   vectors, authors =  creat_bin_file()



