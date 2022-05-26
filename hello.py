from crypt import methods
from unicodedata import name
from unittest import result
from flask import Flask, render_template
from flask import Flask, request, render_template
from requests import request
import requests
app = Flask(__name__)

@app.route("/", methods = ["GET" , "POST"] )
def my_page():
    return render_template("index.html" )

@app.route("/result", methods = ["POST"])

def output():
    text = request.form['text']

    return render_template("result.html" , result = text)
