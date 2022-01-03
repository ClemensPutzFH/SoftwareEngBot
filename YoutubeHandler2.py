import discord
import MessageHandler
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL


players = {}
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

class YoutubeHandler2(MessageHandler.MessageHandler):
  def __init__(self):
    pass
# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in

  async def onMessage(self, message):
   
    #if message.content.startswith("!join"):
      #await join(message)
    
    if message.content.startswith("!play"):
      await join(message)
      await play(message)
   
     
     
async def join(message):
    channel = message.author.voice.channel
    voice = get(client.voice_clients, guild=message.guild)
    if voice and voice.is_connected():
      #TODO can not move to channel
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


# command to play sound from a youtube URL

async def play(message):
   
    videoLink = message.content.split()
    adress = videoLink[1]
    print (adress)
    print(videoLink)
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=message.guild)
    
    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(adress, download=False)
        URL = info['url']
        print (URL)
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await message.send('Bot is playing')

# check if the bot is already playing
    else:
        await message.send("Bot is already playing")
        return

""""
# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')


# command to pause voice if it is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


# command to stop voice
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Stopping...')


# command to clear channel messages
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages have been cleared")

"""""