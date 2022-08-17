from __future__ import division, unicode_literals
from argparse import Namespace
from crypt import methods
import hashlib
from unittest import result
from flask import Flask, redirect, render_template , request, url_for
from pyrfc3339 import generate
import yake
from  GeneratorModel import GeneratorModel
import argparse
import torch
import pandas as pd
from transformers import AutoTokenizer, BartForConditionalGeneration
#!/usr/bin/env python
import argparse

from onmt.translate.Translator import make_translator


import onmt.io
import onmt.translate
import onmt
import onmt.ModelConstructor
import onmt.modules
import onmt.opts
import os
import time
import re
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
# generator = GeneratorModel(Namespace(beam_size=5, decoder_early_stopping=True, decoder_min_length=1, length_penalty=0.6, model_path='hashtag_model_final.pt', no_repeat_ngram_size=3), "hashtag_model_final.pt")

kw_extractor = yake.KeywordExtractor(top=10, stopwords=None)
app = Flask(__name__)

@app.route("/", methods = ["GET" , "POST"] )
def my_form():
    t = ""
 
    if request.method == "POST":
        doc = request.form["text"]
        doc = doc.lower()
        option = request.form['test']
        if option == "yake":
            hashtaglist = kw_extractor.extract_keywords(doc)
            for hashtag, cs in hashtaglist:
                t = t + " #" + hashtag

        # if option == "stance":
        #     t = generator.generate(doc)
        if option == "microblog":
            file1 = open("helper.txt" , "w")
            file1.write(doc)
            file1.close()
            opt = Namespace(alpha=0.0, attn_debug=False, batch_size=64, beam_size=30, beta=-0.0, block_ngram_repeat=0, conversation='commentsfile.txt', coverage_penalty='none', data_type='text', dump_beam='', dynamic_dict=False, gpu=0, ignore_when_blocking=[], length_penalty='none', log_file='', max_length=10, max_sent_length=None, min_length=0, model='sh/saved_models/Twitter_BiAttEncoder_rnn_200emb_seed100_acc_53.76_ppl_34.21_e9.pt', n_best=20, output='outputfile.txt', replace_unk=False, report_bleu=False, report_rouge=False, sample_rate=16000, share_vocab=False, src='helper.txt', src_dir='', stepwise_penalty=False, tgt="hashtags.txt", verbose=False, window='hamming', window_size=0.02, window_stride=0.01)
            translator = make_translator(opt, report_score=True)
            translator.translate(opt.src_dir, opt.src, opt.conversation, opt.tgt, opt.batch_size, opt.attn_debug)







        if t== "":
            t = "No Hashtags Generated!! Please enter a valid text."
        
    return render_template("index.html",  result1 = t )


@app.route("/result/<generated_text>", methods = ["GET" ])
def my_form_post(generated_text):
    return render_template("result.html" , result = generated_text)

if __name__ == "__main__" :
    app.run(debug= True)