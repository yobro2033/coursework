import requests
from bs4 import BeautifulSoup as soup
import json

def Morrisons(productInput):
    productInput = productInput
    productURLInput = productInput.replace(" ","%20")
    my_url = 'https://groceries.morrisons.com/webshop/api/v1/search?searchTerm=' + productURLInput
    response = requests.get(my_url)
    responseCode = str(response)
    morrisonsItems = []
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
                            morrisonsItems.append(row)
                        else:
                            pass
                return morrisonsItems
            else:
                print("Not available!")
        except Exception as e:
            print(e)
            return morrisonsItems
    else:
        print(responseCode)