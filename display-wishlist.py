import json

tests = open("wishlist.json").read()
datas = json.loads(tests)
hello = datas["wishlist"]
print("Here is your wishlist: ")
for h in hello:
    if h['email'] == 'random@yahoo.co.uk':
        url = h['url']
        name = h['name']
        print("\nproduct: ", name)
        print("\nURL: ", url)
    else:
        pass