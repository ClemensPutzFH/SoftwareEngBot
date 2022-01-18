import discord
import os
from DiscordMessageProvider import DiscordMessageProvider
from WeatherHandler import WeatherHandler
from JokeHandler import JokeHandler
from HelpHandler import HelpHandler
from CalculateHandler import CalculateHandler
from ReminderHandler import ReminderHandler
from BlackjackHandler import BlackjackHandler

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

dmp = DiscordMessageProvider()
wh = WeatherHandler()
jh = JokeHandler()
hh = HelpHandler()
ch = CalculateHandler()
rh = ReminderHandler(client)
bj = BlackjackHandler()

dmp.addMessageHandler(wh)
dmp.addMessageHandler(jh)
dmp.addMessageHandler(hh)
dmp.addMessageHandler(ch)
dmp.addMessageHandler(rh)
dmp.addMessageHandler(bj)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=5, name="SoftwareEng"))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  await dmp.provideMsg(message)

@client.event
async def on_member_join(member):
    guild = client.get_guild(member.guild.id)
    #print(guild)
    welcome_channel = discord.utils.get(guild.text_channels, position=0)
    #print(welcome_channel)
    await welcome_channel.send(f'Welcome to the {guild.name} Discord Server, {member.mention}!  :partying_face:')
    await member.send(f'We are glad to have you in the {guild.name} Discord Server, {member.name}!  :partying_face:\nHere is a list of what I am capable of:\n\nUse one of this commands in a textchannel on your Server\n\n!weather \"location\" - get the latest weather information\n!blackjack - play a game of BlackJack\n!calc \"equation\" - calculate a simple equation\n!remindme \"message\" - get reminded\n!help - get more info about my functionality\n!joke - get an amazingly funny joke\n')

my_secret = os.environ['tokenBot']
client.run(my_secret)