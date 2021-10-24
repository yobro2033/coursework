import requests
from bs4 import BeautifulSoup as soup
import json

def MorrisonsOffer():
    my_url = "https://groceries.morrisons.com/on-offer"
    response = requests.get(my_url)
    responseCode = str(response)
    if responseCode == "<Response [200]>":
        productListFound = soup(response.text, 'html.parser')
        containers = productListFound.findAll("a",{"class":"offers carousel"})
        morrisonsOffer = []
        for container in containers:
            try:
                link = container['href']
                imageContainer = container.img['src']
                image = 'https://groceries.morrisons.com/' + imageContainer
                title = "Check website"
                morrisonsOffer.append({'store': 'Morrisons', 'title': title, 'url': link, 'image': image})
            except Exception as e:
                print(e)
                pass
        print(morrisonsOffer)
        return morrisonsOffer
    else:
        print(response)