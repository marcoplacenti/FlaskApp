from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime


def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: 
        lst = os.listdir(path)
        print(lst)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    print(tree)
    return tree

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
            log.write(uploaded_file.filename+","+str(timestamp))
            log.write("\n")
            
    return redirect(url_for('home'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/list of uploads")
def uploads():
    with open("static/logs/log.txt", "r") as f:
        content = f.read()
    #path = os.path.expanduser('static/logs/')
    #return render_template('uploads.html', tree=make_tree(path))
    return render_template('uploads.html', content = content)