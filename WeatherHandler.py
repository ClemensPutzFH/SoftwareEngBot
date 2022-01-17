import MessageHandler
import requests
import discord
import json
import os
import datetime

#Vorlage: https://github.com/itsOwen/basic-discord-weather-bot/blob/main/basic-discord-weather.py

class WeatherHandler(MessageHandler.MessageHandler):
  def __init__(self):
    self.userChangeSettings = []
    self.userLocationSettings = {}
  
  async def onMessage(self, message):
    await self.weather_save_settings(message)  
    if message.content.startswith('!weather'):
      if message.content.startswith('!weather setting'):
        ret = self.weather_settings(message)
        await message.channel.send(embed=ret)
      else :  
        ret = self.get_weather(message)
        await message.channel.send(embed=ret)
    
  def get_weather(self, msg):
    city = msg.content[9:]
    if len(msg.content[9:]) == 0:
      city = self.userLocationSettings.get(msg.author.id)
    
    try: 
      api_key = os.environ['WeatherAPIKey']
      base_url = "https://api.openweathermap.org/data/2.5/weather?appid="+api_key
      complete_url = base_url + "&q=" + city
      response =  requests.get(complete_url) 

      data = json.loads(response.text)
      
      utc_time = datetime.datetime.utcnow()
      timezone_offset = data["timezone"]
      time_change = datetime.timedelta(seconds=timezone_offset)
      current_time = (utc_time + time_change).strftime("%H:%M")

      celsius = round(data["main"]["temp"]-273.15, 1)
      fclike = round(data["main"]["feels_like"]-273.15, 1)
      iconID = data["weather"][0]["icon"]
      name = data["name"]
      
      embed=discord.Embed(title=f"Weather in {name}", color=0x14aaeb)
      embed.set_thumbnail(url='http://openweathermap.org/img/wn/'+iconID+'@2x.png')
      embed.add_field(name="Temperature", value=f"{celsius}" + " C°", inline=True)
      embed.add_field(name="Feels Like", value=f"{fclike}" + " C°", inline=True)
      embed.set_footer(text="Local Time: " f"{current_time}")
    
      return embed
        
    except:
      embed=discord.Embed(title="No response", color=0x14aaeb)
      embed.add_field(name="Error", value="Oops!! Location not found  :white_frowning_face:", inline=True)
      return embed

  def weather_settings(self, msg):
    self.userChangeSettings.append(msg.author.id);
    #print(self.userChangeSettings);
    
    embed=discord.Embed(title=f"{msg.author.name}, please enter your default location for weather updates", color=0x14aaeb)
    embed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/512/975/975660.png')

    return embed

  async def weather_save_settings(self, msg):
    if msg.author.id in self.userChangeSettings:
      if msg.content.startswith("!weather "):
        msgstring = msg.content[9:]
      else:
        msgstring = msg.content

      self.userLocationSettings.update({msg.author.id: msgstring});
      #print(self.userLocationSettings)
      embed=discord.Embed(title=f"{msg.author.name}, your default location was set to " + str(self.userLocationSettings.get(msg.author.id)), color=0x14aaeb)
      self.userChangeSettings.remove(msg.author.id)
      await msg.channel.send(embed=embed)