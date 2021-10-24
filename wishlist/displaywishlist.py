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
            store = h['store']
            image = h['image']
            wishlistdata.append({'url': url, 'name': name, 'store': store, 'image': image})
        else:
            pass
    return wishlistdata