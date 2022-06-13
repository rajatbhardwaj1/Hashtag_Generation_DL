from crypt import methods
from flask import Flask, redirect, render_template , request, url_for
from pyrfc3339 import generate
from keybert import KeyBERT

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
kw_model = KeyBERT(model="all-MiniLM-L6-v2")
keywords = kw_model.extract_keywords(doc)

app = Flask(__name__)

@app.route("/", methods = ["GET" , "POST"] )
def my_form():
    if request.method == "POST":
        doc = request.form["text"]
        keywords = kw_model.extract_keywords(doc)
        t = ""
        for word , cossim  in keywords:
            t = t + "#" + word 

        if t== "":
            t = "Error404 : No text found! "
        return redirect(url_for("my_form_post" , generated_text =  t  ))
    else:
        return render_template("index.html" )


@app.route("/result/<generated_text>", methods = ["GET" ])
def my_form_post(generated_text):
    return render_template("result.html" , result = generated_text)

if __name__ == "__main__" :
    app.run(debug= True)