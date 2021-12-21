import MessageProvider
import discord

class DiscordMessageProvider(MessageProvider):
  client = discord.Client()
  
  def __init__(self):
    MessageProvider.__init__(self)
    
  @client.event
  async def on_message(self, message):
    self.provideMessage(message)