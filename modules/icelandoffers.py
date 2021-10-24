import requests
from bs4 import BeautifulSoup as soup
import json

def IcelandOffer():
    my_url = "https://www.iceland.co.uk/offers"
    response = requests.get(my_url)
    responseCode = str(response)
    if responseCode == "<Response [200]>":
        productListFound = soup(response.text, 'html.parser')
        containers = productListFound.findAll("div",{"class":"card-wrap"})
        icelandOffer = []
        for container in containers:
            try:
                link = "https://www.iceland.co.uk/offers"
                imageContainer = container.find("div", {"class":"card-image"})
                imageSub = imageContainer.find("img")
                image = imageSub['srcset']
                title = imageSub['alt']
                icelandOffer.append({'store': 'Iceland', 'title': title, 'url': link, 'image': image})
            except Exception as e:
                print(e)
                pass
        print(icelandOffer)
        return icelandOffer
    else:
        print(response)