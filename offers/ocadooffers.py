from selenium import webdriver  
from selenium.webdriver.chrome.options import Options 
from bs4 import BeautifulSoup as soup

def OcadoOffer():
    ocadoOffer = []
    options = Options()
    options.add_argument("--headless")
    #Insert your chromedriver path replace the current chrome driver
    driver = webdriver.Chrome(options=options, executable_path=r'/Users/quocvietphan/Downloads/chromedriver')
    driver.get("https://www.ocado.com/on-offer") 
    html = driver.page_source
    response = soup(html, 'html.parser')
    items = response.find_all("div",{"class":"supFund"})
    for item in items:
        imageContainer = item.find('img')
        linkContainer = item.find('a')
        title = imageContainer['alt']
        link = linkContainer['href']
        imagePrefix = imageContainer['src']
        image = 'https://www.ocado.com' + imagePrefix
        ocadoOffer.append({'store': 'Ocado', 'title': title, 'url': link, 'image': image})
    driver.quit()
    return ocadoOffer
