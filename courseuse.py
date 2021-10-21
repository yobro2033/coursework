from flask import Flask, render_template, request, session, redirect, url_for, flash
import pyrebase, webbrowser, requests, json, os, datetime
from threading import Timer
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
from werkzeug.utils import html

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

@app.route('/search')
def searchmodule():
    try:
        productInput = request.form["productInput"]
        try:
            icelandmodule(productInput)
        except Exception:
            pass
    except Exception:
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

def icelandmodule(productInput):
    productInput = productInput
    productURLInput = productInput.replace(" ","%20")
    my_url = 'https://www.iceland.co.uk/search?q=' + productURLInput
    response = requests.get(my_url)
    responseCode = str(response)
    if responseCode == "<Response [200]>":
        try:
            productListFound = soup(response.text, 'html.parser')
            containers = productListFound.findAll("div",{"class":"product-tile"})
            results = []
            for container in containers:
                productLinkContainer = container.find("div",{"class":"product-image"})
                productLinkItem = productLinkContainer.a["href"]
                productName = productLinkContainer.a["title"]
                productImage = productLinkContainer.a.picture.img["src"]
                price_container = container.find("span",{"class":"product-sales-price"})
                productPrice1 = price_container.text
                productPrice1 = str(productPrice1)
                productPrice2 = productPrice1.replace("\n", "")
                productPrice = productPrice2.replace("£", "")
                unitprice_container = container.find("div",{"class":"product-pricing-info"})
                productUnitPrice1 = unitprice_container.text
                productUnitPrice1 = str(productUnitPrice1)
                productUnitPrice = productPrice1.replace("\n", "")
                row = ['Iceland',productName,productLinkItem,productPrice,productImage,productUnitPrice]
                results.append(row)
            return results
        except Exception as e:
            print(e)
            return results
    else:
        print(responseCode)

def morrisonsmodule(productInput):
    productInput = productInput
    productURLInput = productInput.replace(" ","%20")
    my_url = 'https://groceries.morrisons.com/webshop/api/v1/search?searchTerm=' + productURLInput
    response = requests.get(my_url)
    responseCode = str(response)
    results = []
    if responseCode == "<Response [200]>":
        try:
            productListFound = soup(response.text, 'html.parser')
            productListJson = json.loads(str(productListFound))
            if 'mainFopCollection' in productListJson:
                containers = productListJson['mainFopCollection']['sections']
                for container in containers:
                    productContainer = container['fops']
                    for container in productContainer:
                        productSku = container['sku']
                        productLink = 'https://groceries.morrisons.com/products/-' + productSku
                        if 'product' in container:
                            productName = container['product']['name']
                            productImage = 'https://groceries.morrisons.com/productImages/116/116564011_0_640x640.jpg'
                            productPrice = container['product']['price']['current']
                            productPrice = float(productPrice)
                            productUnitPrice = container['product']['price']['unit']['price']
                            productUnitPrice = str(productUnitPrice)
                            unit = container['product']['price']['unit']['per']
                            unit = str(unit)
                            row = ['Morrisons',productName,productLink,productPrice,productImage,productUnitPrice]
                            results.append(row)
                        else:
                            pass
                return results
            else:
                print("Not available!")
        except Exception as e:
            print(e)
            return results
    else:
        print(responseCode)

def sainsburymodule(productInput):
    productInput = productInput
    productURLInput = productInput.replace(" ","%20")
    my_url = 'https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product?filter[keyword]=' + productURLInput
    response = requests.get(my_url).json()
    results = []
    for departure in response['products']:
        productLink = departure['full_url']
        productName = departure['name']
        productImage = departure['image']
        productPrice = departure['retail_price']['price']
        productPrice = float(productPrice)
        productUnitPrice = departure['unit_price']['price']
        productUnitPrice = str(productUnitPrice)
        productUnitAmount = departure['unit_price']['measure_amount']
        productUnitAmount = str(productUnitAmount)
        productUnitMeasure = departure['unit_price']['measure']
        productUnitMeasure = str(productUnitMeasure)
        unitPrice = str(productUnitPrice + productUnitAmount + productUnitMeasure)
        row = ['Sainsbury',productName,productLink,productPrice,productImage,unitPrice]
        results.append(row)
    return results

def tescomodule(productInput):
    productInput = productInput
    productURLInput = productInput.replace(" ","+")
    my_url = 'https://www.tesco.com/groceries/en-GB/search?query=' + productURLInput
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(my_url, headers=headers)
    responseCode = str(response)
    if responseCode == "<Response [200]>":
        try:
            productListFound = soup(response.text, 'html.parser')
            containers = productListFound.findAll("div",{"class":"product-tile-wrapper"})
            results = []
            for container in containers:
                productLinkContainer = container.find("a",{"class":"product-image-wrapper"})
                productLinkItem = productLinkContainer["href"]
                productLink = 'https://www.tesco.com' + productLinkItem
                productImage = container.find("div",{"class":"product-image__container"}).find('img')["src"]
                productName = container.find("div",{"class":"product-image__container"}).find('img')["alt"]
                productPrice1 = container.find('div',{'class':'price-details--wrapper'})
                try:
                    productPrice2 = productPrice1.find('div' ,{'class': ''})
                    productPrice3 = productPrice2.find('span', {'class': 'value'})
                    productPrice = productPrice3.text
                    productPrice = float(productPrice)
                    unitprice_container = container.find("div",{"class":"price-per-quantity-weight"})
                    productUnitPrice = unitprice_container.span.text
                    productUnitPrice = str(productUnitPrice)
                    unitprice_weight_container = unitprice_container.find("span",{"class":"weight"})
                    unitprice_weight = unitprice_weight_container.text
                    unitprice_weight = str(unitprice_weight)
                    row = ['Tesco',productName,productLink,productPrice,productImage,productUnitPrice]
                    results.append(row)
                except Exception as e:
                    pass
            return results
        except Exception as e:
            print(e)
            return results
    else:
        print(responseCode)

def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
      Timer(1, open_browser).start();
      app.run(port=5000)