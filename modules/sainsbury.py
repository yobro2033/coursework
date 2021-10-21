import requests
from bs4 import BeautifulSoup as soup
import json

def Sainsbury(productInput):
    productInput = productInput
    productURLInput = productInput.replace(" ","%20")
    my_url = 'https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product?filter[keyword]=' + productURLInput
    response = requests.get(my_url).json()
    sainsburyItems = []
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
        sainsburyItems.append(row)
    return sainsburyItems
