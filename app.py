from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save("static/preds/"+uploaded_file.filename)
        with open("static/logs/log.txt", "a") as log:
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log.write(uploaded_file.filename+" - "+str(timestamp))
            log.write("\n")
            
    return redirect(url_for('home'))

@app.route("/classifica")
def classifica():
    return render_template("classifica.html")

@app.route("/list of uploads")
def uploads():
    with open("static/logs/log.txt", "r") as f:
        content = f.read()
   
    return render_template('uploads.html', content = content)