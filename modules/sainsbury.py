import requests
from bs4 import BeautifulSoup as soup
import json

def Sainsbury(productInput):
    productInput = productInput
    productURLInput = productInput.replace(" ","%20")
    my_url = 'https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product?filter[keyword]=' + productURLInput
    response = requests.get(my_url).json()
    sainsburyItems = []
    i = 0
    while i < 11:
        try:
            for departure in response['products']:
                productLink = departure['full_url']
                productName = departure['name']
                productImage = departure['image']
                productPrice = departure['retail_price']['price']
                productPrice = str(productPrice)
                sainsburyItems.append({'store': 'Sainsbury', 'name': productName, 'url': productLink, 'image': productImage, 'price': productPrice})
                i = i + 1
            return sainsburyItems
        except Exception as e:
            print(e)
            return sainsburyItems
