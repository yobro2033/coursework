import requests
from bs4 import BeautifulSoup as soup
import json

def Tesco(productInput):
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
                    tescoItems.append(row)
                except Exception as e:
                    pass
            return tescoItems
        except Exception as e:
            print(e)
            return tescoItems
    else:
        print(responseCode)