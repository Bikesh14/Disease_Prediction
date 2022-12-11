from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
)
import predengine

from transcribingmedicalrecords import summarizer 
app=Flask(__name__)

@app.route("/",  methods=("GET", "POST"))
def index():
    # symptoms='itching,skin_rash,chills,shivering'
    if request.method=="POST":
        symptoms=request.form['prescription']
        prediction=predengine.predict_disease(symptoms)
        return render_template('index.html', prediction=prediction)

    return render_template('index.html')




# @app.route("/", methods=("GET", "POST"))
# def transcribe():
#     string = ''
#     keywords = list()
#     if request.method == 'POST':
#         transcription = request.form['transcription']
#         keywords = summarizer(transcription)
#         print(keywords)
#         return render_template('summarizer.html', hello='world')

#     return render_template('summarizer.html')



if __name__=="__main__":
    app.run(debug=True)

