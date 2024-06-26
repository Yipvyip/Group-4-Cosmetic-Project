from flask import Flask, render_template, request
import google.generativeai as palm
import replicate
import os
from flask import Markup

flag = 1
name = ""

makersuite_api = os.getenv("MAKERSUITE_API_TOKEN")
palm.configure(api_key=makersuite_api)

model = {"model" : "models/chat-bison-001"}
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    global flag, name
    print("flag", flag)
    if flag == 1:
        name = request.form.get("q")
        flag = 0
    return(render_template("main.html",r=name))

@app.route("/generate_text",methods=["GET","POST"])
def generate_text():
    return(render_template("generate_text.html"))

@app.route("/text_result_makersuite",methods=["GET","POST"])
def text_result_makersuite():
    q = request.form.get("q")
    r = palm.chat(**model, messages=q)
    return(render_template("text_result_makersuite.html",r=r.last))

@app.route("/generate_image",methods=["GET","POST"])
def generate_image():
    return(render_template("generate_image.html"))

@app.route("/image_result",methods=["GET","POST"])
def image_result():
    q = request.form.get("q")
    r = replicate.run("stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
      input = {"prompt":q}
    )
    return(render_template("image_result.html",r=r[0]))

@app.route("/end",methods=["GET","POST"])
def end():
    global flag
    flag = 1
    return(render_template("index.html"))

if __name__ == "__main__":
    app.run()
