import requests
from bs4 import BeautifulSoup as soup

def TescoOffer():
    my_url = 'https://www.tesco.com/groceries/en-GB/promotions'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(my_url, headers=headers)
    responseCode = str(response)
    if responseCode == "<Response [200]>":
        try:
            productListFound = soup(response.text, 'html.parser')
            containers = productListFound.findAll("div",{"class":"product-tile-wrapper"})
            tescoOffer = []
            for container in containers:
                productLinkContainer = container.find("a",{"class":"product-image-wrapper"})
                link = productLinkContainer["href"]
                image = container.find("div",{"class":"product-image__container"}).find('img')["src"]
                title = container.find("div",{"class":"product-image__container"}).find('img')["alt"]
                tescoOffer.append({'store': 'Tesco', 'title': title, 'url': link, 'image': image})
            return tescoOffer
        except Exception as e:
            print(e)
            return tescoOffer
    else:
        print(responseCode)
