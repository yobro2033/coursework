from flask import Flask, render_template, request, session, redirect, url_for, flash
import pyrebase, webbrowser, requests, json, os, datetime
from threading import Timer
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
from werkzeug.utils import html
from flask import request
from django.contrib.auth import logout

app = Flask(__name__)
app.secret_key = os.urandom(24)
firebaseConfig = {
    "apiKey": "AIzaSyBeOr7f2Il4mMNL2WHoKE7CcxuNKu2LS7I",
    "authDomain": "pricechecker-bb931.firebaseapp.com",
    "projectId": "pricechecker-bb931",
    "storageBucket": "pricechecker-bb931.appspot.com",
    "messagingSenderId": "377615563114",
    "appId": "1:377615563114:web:e3e44e1063cf23a8018d13",
    "measurementId": "G-726Y8YKFDE",
    "databaseURL": "localhost"
  }

firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
db = firebase.database()
status = ""


@app.route('/')
def home():
    return render_template("welcome.html")

@app.route('/login')
def logindash():
    return render_template("login_form.html")

@app.route('/signup')
def signupdash():
    pass

@app.route('/dashboard')
def dashboard():
    pass

@app.route('/insert', methods=['POST'])
def signup():
    pass 

@app.route('/verify', methods=['POST', 'GET'])
def verify():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            user = authe.refresh(user['refreshToken'])
            user_id = user['idToken']
            session['usr'] = user_id
            return redirect(url_for('dashboard'))
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
    return render_template("login_form.html", error=error)

@app.route('/logout')
def logout():
    pass

@app.route('/search', methods=['POST'])
def search():
    pass

@app.route('/result', methods=['POST'])
def result():
    pass

def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
      Timer(1, open_browser).start();
      app.run(port=5000)
