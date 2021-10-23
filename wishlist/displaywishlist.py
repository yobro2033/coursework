import json

def displayWishlist(currentUser):
    currentUser = str(currentUser)
    tests = open("wishlist.json").read()
    datas = json.loads(tests)
    hello = datas["wishlist"]
    wishlistdata = []
    for h in hello:
        if h['email'] == currentUser:
            url = h['url']
            name = h['name']
            wishlistdata.append({'url': url, 'name': name})
        else:
            pass
    return wishlistdata
