from replit import db
import discord
from datetime import datetime
import os

data = {
    "2023-06-07T06:38:55.354488": {
        "id": "",
        "name": "bongrip2",
        "count": 36,
        "category": "amp",
    },
    "2023-06-07T06:38:56.354488": {
        "id": "",
        "name": "Everblue",
        "count": 23,
        "category": "amp",
    },
    "2023-06-07T06:38:57.354488": {
        "id": "",
        "name": "Grey Ghost",
        "count": 22,
        "category": "amp",
    },
    "2023-06-07T06:38:58.354488": {
        "id": "",
        "name": "Nobody",
        "count": 13,
        "category": "amp",
    },
    "2023-06-07T06:38:59.354488": {
        "id": 458748702794711061,
        "name": "Z Mortar",
        "count": 8,
        "category": "amp",
    },
    "2023-06-07T06:39:00.354488": {
        "id": "",
        "name": "Aeternus",
        "count": 3,
        "category": "amp",
    },
    "2023-06-07T06:39:01.354488": {
        "id": "",
        "name": "fev",
        "count": 2,
        "category": "amp",
    },
    "2023-06-07T06:39:02.354488": {
        "id": "",
        "name": "Guts",
        "count": 2,
        "category": "amp",
    },
    "2023-06-07T06:39:03.354488": {
        "id": "",
        "name": "GreaterDom",
        "count": 2,
        "category": "amp",
    },
    "2023-06-07T06:39:04.354488": {
        "id": "",
        "name": "Gloriads",
        "count": 2,
        "category": "amp",
    },
    "2023-06-07T06:39:05.354488": {
        "id": "",
        "name": "Idioteque (July/Fanta)",
        "count": 2,
        "category": "amp",
    },
    "2023-06-07T06:39:06.354488": {
        "id": "",
        "name": "Werewo1F / WraithWrW",
        "count": 1,
        "category": "amp",
    },
    "2023-06-07T06:39:07.354488": {
        "id": "",
        "name": "Richi01 (UTC +6)",
        "count": 1,
        "category": "amp",
    },
    "2023-06-07T06:39:08.354488": {
        "id": "",
        "name": "Usnow",
        "count": 1,
        "category": "amp",
    },
    "2023-06-07T06:39:09.354488": {
        "id": "",
        "name": "guest******",
        "count": 1,
        "category": "amp"
    }
}
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = int(os.getenv("DISCORD_GUILD"))
LEADERBOARD_CHANNEL_ID = int(os.getenv("LEADERBOARD_CHANNEL_ID"))
LEADERBOARD_MESSAGE_ID = os.getenv("LEADERBOARD_MESSAGE_ID")


async def record_to_db(timestamp, **record):
    data = {
        "id": record.get("id"),
        "name": record.get("name"),  # using display name instead of name
        "count": record.get("count"),
        "category": record.get("category"),  # add the category here
    }

    # Check if the user already has entries in the db
    if str(record["name"]) in db.keys():
        user_data = db[str(record["name"])]
    else:
        user_data = {}

    # Store the data under the timestamp key in the user's data
    user_data[timestamp] = data

    # Store the user's data back in the replit db
    db[str(record["name"])] = user_data


@client.event
async def on_ready():
    print("Ready!")
    guild = discord.utils.get(client.guilds,
                              id=GUILD)  # Get the guild by its ID

    # Fetch all the members of the guild
    members = []
    async for member in guild.fetch_members(limit=None):
        members.append(member)

    member_dict = {
        member.display_name: member.id
        for member in members
    }  # Create a dictionary mapping member nicknames to their IDs

    # Populate user ids in data
    for timestamp, record in data.items():
        name = record["name"]
        if name in member_dict:
            record["id"] = member_dict[name]
            print(f'Member {name} matched to id {record["id"]}')
        else:
            print(f"Member {name} not found in guild.")

    # Display data
    print(data)

    # Store the data in the database
    for timestamp, record in data.items():
        await record_to_db(timestamp, **record)


client.run(TOKEN)
