import json

currentUser = "random@yahoo.co.uk"
productName = "Sainsbury's Braeburn Apple Single"

def removeWishlist(currentUser, productName):
    currentUser = str(currentUser)
    productName = str(productName)
    with open('wishlist.json') as json_data:
        datas = json.load(json_data)
        elements = datas['wishlist']
        for data in elements:
            if data['email'] == currentUser and data['name'] == productName:
                data['email'] = 'removed'
            else:
                pass
        with open('wishlist.json','w') as file:
            json.dump(datas, file, indent = 4)
removeWishlist(currentUser, productName)