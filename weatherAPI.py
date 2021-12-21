import os
import requests
import discord
import json
import datetime
import emoji

#Vorlage: https://github.com/itsOwen/basic-discord-weather-bot/blob/main/basic-discord-weather.py

def get_weather(city):
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
        embed.add_field(name="Error", value="Oops!! Location not found  /U00002639", inline=True)
        return embed