import requests
from bs4 import BeautifulSoup as soup
import json

def Tesco(productInput,filterOption):
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
            tescoItems = []
            i = 0
            while i < 11:
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
                        productPrice = str(productPrice)
                        tescoItems.append({'store': 'Tesco', 'name': productName, 'url': productLink, 'image': productImage, 'price': productPrice})
                        i = i + 1
                    except Exception as e:
                        pass
                if filterOption == "lowest":
                    tescoItems = sorted(tescoItems,key=lambda x: x['price'])
                else:
                    tescoItems = sorted(tescoItems,key=lambda x: x['price'], reverse=True)
                return tescoItems
        except Exception as e:
            if filterOption == "lowest":
                tescoItems = sorted(tescoItems,key=lambda x: x['price'])
            else:
                tescoItems = sorted(tescoItems,key=lambda x: x['price'], reverse=True)
            return tescoItems
    else:
        print(responseCode)
