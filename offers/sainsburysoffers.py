import requests
from bs4 import BeautifulSoup as soup
import json

def SainsburysOffer():
    my_url = "https://www.sainsburys.co.uk/shop/gb/groceries/great-offers"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}
    response = requests.get(my_url, headers=headers)
    responseCode = str(response)
    if responseCode == "<Response [200]>":
        productListFound = soup(response.text, 'html.parser')
        containers = productListFound.findAll("div",{"class":"mEspotCol"})
        sainsburyOffer = []
        for container in containers:
            try:
                linkContainer = container.find("a", {"class":"mContentTile272x272-link"})
                link = linkContainer["href"]
                imageContainer = container.find("img", {"class":"mContentTile272x272-image"})
                image = imageContainer["src"]
                titleContainer = container.find("div", {"class":"mContentTile272x272-text"})
                title = titleContainer.h3.text
                title = str(title)
                title = title.replace("\n","")
                sainsburyOffer.append({'store': 'Sainsburys', 'title': title, 'url': link, 'image': image})
            except Exception as e:
                print(e)
                pass
        print(sainsburyOffer)
        return sainsburyOffer
    else:
        print(response)

SainsburysOffer()