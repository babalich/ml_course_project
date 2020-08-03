
import numpy as np
import flask
import io
import dill
import os
import urllib
import json

from flask_wtf import FlaskForm
from flask import Flask, render_template, redirect, url_for, request

from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import DataRequired


app = flask.Flask(__name__)
model = None

class ClientDataForm(FlaskForm):
    description = StringField('text', validators=[DataRequired()])

def load_model():
    global model
    with open('./models/model_trained.dill', 'rb') as file:
        model = dill.load(file)

load_model()

app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)

@app.route("/")
def index():
    return render_template('index.html')


def get_prediction(text):
    body = {"text": text}
    print('get_pred',body)
    myurl = "http://localhost:5000/api/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    # print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']

@app.route('/predicted/<response>')
def predicted(response):
    #response = json.loads(response)
    print(response)
    text = request.args.get('text')
    message = ''
    if response[0] == 0:
        message = 'not toxic'
    else:
        message = 'toxic'
    return render_template('predicted.html', response=message, text=text)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data["text"] = [request.form.get("text")]
        print(data)
        try:
            response = str(get_prediction(data['text']))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response, text=data['text']))
    return render_template('form.html', form=form)



if __name__== '__main__':
    print('prilojenie start')
    port = int(os.environ.get('PORT', 5001))
    app.run(host='127.0.0.1', port=port, debug=True)



pass