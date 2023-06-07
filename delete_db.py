from replit import db

# Retrieve all keys in the database
all_keys = db.keys()

# Delete each key one by one
for key in all_keys:
    del db[key]
