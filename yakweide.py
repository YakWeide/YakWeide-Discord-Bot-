# Imports
from time import sleep

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

# Credentials
import yakweide

DISCORD_TOKEN = ''
GUILD_ID = 817139732026228767
LOG_CHANNEL_ID = 979135868910592071
previouslog = None
previousmove = None
previousdisconnect = None
goodbyeActive = False
# Create bot
client = commands.Bot(command_prefix='!')


# Startup Information
@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
    channel = client.get_channel(LOG_CHANNEL_ID)
    await channel.send('I´m ready')
    print('I´m ready')


@client.command()
async def activate(ctx):
    global goodbyeActive
    goodbyeActive = True
    return


@client.command()
async def deactivate(ctx):
    global goodbyeActive
    goodbyeActive = False
    return


@client.event
async def on_voice_state_update(member, before, after):
    await checkLog(member=member)
    # if user leaves channel
    if before.channel is not None and after.channel is None and goodbyeActive:
        if member.id != client.user.id:
            voice = await before.channel.connect()
            voice.play(FFmpegPCMAudio("Ciaoooo.mp3"))
            while voice.is_playing():
                sleep(1)
            await voice.disconnect()

        else:
            print("Bot ist geleavet")
            return
    else:
        print("kein leaven")
        return



async def checkLog(member):
    guild = client.get_guild(GUILD_ID)
    newlog = None
    newdisconnect = None
    newMove = None

    i = 0
    async for entry in guild.audit_logs(limit=100):
        if i == 0:
            newlog = entry
        action = f'{entry.action}'
        if newdisconnect is None and action == 'AuditLogAction.member_disconnect':
            newdisconnect = entry
        if newMove is None and action == 'AuditLogAction.member_move':
            newMove = entry
        if newdisconnect is not None and newMove is not None:
            break
        i = i+1

    if previouslog is None:
        yakweide.previouslog = newlog
        return

    if previouslog.id != newlog.id:
        yakweide.previouslog = newlog
        await printLog(entry=newlog, member=member)
        return

    if f'{newlog.action}' == 'AuditLogAction.member_disconnect':
        if yakweide.previousdisconnect is None:
            yakweide.previousdisconnect = newlog
            await printLog(entry=newlog, member=member)
            return
        elif yakweide.previousdisconnect.id != newlog.id:
            yakweide.previousdisconnect = newlog
            await printLog(entry=newlog, member=member)
            return
        else:
            print("previousdisconnect nein")

    if f'{newlog.action}' == 'AuditLogAction.member_move':
        if yakweide.previousmove is None:
            yakweide.previousmove = newlog
            await printLog(entry=newlog, member=member)
            return
        elif yakweide.previousmove.id != newlog.id:
            yakweide.previousmove = newlog
            await printLog(entry=newlog, member=member)
            return
        else:
            print("previousmove nein")

async def printLog(entry, member):
    channel = client.get_channel(LOG_CHANNEL_ID)
    action = f'{entry.action}'

    if action == 'AuditLogAction.member_disconnect':
        if member is not None:
            message = f'{entry.user} disconnected {member}'
        else:
            message = f'{entry.user} disconnected a user'
    elif action == 'AuditLogAction.member_move':
        if member is not None:
            message = f'{entry.user} moved {member}'
        else:
            message = f'{entry.user} moved a user'
    elif action == 'AuditLogAction.unban':
        message = f'{entry.user} unbanned {entry.target}'
    elif action == 'AuditLogAction.ban':
        message = f'{entry.user} banned {entry.target}'
    elif entry.target is None:
        message = f'{entry.user} did {action}'
    else:
        message = f'{entry.user} did {action} to {entry.target}'

    print(message)
    await channel.send(message)


client.run(DISCORD_TOKEN)
