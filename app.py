from argparse import Namespace
from crypt import methods
from unittest import result
from flask import Flask, redirect, render_template , request, url_for
from pyrfc3339 import generate
import yake
from  GeneratorModel import GeneratorModel
import argparse
import torch
import pandas as pd
from transformers import AutoTokenizer, BartForConditionalGeneration

doc = """
         Supervised learning is the machine learning task of learning a function that
         maps an input to an output based on example input-output pairs. It infers a
         function from labeled training data consisting of a set of training examples.
         In supervised learning, each example is a pair consisting of an input object
         (typically a vector) and a desired output value (also called the supervisory signal).
         A supervised learning algorithm analyzes the training data and produces an inferred function,
         which can be used for mapping new examples. An optimal scenario will allow for the
         algorithm to correctly determine the class labels for unseen instances. This requires
         the learning algorithm to generalize from the training data to unseen situations in a
         'reasonable' way (see inductive bias).
      """
generator = GeneratorModel(Namespace(beam_size=5, decoder_early_stopping=True, decoder_min_length=1, length_penalty=0.6, model_path='hashtag_model_final.pt', no_repeat_ngram_size=3), "hashtag_model_final.pt")

kw_extractor = yake.KeywordExtractor(top=10, stopwords=None)
app = Flask(__name__)

@app.route("/", methods = ["GET" , "POST"] )
def my_form():
    t = ""

    if request.method == "POST":
        t = ""
        doc = request.form["text"]
        doc = doc.lower()
        keywords = kw_extractor.extract_keywords(doc)
        for word , cs in keywords:
            t = t + "#"+word+" " 

        if t== "":
            t = "No Hashtags Generated!! Please enter a valid text."
        
    return render_template("index.html",  result1 = t )


@app.route("/result/<generated_text>", methods = ["GET" ])
def my_form_post(generated_text):
    return render_template("result.html" , result = generated_text)

if __name__ == "__main__" :
    app.run(debug= True)