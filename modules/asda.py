import requests

def Asda(productInput):
    productInput = productInput
    productURLInput = productInput.replace(" ","+")
    my_url = 'https://groceries.asda.com/cmscontent/v2/items/autoSuggest?requestorigin=gi&searchTerm=' + productURLInput
    response = requests.get(my_url).json()
    responsePayload = response['payload']
    asdaItems = []
    i = 0
    while i < 11:
        try:
            for departure in responsePayload['autoSuggestionItems']:
                productLinkBased = 'https://groceries.asda.com/product/'
                productSku = departure['skuId']
                productLink = productLinkBased + productSku
                productBrand = departure['brand']
                productName = departure['skuName']
                productFullName = productBrand + ' ' + productName
                productImageBased = 'https://ui.assets-asda.com/dm/asdagroceries/'
                productImageSku = departure['scene7AssetId']
                productImage = productImageBased + productImageSku
                productPrice = departure['price']
                productPrice = str(productPrice)
                productPrice = productPrice.replace('£', '')
                asdaItems.append({'store': 'Asda', 'name': productFullName, 'url': productLink, 'image': productImage, 'price': productPrice})
                i = i + 1
            return asdaItems
        except Exception as e:
            print(e)
            pass
