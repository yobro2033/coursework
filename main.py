from flask import Flask, render_template, request, session, redirect, url_for
from bs4 import BeautifulSoup
import pyrebase, webbrowser, requests, json, os, re
from threading import Timer
from werkzeug.utils import html
from modules.iceland import Iceland
from modules.morrisons import Morrisons
from modules.sainsbury import Sainsbury
from modules.tesco import Tesco
from modules.asda import Asda
from modules.ocado import Ocado
from wishlist.wishlistAPI import addNew
from wishlist.displaywishlist import displayWishlist
from offers.icelandoffers import IcelandOffer
from offers.morrisonsoffers import MorrisonsOffer
from offers.sainsburysoffers import SainsburysOffer
from offers.tescooffers import TescoOffer
from offers.asdaoffers import AsdaOffer
#from offers.ocadooffers import OcadoOffer

app = Flask(__name__)
app.secret_key = os.urandom(24)

#Firebase config, get the config from firebase's dashboard setting
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
    email = currentUser
    try:
        #use to check user's session valid
        if session['usr'] != None:
            return render_template("dashboard.html", email=email)
        else: 
            raise KeyError
    except KeyError:
        return render_template('welcome.html')

@app.route('/login', methods=['GET'])
def logindash():
    email = currentUser
    try:
        if session['usr'] != None:
            return render_template("dashboard.html", email=email)
        else:
            raise KeyError
    except KeyError:
	    return render_template('login_form.html')

@app.route('/signup', methods=['GET'])
def signupdash():
    email = currentUser
    try:
        if session['usr'] != None:
            return render_template("dashboard.html", email=email)
        else:
            raise KeyError
    except KeyError:
	    return render_template('signup_form.html')

@app.route('/tos')
def tos():
	return render_template('termsofservice.html')

@app.route('/dashboard')
def dashboard():
    email = currentUser
    try:
        if session['usr'] != None:
            return render_template("dashboard.html", email=email)
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
        error_code = json.loads(error_json)['error']['code'] #get error code
        return render_template('signup_form.html', error=error) #Redirect back to the signup page and display error getting from firebase's api

@app.route('/verify', methods=['POST', 'GET'])
def verify():
    error = ""
    global currentUser
    if request.method == "POST":
        #request the info sent through POST method from the form
        email = request.form["email"]
        password = request.form["password"]
        currentUser = email
        error = None
        try:
            user = authe.sign_in_with_email_and_password(email, password) #Using pyrebase REST API
            user = authe.refresh(user['refreshToken']) #get the token
            user_id = user['idToken']
            #Assign the user's session
            session['usr'] = user_id
            return redirect(url_for('dashboard'))
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
    return render_template("login_form.html", error=error)

@app.route('/search', methods=['POST'])
def search():
    productInput = request.form["productInput"]
    productInput = str(productInput)
    productInput = removeSC(productInput)
    filterOption = request.form["filterOption"]
    if productInput != None and filterOption != None:
        #execute the get items function to retrieve the product scraped
        items = getItems(productInput)
        #change the price into float to sort the list
        items = formatList(items)
        #sort the price with the given criteria
        if filterOption == "lowest":
            items = sorted(items,key=lambda x: x['price'])
        else:
            items = sorted(items,key=lambda x: x['price'], reverse=True)
        return render_template("result.html", items=items)
    else:
        pass

#Save wishlist to json file and redirect to display page
@app.route('/addWishlist', methods=["POST"])
def wishlist():
    email = currentUser
    addWishlist = ""
    try:
        #request the value from form through method post
        name = request.form['productName']
        url = request.form['productURL']
        store = request.form['productStore']
        image = request.form['productImage']
        price = request.form['productPrice']
        addWishlist = addNew(email, url, name, store, image, price)
        return redirect(url_for('displayWL'))
    except Exception as e:
        pass
    return addWishlist

#Display wishlist
@app.route('/wishlist')
def displayWL():
    try:
        global currentUser
        if session['usr'] != None:
            items = displayWishlist(currentUser) #read the json file to retrieve the file
            totalItems = []
            counts = 0 #count total items in the list
            #sum the total price for items in current shopping list
            for item in items:
                item['price'] = float(item['price'])
                newItem = item['price']
                totalItems.append(newItem)
                counts = counts + 1
            priceItems = sum(totalItems)
            priceItems = str(round(priceItems,2)) #ensure no encountered error in price
            return render_template("wishlist.html", items=items, priceItems=priceItems, counts=counts)
        else:
            raise KeyError
    except KeyError:
        return render_template('welcome.html')

#remove wishlist
@app.route('/removeWishlist', methods=["POST"])
def removeWishlist():
    global currentUser
    currentUser = str(currentUser)
    try:
        productName = request.form['name']
        with open('wishlist.json') as json_data:
            datas = json.load(json_data)
            elements = datas['wishlist']
            for data in elements:
                #change the email to "removed" if the user wished to remove item from wishlist
                if data['email'] == currentUser and data['name'] == productName:
                    #changed to "removed" will prevent the program from displaying this item as the email is invalid
                    data['email'] = 'removed'
                else:
                    pass
        #write the list back into json file
        with open('wishlist.json','w') as file:
            json.dump(datas, file, indent = 4)
        return redirect(url_for('displayWL'))
    except Exception as e:
        pass

