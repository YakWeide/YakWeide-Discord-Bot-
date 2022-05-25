# Imports
import discord
from discord.ext import commands

# Credentials
TOKEN = 'Njc4MDEyOTMxMDg1OTU5MTk0.Gb3Vb9.Buy4uSdDUt2fSXGVOzDKogzefwmdNa1howeL24'

# Create bot
client = commands.Bot(command_prefix='!')

# Startup Information
@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

# Command
@client.command()
async def helloworld(ctx):
    await ctx.send('Hello World!')

client.run(TOKEN)