import discord
import os
import requests
import json
import weatherAPI
from random import seed, randint
seed(12345679)

client = discord.Client()


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  
    if message.author == client.user:
        return
#WeatherBot gets his message
    msg = message.content
    weatherAPI.get_weather(msg[:9])
    
    if message.content.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if message.content.startswith('!Julian'):
        await message.channel.send(
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        await message.channel.send('<3')
        
    if message.content.startswith('!Aaron'):
        await message.channel.send(
            'https://www.youtube.com/watch?v=dQw4w9WgXfQ')
        await message.channel.send('<3')

    if message.content.startswith('!Clemens'):
        await message.channel.send(
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        await message.channel.send('<3')

    if message.content.startswith('!rave'):
        await message.channel.send(
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ')

#    if message.content.startswith('!send'):
#        await message.channel.send('Clemens Bot stinkt!')

    if message.content.startswith('!xmas'):
        await message.channel.send(
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ')

    if message.content.startswith('!diss'):
        msg = msg[6:]
        rng = randint(0,4)
        if rng == 0:
          await message.channel.send(msg + ' stinkt!')
        if rng == 1:
          await message.channel.send(msg + ' ist ein doofer Pupskopf!')
        if rng == 2:
          await message.channel.send(msg + ' stinkt untenrum!')
        if rng == 3:
          await message.channel.send(msg + ' hat üblen Mundgeruch!')
        if rng == 4:
          await message.channel.send('Keiner mag ' + msg + '!')

my_secret = os.environ['tokenBot']
client.run(my_secret)
