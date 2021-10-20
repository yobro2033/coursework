import requests
from bs4 import BeautifulSoup as soup
import json

productInput = input("Please enter your product you want to find: ")
productURLInput = productInput.replace(" ","+")
my_url = 'https://www.tesco.com/groceries/en-GB/search?query=' + productURLInput
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(my_url, headers=headers)
responseCode = str(response)
if responseCode == "<Response [200]>":
    try:
        print("We have found your product: " + productInput)
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
        print(sorted(results,key=lambda x: x[3])) #, reverse=True
        print("Thank you for using our service!")
    except Exception as e:
        print(sorted(results,key=lambda x: x[3])) #, reverse=True
        print(e)
        print("Thank you for using our service!")
        pass
    #with open('result.json', 'a', newline='') as outfile:
    #    json.dump(results, outfile, ensure_ascii=False, indent=4)
else:
    print(responseCode)
    print("Please try again later!")
