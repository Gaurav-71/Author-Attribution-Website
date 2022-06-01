import pickle
import os
import sys
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import ngram_model as  nm
import compression_method as cm
from flask import Flask, request, render_template
#Initialize the flask App
app = Flask(__name__)
clf = pickle.load(open('attribution.pkl','rb'))
loaded_vec = pickle.load(open("vect.pkl", "rb"))



#default page of our web-app
@app.route('/')
def home():
    return render_template('homepage.html')
@app.route('/index')
def index():
    return render_template('predict_author.html')

@app.route('/login')
def login():
    return render_template('upload_file.html')
    
#To use the predict button in our web-app
@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        if request.form.get('submit_button') == 'ngram':
            result = request.form['kannada_text']
            #print(result)
            txt_vc = loaded_vec.transform([result])
            result_pred = clf.predict(txt_vc)
            return render_template('predict_author.html', prediction_text='predicted authors :{}'.format(result_pred[0]))
        elif request.form.get('submit_button') == 'comp':
            user_text = request.form['kannada_text']
            result  = cm.compression(user_text)
            accuracy = nm.ngram_accuracy
            return render_template('predict_author.html', accuracy ="  Accuracy:"+str(accuracy), prediction_text='predicted authors :{}'.format(result))
        
        elif request.form.get('goback_button') == 'goback':
            return render_template('homepage.html')

#upload files 
@app.route('/upload',methods=['POST'])
def upload():
    if request.method=='POST':
        file_data = request.files.getlist('upload_file')
        
        author_name = request.form['author_name']
        script_dir = os.path.dirname(__file__)
        rel_path = "pending_author_files"
        author_directory = author_name
        abs_file_path = os.path.join(script_dir, rel_path)
        path = os.path.join(abs_file_path, author_directory)
        try:
            os.mkdir(path)
            
        except :
            file_already_present = "This file already submitted! please try other files"
        for file in file_data:
            file.save(os.path.join(path, secure_filename(file.filename)))
        print("Directory '% s' created" % author_directory)
        return render_template('upload_file.html', file_uploded_status ="files uploaded Successfully!")
if __name__ == "__main__":
    app.run(debug=True)

