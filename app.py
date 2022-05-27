from crypt import methods
from flask import Flask, redirect, render_template , request, url_for
from pyrfc3339 import generate

app = Flask(__name__)

@app.route("/", methods = ["GET" , "POST"] )
def my_form():
    if request.method == "POST":
        t = request.form["text"]
        return redirect(url_for("my_form_post" , generated_text =  t  ))
    else:
        return render_template("index.html" )


@app.route("/result/<generated_text>", methods = ["GET" ])
def my_form_post(generated_text):
    return render_template("result.html" , result = generated_text)

if __name__ == "__main__" :
    app.run(debug= True)