#Proceed with the keywords to retrieve data from hotdeals
@app.route('/hotdeals', methods=['GET'])
def hotdeals():
    try:
        if session['usr'] != None:
            return render_template("hotdeals.html")
        else: 
            raise KeyError
    except KeyError:
        return render_template('welcome.html')

#Display hot deals from third-party site
@app.route('/hotdealssearch', methods=['POST'])
def hotdealssearch():
    try:
        if session['usr'] != None:
            n=50
            deals = []
            for i in range(0,n):
                deals.extend(getDeals(i+1))
            sortedDeals = deals
            keywords = request.form['keywords']
            keywords = keywords.split(',')
            sortedDeals = keyFilter(keywords, deals)
            return render_template("hotdealsresult.html", items=sortedDeals)
        else: 
            raise KeyError
    except KeyError:
        return render_template('welcome.html')

#Display offers from the retailer
@app.route('/offers')
def displayOffers():
    try:
        if session['usr'] != None:
            items = getOffers()
            return render_template("offers.html", items=items)
        else: 
            raise KeyError
    except KeyError:
        return render_template('welcome.html')

#remove session, logged out user
@app.route('/logout')
def logout():
    global currentUser
    try:
        session['usr'] = None
        currentUser = ""
        return redirect(url_for('home'))
    except KeyError:
        return render_template('welcome.html')

#Collect the items with input product by using the module from modules folder then short with user's option
def getItems(productInput):
    #Get the returned list items found from 6 modules imported
    icelandObject = Iceland(productInput)
    morrisonsObject = Morrisons(productInput)
    sainsburyObject = Sainsbury(productInput)
    tescoObject = Tesco(productInput)
    asdaObject = Asda(productInput)
    ocadoObject = Ocado(productInput)

    #It will then add it into 1 total list
    totalItems = []
    if icelandObject != None:
        totalItems.extend(icelandObject)
    if morrisonsObject != None:
        totalItems.extend(morrisonsObject)
    if sainsburyObject != None:
        totalItems.extend(sainsburyObject)
    if tescoObject != None: 
        totalItems.extend(tescoObject)
    if asdaObject != None:
        totalItems.extend(asdaObject)
    if ocadoObject != None:
        totalItems.extend(ocadoObject)
    else:
        pass

    return totalItems

#Collect offers available from e-commerce websites
def getOffers():
    icelandOffer = IcelandOffer()
    morrisonsOffer = MorrisonsOffer()
    sainsburysOffer = SainsburysOffer()
    tescoOffer = TescoOffer()
    asdaOffer = AsdaOffer()
    #ocadoOffer = OcadoOffer()

    totalItems = []
    if icelandOffer != None:
        totalItems.extend(icelandOffer)
    if morrisonsOffer != None:
        totalItems.extend(morrisonsOffer)
    if sainsburysOffer != None:
        totalItems.extend(sainsburysOffer)
    if tescoOffer != None:
        totalItems.extend(tescoOffer)
    if asdaOffer != None:
        totalItems.extend(asdaOffer)
    #if ocadoOffer != None:
        #totalItems.extend(ocadoOffer)
    else:
        pass

    return totalItems

#Attempting to scrape deals from third party
def getDeals(n):
    dealsList=[]
    url="https://www.hotukdeals.com/tag/groceries?page={}".format(n)
    soup = BeautifulSoup(requests.get(url).content,"html5lib")
    deals = soup.find_all("article")
    for deal in deals:
        if "thread--expired" in deal["class"]:
            continue
        linkElement = deal.find("a",{"class":"thread-title--list"})
        title = linkElement["title"]
        try:
            href = deal.find("a",{"class":"cept-dealBtn"})["href"]
            price = deal.find("span",{"class":"thread-price"}).text
            image = deal.find("img", {"class":"cept-thread-img"})['src']
        except (AttributeError, TypeError):
            continue
        if price == "FREE":
            price = 0
        else:
            try:
                price = float(price[1:].replace(",",""))
            except ValueError:
                continue
        dealsList.append({"title": title, "price": price, "url": href, "image": image})
    return dealsList

#Keywords filter for hotdeals
def keyFilter(keywords,deals):
    filteredList = []
    for item in deals:
        if any(key.lower() in item['title'].lower() for key in keywords):
            filteredList.append(item)
    return filteredList

#Remove special characters to prevent crashes
def removeSC(productInput):
    productInput = re.sub('[^a-zA-Z.\d\s]', '', productInput) #[^a-zA-Z.\d\s] means remove all special character apart from space
    return productInput

#format the price fro string into float to sort
def formatList(items):
    for item in items:
        try:
            item['price'] = float(item['price'])
        except:
            pass
    return items

#Auto open browser as soon as users run the program
def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/')

#Attempt to run the program, open the browser
if __name__ == "__main__":
      Timer(1, open_browser).start();
      app.run(port=5000)
