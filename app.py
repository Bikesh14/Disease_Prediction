from functools import reduce
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
)
import predengine

from transcribingmedicalrecords import summarizer 
app=Flask(__name__)

@app.route("/",  methods=("GET", "POST"))
def index():
    if request.method=="POST":

        # symptom1, symptom2, symptom3, symptom4, symptom5, symptom6=request.form['symptom1'], request.form['symptom2'], request.form['symptom3'], request.form['symptom4'], request.form['symptom5'], request.form['symptom6']

        symptoms_list=list(request.form.values())
        # symptoms_list.append(symptom1)
        print(symptoms_list)

        symptoms_str = reduce(lambda a, b : a+ "," +str(b), symptoms_list)

        print("-----------------------------")
        prediction=predengine.predict_disease(symptoms_str)
        print(prediction)
        print(type(prediction))

        prediction_str=" ".join(prediction)
        return render_template('index.html', prediction=prediction_str, symptom1=symptoms_list[0], symptom2=symptoms_list[1], symptom3=symptoms_list[2], symptom4=symptoms_list[3], symptom5=symptoms_list[4], symptom6=symptoms_list[5])

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

