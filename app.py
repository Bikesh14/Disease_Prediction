from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
)

from transcribingmedicalrecords import summarizer 
app=Flask(__name__)



@app.route("/", methods=("GET", "POST"))
def transcribe():
    string = ''
    keywords = list()
    if request.method == 'POST':
        transcription = request.form['transcription']
        keywords = summarizer(transcription)
        print(keywords)
        return render_template('summarizer.html', hello='world')

    return render_template('summarizer.html')

