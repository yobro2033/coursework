import json

def addNew(email,url,name,store,image):
    def write_json(new_data, filename='wishlist.json'):
        with open(filename,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data["wishlist"].append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)

    # python object to be appended
    newWishlist = {"email": email,
        "url": url,
        "name": name,
        "store": store,
        "image": image
        }
        
    write_json(newWishlist)
    return newWishlist