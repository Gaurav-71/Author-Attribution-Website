import pickle
import os
import sys
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import ngram_model as  nm
import compression_method as cm
from flask import Flask, request, render_template, jsonify
#Initialize the flask App
app = Flask(__name__)
ngram_clf = pickle.load(open('ngram_attribution.pkl','rb'))
ngram_loaded_vec = pickle.load(open("ngram_vect.pkl", "rb"))

@app.route('/test', methods = ['GET', 'POST'])
def test():
    if request.method == 'GET':
        return jsonify ({"response": "Get Request called"})
    elif request.method == 'POST':
        req_Json = request.json
        name = req_Json['name']
        return jsonify({"response": "Hi" +name})

@app.route('/ngram', methods = ['GET', 'POST'])
def ngram():
    if request.method == 'POST':
        input_text = request.form['kannada_text']
        txt_vc = ngram_loaded_vec.transform([input_text])
        result_pred = ngram_clf.predict(txt_vc)
        accuracy = nm.ngram_accuracy
        return jsonify(
            {
                "Author_Name ":'{}'.format(result_pred[0]),
                "Accuracy ":str(accuracy),
                "Model ": "ngram model"
            }
        )

        #return render_template('predict_author.html', prediction_text='predicted authors :{}'.format(result_pred[0]))
@app.route('/compression', methods = ['GET', 'POST'])
def compression():
    if request.method == 'POST':
        user_text = request.form['kannada_text']
        result  = cm.compression(user_text)
        accuracy = cm.comp_accuracy
        return jsonify(
            {
                "Author_Name ":'{}'.format(result),
                "Accuracy ":str(accuracy),
                "Model ": "compression Model (bzip)"
            }

        )
        # return render_template('predict_author.html', accuracy ="  Accuracy:"+str(accuracy), prediction_text='predicted authors :{}'.format(result))
    

@app.route('/lexical', methods = ['GET', 'POST'])
def lexical():
    if request.method == 'POST':
        pass
  

@app.route('/emotion_poly', methods = ['GET', 'POST'])
def emotion_poly():
    if request.method == 'POST':
        author_name = "" 
        accuracy  = ""
        return jsonify({"response":"emotion_poly called"})
    
if __name__ == "__main__":
    app.run(debug=True, port = 9090)