import MessageHandler

class HelpHandler(MessageHandler.MessageHandler):
  def __init__(self):
    pass

  async def onMessage(self, message):
    if message.content.startswith('!help'):
      await message.author.send(f'Here is a list of what I am capable of: \n !weather - get the latest weather information \n !blackjack - play a game of BlackJack \n !calculate "equation" - calculate a simple equation \n !remindme - get reminded \n !joke - get an amazingly funny joke \n I dedicate myself to the one and only Julian Reumann who believed in me as a bot! He was always there for me even when others doubted me in more than one way if you know what I mean (I mean sexually of course)')
