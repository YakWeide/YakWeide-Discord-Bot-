# Imports
import discord
from discord.ext import commands

# Credentials
DISCORD_TOKEN = 'Njc4MDEyOTMxMDg1OTU5MTk0.Gb3Vb9.Buy4uSdDUt2fSXGVOzDKogzefwmdNa1howeL24'
GUILD_ID = 817139732026228767
LOG_CHANNEL_ID = 979135868910592071


# Create bot
client = commands.Bot(command_prefix='!')


# Startup Information
@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
    await successLogin()


# sets both guild and log channel, also fetches the two most recent move and disconnect logs
async def successLogin():
    channel = client.get_channel(LOG_CHANNEL_ID)
    guild = client.get_guild(GUILD_ID)

    async for entry in guild.audit_logs(action=discord.AuditLogAction.ban):
        message = f'{entry.user} banned {entry.target}'
        print(message)
        await channel.send(message)

    async for entry in guild.audit_logs(action=discord.AuditLogAction.member_disconnect):
        message = f'{entry.user} disconnected {entry.target}'
        print(message)
        await channel.send(message)

    async for entry in guild.audit_logs(action=discord.AuditLogAction.kick):
        message = f'{entry.user} kicked {entry.target}'
        print(message)
        await channel.send(message)

    async for entry in guild.audit_logs(action=discord.AuditLogAction.unban):
        message = f'{entry.user} unbanned {entry.target}'
        print(message)
        await channel.send(message)

    async for entry in guild.audit_logs(action=discord.AuditLogAction.member_move):
        message = f'{entry.user} moved {entry.target}'
        print(message)
        await channel.send(message)

    await channel.send('I´m ready')


# Command
# @client.command()
# async def helloworld(ctx):
# await ctx.send('Hello World!')


client.run(DISCORD_TOKEN)
