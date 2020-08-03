
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
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)
model = None




def load_model():
    global model
    with open('./models/model_trained.dill', 'rb') as file:
        model = dill.load(file)

load_model()

@app.route('/', methods=['GET'])
def general():
    return render_template('form.html')


@app.route("/api/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        text = ''
        request_json = flask.request.get_json()

        if request_json['text']:
           text = request_json['text']

        pred = model.predict(text)

        data["predictions"] = pred[0]
        data["success"] = True


    return flask.jsonify(data)

def get_prediction(text):
    body = {"text": text}
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
    text = request.args.get('text')
    return render_template('form.html', response=response, text=text)

class ClientDataForm(FlaskForm):
    description = StringField('text', validators=[DataRequired()])

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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)



pass