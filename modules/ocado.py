from selenium import webdriver  
from selenium.webdriver.chrome.options import Options 
from bs4 import BeautifulSoup as soup

def Ocado(productInput):
    productInput = productInput
    productURLInput = productInput.replace(" ","+")
    my_url = 'https://www.ocado.com/search?entry=' + productURLInput
    ocadoItems = []
    options = Options()
    options.add_argument("--headless")
    #Insert your chromedriver path replace the current chrome driver
    driver = webdriver.Chrome(options=options, executable_path=r'/Users/quocvietphan/Downloads/chromedriver')
    driver.get(my_url) 
    html = driver.page_source
    response = soup(html, 'html.parser')
    items = response.find_all("div",{"class":"fop-contentWrapper"})
    i = 0
    while i < 11:
        for item in items:
            linkContainer = item.find('a')
            linkPrefix = linkContainer['href']
            productLink = 'https://www.ocado.com' + linkPrefix
            imageContainer = item.find("div",{"class": "fop-img-wrapper"})
            imageclass = imageContainer.find('img')
            imagePrefix = imageclass['src']
            productImage = 'https://www.ocado.com' + imagePrefix
            productName = imageclass['alt']
            priceContainer = item.find("span",{"class":"fop-price"})
            productPrice = priceContainer.text
            productPrice = str(productPrice)
            #attempt to format the price in case it's in 50p instead of £0.50
            if "p" in productPrice:
                productPrice = productPrice.replace("p", "")
                productPrice = "0." + productPrice
            else:
                productPrice = productPrice.replace("£", "")
            ocadoItems.append({'store': 'Ocado', 'name': productName, 'url': productLink, 'image': productImage, 'price': productPrice})
            i = i + 1
    driver.quit()
    return ocadoItems
