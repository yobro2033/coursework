import requests
from bs4 import BeautifulSoup as soup
import json

def Morrisons(productInput,filterOption):
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
                i = 0
                while i < 11:
                    for container in containers:
                        productContainer = container['fops']
                        for container in productContainer:
                            productSku = container['sku']
                            headSub = productSku[0:3]
                            productLink = 'https://groceries.morrisons.com/products/-' + productSku
                            productURL = 'https://groceries.morrisons.com/productImages/' + headSub + '/' + productSku + '_0_640x640.jpg'
                            if 'product' in container:
                                productName = container['product']['name']
                                productImage = 'https://groceries.morrisons.com/productImages/116/116564011_0_640x640.jpg'
                                productPrice = container['product']['price']['current']
                                productPrice = str(productPrice)
                                morrisonsItems.append({'store': 'Morrisons', 'name': productName, 'url': productLink, 'image': productURL, 'price': productPrice})
                                i = i + 1
                            else:
                                pass
                if filterOption == "lowest":
                    morrisonsItems = sorted(morrisonsItems,key=lambda x: x['price'])
                else:
                    morrisonsItems = sorted(morrisonsItems,key=lambda x: x['price'], reverse=True)
                return morrisonsItems
            else:
                print("Not available!")
        except Exception as e:
            print(e)
            if filterOption == "lowest":
                morrisonsItems = sorted(morrisonsItems,key=lambda x: x['price'])
            else:
                morrisonsItems = sorted(morrisonsItems,key=lambda x: x['price'], reverse=True)
            return morrisonsItems
    else:
        print(responseCode)