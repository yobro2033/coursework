import requests
from bs4 import BeautifulSoup as soup
import json
productInput = input("Please enter your product you want to find: ")
filterOption = input("Please enter your filter option (cheapest or expensive): ")
filterOption = filterOption.lower()
productURLInput = productInput.replace(" ","%20")
my_url = 'https://www.iceland.co.uk/search?q=' + productURLInput
response = requests.get(my_url)
responseCode = str(response)
if responseCode == "<Response [200]>":
    try:
        print("We have found your product: " + productInput)
        productListFound = soup(response.text, 'html.parser')
        containers = productListFound.findAll("div",{"class":"product-tile"})
        results = []
        for container in containers:
            productLinkContainer = container.find("div",{"class":"product-image"})
            productLinkItem = productLinkContainer.a["href"]
            productName = productLinkContainer.a["title"]
            productImage = productLinkContainer.a.picture.img["src"]
            price_container = container.find("span",{"class":"product-sales-price"})
            productPrice1 = price_container.text
            productPrice1 = str(productPrice1)
            productPrice2 = productPrice1.replace("\n", "")
            productPrice = productPrice2.replace("£", "")
            unitprice_container = container.find("div",{"class":"product-pricing-info"})
            productUnitPrice1 = unitprice_container.text
            productUnitPrice1 = str(productUnitPrice1)
            productUnitPrice = productPrice1.replace("\n", "")
            row = ['Iceland',productName,productLinkItem,productPrice,productImage,productUnitPrice]
            results.append(row)
        print("Thank you for using our service!")
        if filterOption == "cheapest":
            print(sorted(results,key=lambda x: x[3]))
        else:
            print(sorted(results,key=lambda x: x[3], reverse=True))
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