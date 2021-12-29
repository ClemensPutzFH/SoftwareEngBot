import MessageHandler
import requests
import json

class JokeHandler(MessageHandler.MessageHandler):
  def __init__(self):
    pass
  
  async def onMessage(self, message):
    if message.content.startswith("!joke"):
      quote = self.get_joke()
      await message.channel.send(quote)
      
  def get_joke(self):
    response = requests.get("https://v2.jokeapi.dev/joke/Any?type=single")
    json_data = json.loads(response.text)
    joke = json_data["joke"]
    return joke