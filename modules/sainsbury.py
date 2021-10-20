import requests
from bs4 import BeautifulSoup as soup
import json
from pprint import pprint

productInput = input("Please enter your product you want to find: ")
productURLInput = productInput.replace(" ","%20")
my_url = 'https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product?filter[keyword]=' + productURLInput
response = requests.get(my_url).json()
print("We have found your product: " + productInput)
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
#with open('result.json', 'a', newline='') as outfile:
#    json.dump(results, outfile, ensure_ascii=False, indent=4)
sort = sorted(results,key=lambda x: x[3]) #, reverse=True
pprint(sort)
#for i in sort:
#    print(i[3])
print("Thank you for using our service!")