# Imports
import discord
import asyncio
import logging

def run(config):
    client = discord.Client()

    @client.event
    asyncio.def on_ready():
        logging.info("Logged in as %s", client.user)

    client.run(config["token"])
