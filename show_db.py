from replit import db

print(db.keys())

for user_id in db.keys():
    print(f"Debug user_id: {user_id}")  # Debug print statement
    data = db[user_id]
    #print(f"Debug data: {data}")  # Debug print statement
    for timestamp, record in data.items():
        print(f"Debug records: {timestamp}: {record}")  # Debug print statement



