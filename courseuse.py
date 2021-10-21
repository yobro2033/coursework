from flask import Flask, render_template, request, session, redirect, url_for, flash
import pyrebase, webbrowser, requests, json, os, datetime
from threading import Timer
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
from werkzeug.utils import html
from modules.iceland import Iceland
from modules.morrisons import Morrisons
from modules.sainsbury import Sainsbury
from modules.tesco import Tesco

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
    try:
        if session['usr'] != None:
            return render_template("dashboard.html")
        else: 
            raise KeyError
    except KeyError:
        return render_template('welcome.html')

@app.route('/login', methods=['GET'])
def logindash():
    try:
        if session['usr'] != None:
            return render_template("dashboard.html")
        else:
            raise KeyError
    except KeyError:
	    return render_template('login_form.html')

@app.route('/signup', methods=['GET'])
def signupdash():
    try:
        if session['usr'] != None:
            return render_template("dashboard.html")
        else:
            raise KeyError
    except KeyError:
	    return render_template('signup_form.html')

@app.route('/tos')
def tos():
	return render_template('termsofservice.html')

@app.route('/dashboard')
def dashboard():
    try:
        if session['usr'] != None:
            return render_template("dashboard.html")
        else:
            raise KeyError
    except KeyError:
        return redirect(url_for('logindash'))

@app.route('/insert', methods=['POST'])
def signup():
    error = None
    try:
        email = request.form['email']
        password = request.form['password']
        status = authe.create_user_with_email_and_password(email, password)
        return redirect(url_for('logindash'))
    except requests.exceptions.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        error_code = json.loads(error_json)['error']['code']
        return render_template('signup_form.html', error=error)

@app.route('/verify', methods=['POST', 'GET'])
def verify():
    error = ""
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
    try:
        session['usr'] = None
        return redirect(url_for('home'))
    except KeyError:
        return render_template('welcome.html')

@app.route('/search', methods=['POST'])
def searchmodule():
    productInput = request.form["productInput"]
    if productInput != None:
        items = getItems(productInput)
        print(items)
        return render_template("items.html", items=items)
    else:
        pass

@app.route('/results')
def result():
    try:
        if session['usr'] != None:
            return render_template("test.html")
        else: 
            raise KeyError
    except KeyError:
        return render_template('welcome.html')

def getItems(productInput):
    icelandObject = Iceland(productInput)
    morrisonsObject = Morrisons(productInput)
    sainsburyObject = Sainsbury(productInput)
    tescoObject = Tesco(productInput)

    totalItems = []
    icelandItems = []
    morrisonsItems = []
    sainsburyItems = []
    tescoItems = []

    return sainsburyObject

def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
      Timer(1, open_browser).start();
      app.run(port=5000)