from flask import Flask, render_template, request, session, redirect, url_for, flash
import pyrebase, webbrowser, requests, json, os, datetime
import re
from threading import Timer
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
from werkzeug.utils import html
from modules.iceland import Iceland
from modules.morrisons import Morrisons
from modules.sainsbury import Sainsbury
from modules.tesco import Tesco
from wishlist.wishlistAPI import addNew

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
currentUser = ""

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
    global currentUser
    try:
        email = request.form['email']
        password = request.form['password']
        status = authe.create_user_with_email_and_password(email, password) #Using pyrebase REST API
        currentUser = email
        return redirect(url_for('logindash'))
    except requests.exceptions.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        error_code = json.loads(error_json)['error']['code']
        return render_template('signup_form.html', error=error)

@app.route('/verify', methods=['POST', 'GET'])
def verify():
    error = ""
    global currentUser
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        currentUser = email
        error = None
        try:
            user = authe.sign_in_with_email_and_password(email, password) #Using pyrebase REST API
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
    global currentUser
    try:
        session['usr'] = None
        currentUser = ""
        return redirect(url_for('home'))
    except KeyError:
        return render_template('welcome.html')

@app.route('/search', methods=['POST'])
def searchmodule():
    productInput = request.form["productInput"]
    productInput = str(productInput)
    productInput = removeSC(productInput)
    filterOption = request.form["filterOption"]
    if productInput != None and filterOption != None:
        items = getItems(productInput, filterOption)
        return render_template("result.html", items=items)
    else:
        pass

#Collect the items with input product by using the module from modules folder then short with user's option
def getItems(productInput,filterOption):
    icelandObject = Iceland(productInput,filterOption)
    morrisonsObject = Morrisons(productInput,filterOption)
    sainsburyObject = Sainsbury(productInput,filterOption)
    tescoObject = Tesco(productInput,filterOption)

    totalItems = []
    if icelandObject != None:
        totalItems.extend(icelandObject)
    if morrisonsObject != None:
        totalItems.extend(morrisonsObject)
    if sainsburyObject != None:
        totalItems.extend(sainsburyObject)
    if tescoObject != None: 
        totalItems.extend(tescoObject)
    else:
        pass

    if filterOption == "lowest":
        totalItems = sorted(totalItems,key=lambda x: x['price'])
    else:
        totalItems = sorted(totalItems,key=lambda x: x['price'], reverse=True)
    return totalItems

@app.route('/wishlist', methods=["POST"])
def wishlist():
    wishlistObject = ""
    email = currentUser
    try:
        name = request.form['productName']
        url = request.form['productURL']
        wishlistObject = addNew(email, url, name)
        return wishlistObject
    except Exception as e:
        print(e)
        pass
    return wishlistObject

# Remove special characters to prevent crashes
def removeSC(productInput):
    productInput = re.sub('[^a-zA-Z.\d\s]', '', productInput)
    return productInput

#Auto open browser as soon as users run the program
def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
      Timer(1, open_browser).start();
      app.run(port=5000)