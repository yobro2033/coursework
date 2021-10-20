import requests
from bs4 import BeautifulSoup as soup
import json

productInput = input("Please enter your product you want to find: ")
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
            print("We have found your product: " + productInput)
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
            print(sorted(results,key=lambda x: x[3])) #, reverse=True
        else:
            print("Not available!")
        print("Thank you for using our service!")
    except Exception as e:
        print(sorted(results,key=lambda x: x[3])) #, reverse=True
        print(e)
        print("Thank you for using our service!")
    #with open('result.json', 'a', newline='') as outfile:
    #    json.dump(results, outfile, ensure_ascii=False, indent=4)
else:
    print(responseCode)
    print("Please try again later!")
