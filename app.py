from flask import Flask, render_template, request
import pickle
import pandas as pd 
import numpy as np
import predengine


app=Flask(__name__)

@app.route('/')
def index():
    symptoms='itching,skin_rash,chills,shivering'
    prediction=predengine.predict_disease(symptoms)

    return render_template('index.html', prediction=prediction)
    # return render_template('index.html')
    


# @app.route('/', methods=['POST'])
# def disease_predict():
    # symptoms=[x for x in request.form.values()]
    # features=['itching,skin_rash,chills,shivering']
   





if __name__=="__main__":
    app.run(debug=True)

