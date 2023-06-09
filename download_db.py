from replit import db
import csv

def download_db():
    # get all keys from the database
    keys = db.keys()

    # prepare a list of dictionaries to represent each row
    table = []

    # iterate over each key
    for key in keys:
        # get the value associated with the key
        value = db[key]

        # add the key-value pair as a dictionary to the table
        table.append({'key': key, 'value': value})

    # write the table to a CSV file
    with open('database.csv', 'w', newline='') as csvfile:
        fieldnames = ['key', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(table)

    print("Data downloaded successfully")

download_db()
