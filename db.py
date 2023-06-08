import json
from replit import db

class DatabaseManager:
    def __init__(self):
        self.first_run = True
        self.user_points = defaultdict(lambda: defaultdict(int))

    async def load_data(self, category):
        if self.first_run:
            try:
                # Open and read the db.json file
                with open('db.json', 'r') as f:
                    data = json.load(f)
    
                # Iterate over the data from the db.json file
                for user_id, records in data.items():
                    print(f"Debug user_id: {user_id}")  # Debug print statement
                    print(f"Debug records: {records}")  # Debug print statement
                    
                    # Write the records to the Replit database
                    db[user_id] = records
                    
                    for timestamp, record in records.items():
                        print(f"Debug timestamp: {timestamp}: {record}")  # Debug print statement
                        if record['category'] == category:
                            guild = self.client.guilds[GUILD]  # replace with the appropriate guild
                            user = await guild.fetch_member(int(user_id))
                            self.user_points[user.display_name][category] += record['count']
                self.first_run = False
    
            except Exception as e:
                print(f"Error: {e}")





    def update_db(self, interaction, count, category):
        guild = interaction.guild # This is a discord.Guild object
        user = await guild.fetch_member(interaction.user.id)
        timestamp = datetime.now().isoformat()

        data = {
            "id": interaction.user.id,
            "name": user.display_name, # using display name instead of name
            "count": count,
            "category": category, # add the category here
        }

        # Check if the user already has entries in the db
        if str(interaction.user.id) in db.keys():
            user_data = db[str(interaction.user.id)]
        else:
            user_data = {}

        # Store the data under the timestamp key in the user's data
        user_data[timestamp] = data

        # Store the user's data back in the replit db
        db[str(interaction.user.id)] = user_data
