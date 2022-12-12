from functools import reduce
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
)
import predengine

import json
with open('symptom_Description.txt') as f1:
    s_d = f1.read()
symptom_description=json.loads(s_d)

with open('symptom_precaution.txt') as f2:
    s_p = f2.read()
symptom_precaution=json.loads(s_p)
    

from transcribingmedicalrecords import summarizer 
app=Flask(__name__)

@app.route("/",  methods=("GET", "POST"))
def index():
    if request.method=="POST":


        symptoms_list=list(request.form.values())
        print(symptoms_list)

        symptoms_str = reduce(lambda a, b : a+ "," +str(b), symptoms_list)

        print("-----------------------------")
        prediction=predengine.predict_disease(symptoms_str)
        print(prediction)
        print(type(prediction))

        prediction_str=" ".join(prediction)
        print()
        
        description= symptom_description[prediction_str]
        precaution= symptom_precaution[prediction_str]

        return render_template('index.html', prediction=prediction_str, description=description, precaution=precaution, symptom1=symptoms_list[0], symptom2=symptoms_list[1], symptom3=symptoms_list[2], symptom4=symptoms_list[3], symptom5=symptoms_list[4], symptom6=symptoms_list[5])

    return render_template('index.html')




@app.route("/summarize", methods=("GET", "POST"))
def transcribe():
    string = ''
    keywords = list()
    if request.method == 'POST':
        transcription = request.form['transcription']
        keywords = summarizer(transcription)
        print(keywords)
        return render_template('summarizer.html', hello='world')

    return render_template('summarizer.html')



if __name__=="__main__":
    app.run(debug=True)

