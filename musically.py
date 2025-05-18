import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix = '-')

musicqueue = []

@client.event
async def on_ready():
    print(f'{client.user.display_name} has connected to Discord!')

@client.command(aliases=['p'])
async def play(ctx,songname):
    caller = ctx.author
    callervoice = caller.voice
    if callervoice is not None:
        callervc = callervoice.channel
        botvoiceclient = client.voice_clients
        if len(botvoiceclient) != 0:
            if(botvoiceclient[0].channel != callervc):
                await botvoiceclient[0].disconnect()
                await callervc.connect()
        else:
            await callervc.connect()
        if len(musicqueue) == 0:
            await ctx.send(f'playing **{songname}**')
        else:
            await ctx.send(f'**{songname}** added to queue')
        musicqueue.append(songname)
    else:
        await ctx.send(f'you have to be in a voice channel to play a song')

@client.command()
async def clear(ctx):
    del musicqueue[:]
    await ctx.send(f'queue cleared')

@client.command(aliases=['q'])
async def queue(ctx):
    if len(musicqueue) == 0:
        await ctx.send(f'the queue is empty')
    else:
        queuemsg = ''
        for idx,song in enumerate(musicqueue):
            queuemsg += f'{idx+1}. **{song}'
            queuemsg += '**\n'
        await ctx.send(f'{queuemsg}')

@client.command(aliases=['s'])
async def stop(ctx):
    await ctx.send(f'stopping **{musicqueue[0]}**')

@client.command(aliases=['d'])
async def disconnect(ctx):
    botvoiceclient = client.voice_clients
    if len(botvoiceclient) != 0:
        await botvoiceclient[0].disconnect()

@client.check
async def check_commands(ctx):
    with open('banned.txt') as f:
        bannedusers = f.read().splitlines()
        if str(ctx.author) in bannedusers:
            await ctx.send(f'{ctx.author.display_name} bye!')
            return False
        else:
            return True

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        pass
    else:
        print(error)

client.run(TOKEN)
