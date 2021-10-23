import json
currentUser = str(input("Please enter your email: "))
tests = open("wishlist.json").read()
datas = json.loads(tests)
hello = datas["wishlist"]
print("Here is your wishlist: ")
for h in hello:
    if h['email'] == currentUser:
        url = h['url']
        name = h['name']
        print("\nproduct: ", name)
        print("\nURL: ", url)
    else:
        pass