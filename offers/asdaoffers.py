from selenium import webdriver  
from selenium.webdriver.chrome.options import Options 
from bs4 import BeautifulSoup as soup

def AsdaOffer():
    asdaOffer = []
    options = Options()
    options.add_argument("--headless")
    #Insert your chromedriver path replace the current chrome driver
    driver = webdriver.Chrome(options=options, executable_path=r'/Users/quocvietphan/Downloads/chromedriver')
    driver.get("https://groceries.asda.com/special-offers/top-offers") 
    html = driver.page_source
    response = soup(html, 'html.parser')
    items = response.find_all("div",{"class":"asda-banner-static-tempo"})
    for item in items:
        imageContainer = item.find('img')
        linkContainer = item.find('a')
        title = imageContainer['alt']
        if title != '':
            link = linkContainer['href']
            image = imageContainer['src']
            asdaOffer.append({'store': 'Asda', 'title': title, 'url': link, 'image': image})
    driver.quit()
    return asdaOffer