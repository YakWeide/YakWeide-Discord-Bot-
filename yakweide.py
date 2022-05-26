# Imports
from time import sleep

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

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
    channel = client.get_channel(LOG_CHANNEL_ID)
    await channel.send('I´m ready')
    print('I´m ready')


@client.event
async def on_voice_state_update(member, before, after):
    # if user leaves channel
    if before.channel is not None and after.channel is None:
        if member.id != client.user.id:
            voice = await before.channel.connect()
            voice.play(FFmpegPCMAudio("quelle.mp3"))
            while voice.is_playing():
                sleep(1)
            await voice.disconnect()

        else:
            print("Bot ist geleavet")
            return
    else:
        print("kein leaven")
        return


@client.event
async def on_member_ban(guild, user):
    await printLastLog()


@client.event
async def on_member_kick(guild, user):
    await printLastLog()


@client.event
async def on_member_join(member):
    await printLastLog()


@client.event
async def on_member_remove(member):
    await printLastLog()


@client.event
async def on_member_update(member):
    await printLastLog()


async def printLog(limit):
    channel = client.get_channel(LOG_CHANNEL_ID)
    guild = client.get_guild(GUILD_ID)
    async for entry in guild.audit_logs(limit=limit):
        action = f'{entry.action}'

        if action == 'AuditLogAction.member_disconnect':
            message = f'{entry.user} disconnected a user'
        elif action == 'AuditLogAction.member_move':
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


async def printLastLog():
    await printLog(1)


@client.command()
async def logs(ctx):
    channel = client.get_channel(LOG_CHANNEL_ID)

    await channel.send('\n\n------------------------------------------------------------------------------')
    await channel.send('Last 100 Logs:')
    await channel.send('------------------------------------------------------------------------------')

    await printLog(100)

    await channel.send('------------------------------------------------------------------------------\n\n')


client.run(DISCORD_TOKEN)
