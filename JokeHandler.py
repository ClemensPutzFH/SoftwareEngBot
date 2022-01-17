import MessageHandler
import requests
import json
import discord

class JokeHandler(MessageHandler.MessageHandler):
  def __init__(self):
    pass
  
  async def onMessage(self, message):
    if message.content.startswith("!joke"):
      quote = self.get_joke()
      embed=discord.Embed(title="Enjoy this joke at your own risk! :)", color=0xEC54DA)
      embed.add_field(name=f"Category: {quote[1]}", value=f"{quote[0]}", inline=True)
      embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/747/747858.png")
      await message.channel.send(embed=embed)
      
  def get_joke(self):
    response = requests.get("https://v2.jokeapi.dev/joke/Any?type=single")
    json_data = json.loads(response.text)
    joke = json_data["joke"]
    category = json_data["category"]
    return [joke, category]