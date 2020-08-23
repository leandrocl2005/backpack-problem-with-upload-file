from flask import Flask, render_template
import io

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd

from functions import solveknapSack

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super-secret'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            df = pd.read_csv(stream)
            df['brPrice'] = df['brPrice'].map(lambda x: x/5.6)
            _ids = list(df['items'])
            val = list((df['brPrice'] - df['usPrice']).map(int))
            wt = list(df['usPrice'].map(int))
            W = 200
            n = len(val)
            items, result = solveknapSack(W, wt, val, _ids, n)
            df.to_csv(os.path.join(app.config['UPLOAD_FOLDER'])+"/teste.csv")
            return render_template("results.html", items=items, result=result)
    return render_template("results.html", items=["Alguma coisa deu errado"])
    
if __name__ == "__main__":
    app.run(debug=True)
