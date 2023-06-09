# Imports
import discord
import asyncio

def setup_commands(client):
    @client.command()
    asyncio.def ping(ctx):
        await ctx.send("Pong!")
