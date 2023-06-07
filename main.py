import os
import discord
from discord import app_commands

from collections import Counter
from tabulate import tabulate
from collections import defaultdict
from discord import Embed
from discord.ext import tasks
import json
from datetime import datetime

import unicodedata
from replit import db

import roles


def strip_non_ascii(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text)
                   if unicodedata.category(c) != 'So')


first_run = True

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

env_type = os.getenv('ENV_TYPE')

if env_type == 'dev':
    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = int(os.getenv("DEV_DISCORD_GUILD"))
    LEADERBOARD_CHANNEL_ID = int(os.getenv("DEV_LEADERBOARD_CHANNEL_ID"))
    LEADERBOARD_MESSAGE_ID = os.getenv("DEV_LEADERBOARD_MESSAGE_ID")
else:  # 'prod' or any other value
    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = int(os.getenv("DISCORD_GUILD"))
    LEADERBOARD_CHANNEL_ID = int(os.getenv("LEADERBOARD_CHANNEL_ID"))
    LEADERBOARD_MESSAGE_ID = os.getenv("LEADERBOARD_MESSAGE_ID")

# Initialize an empty dictionary to store points for each user
amp_points = Counter()
base_points = Counter()
total_points = Counter()
outpost_points = Counter()
fleet_points = Counter()
recon_points = Counter()
user_points = defaultdict(lambda: defaultdict(int))

# Command points
points = {"amp": 1}


def strip_non_ascii(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text)
                   if unicodedata.category(c) != 'So')


async def record_to_file(interaction: discord.Interaction, count: int,
                         category: str):
    guild = interaction.guild  # This is a discord.Guild object
    user = await guild.fetch_member(interaction.user.id)
    data = {
        "id": interaction.user.id,
        "name": user.display_name,  # using display name instead of name
        "count": count,
        "category": category,  # add the category here
        "timestamp": datetime.now().isoformat(),
    }
    with open('data.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')


async def record_to_db(interaction: discord.Interaction, count: int,
                       category: str):
    guild = interaction.guild  # This is a discord.Guild object
    user = await guild.fetch_member(interaction.user.id)
    timestamp = datetime.now().isoformat()

    data = {
        "id": interaction.user.id,
        "name": user.display_name,  # using display name instead of name
        "count": count,
        "category": category,  # add the category here
        "timestamp": timestamp,
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


@tree.command(name="add",
              description="Add points for a task",
              guild=discord.Object(id=int(GUILD)))
async def add_points(interaction: discord.Interaction, tasks: str):
    tasks = tasks.lower().split()
    amp_count = tasks.count("amp")
    response_messages = []
    for task in tasks:
        if task not in points:
            response_messages.append(f"Unknown category: {task}")
        else:
            user_points[interaction.user.id][task] += points[task]

    if amp_count > 0:
        response_messages.append(
            f"{points['amp'] * amp_count} AMP kill(s) added, Great job!")

    await interaction.response.send_message("\n".join(response_messages))

    # Update the leaderboard
    await generate_leaderboard(interaction, user_points, "amp")

    # Record data to a local file
    await record_to_db(interaction, amp_count * points['amp'], 'amp')


@tree.command(name="remove",
              description="Remove points for a task",
              guild=discord.Object(id=int(GUILD)))
async def remove_points(interaction: discord.Interaction, tasks: str):
    tasks = tasks.lower().split()
    task_counts = {task: tasks.count(task) for task in set(tasks)}
    response_messages = []
    for task, count in task_counts.items():
        if task not in points:
            response_messages.append(f"Unknown category: {task}")
        elif user_points[interaction.user.id][task] < count * points[
                task]:  # Ensure user has enough points to remove
            response_messages.append(
                f"Not enough points to remove for {task.upper()}")
        else:
            user_points[interaction.user.id][task] -= count * points[task]
            response_messages.append(
                f"{points[task] * count} {task.upper()} Kill(s) removed.")
    await interaction.response.send_message("\n".join(response_messages))

    # Update the leaderboard
    await generate_leaderboard(interaction, user_points, "amp")

    # Record data to a local file
    for task, count in task_counts.items():
        if task in points:
            await record_to_db(interaction, -count * points[task], task)


@tree.command(name="lb",
              description="Show leaderboard for a category",
              guild=discord.Object(id=int(GUILD)))
async def leaderboard(interaction: discord.Interaction, category: str):
    """Generate leaderboard for the given category."""
    if category not in ['amp']:
        await interaction.response.send_message(
            f'Invalid category. Please choose amp.')
    else:
        leaderboard_data = await generate_leaderboard(interaction, user_points,
                                                      category)
        await interaction.response.send_message(f"```\n{leaderboard_data}\n```"
                                                )


# Function to generate leaderboard
async def generate_leaderboard(interaction: discord.Interaction, points_dict,
                               category):

    global LEADERBOARD_MESSAGE_ID
    global first_run

    # Load historical data from database file on first run
    if first_run:
        try:
            # Fetch data from the replit db
            for user_id in db.keys():
                for timestamp, data in points_dict.items():
                    if data['category'] == category:
                        user_points[data['id']][category] += data['count']
        except FileNotFoundError:
            pass
        finally:
            first_run = False

    # Sort user_points dictionary by category score in descending order
    sorted_dict = sorted(points_dict.items(),
                         key=lambda item: item[1][category],
                         reverse=True)

    leaderboard_data = []
    for user_id, scores in sorted_dict:
        guild = interaction.guild  # This is a discord.Guild object
        user = await guild.fetch_member(
            user_id)  # Fetch the user corresponding to user_id
        score = scores[category]
        username = strip_non_ascii(user.display_name)
        leaderboard_data.append((username, score))

    leaderboard = tabulate(leaderboard_data,
                           headers=["Member", "Score"],
                           tablefmt="fancy_grid")

    channel = client.get_channel(LEADERBOARD_CHANNEL_ID)

    if LEADERBOARD_MESSAGE_ID is not None:
        try:
            old_message = await channel.fetch_message(LEADERBOARD_MESSAGE_ID)
            await old_message.delete()
        except:
            pass

    new_message = await channel.send(f"```\n ###  AMP Killboard  ### \
                                     \n{leaderboard}\n```")

    LEADERBOARD_MESSAGE_ID = new_message.id
    # Assign roles based on the leaderboard
    await roles.assign(interaction, sorted_dict)

    return tabulate(leaderboard)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD))
    print("Ready!")


client.run(TOKEN)
