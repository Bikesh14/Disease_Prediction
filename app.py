from urllib import request
from flask import Flask, render_template, url_for


app=Flask(__name__)



@app.route("/", methods=("GET", "POST"))
def transcribe():
    string = ''

    if request.method == 'POST':
        return render_template('index.html')

    return render_template('index.html')

