import discord
import os
import requests
import json

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
    message = message.content
    if message.author == client.user:
        return

    if message.content.startswith('!inspire'):

        quote = get_quote()
        await message.channel.send(quote)

    if message.content.startswith('!Julian'):
        await message.channel.send(
            'https://www.youtube.com/watch?v=wyx6JDQCslE')
        await message.channel.send('<3')
        
    if message.content.startswith('!Aaron'):
        await message.channel.send(
            'https://www.youtube.com/watch?v=FpOOXSd9IxY')
        await message.channel.send('<3')

    if message.content.startswith('!send'):
        await message.channel.send('Clemens Bot stinkt!')

    if message.content.startswith('!diss')


my_secret = os.environ['tok']
client.run(my_secret)
