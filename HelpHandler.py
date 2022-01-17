import MessageHandler
import discord

class HelpHandler(MessageHandler.MessageHandler):
  def __init__(self):
    pass

  async def onMessage(self, message):
    if message.content.startswith('!help'):
      embed=discord.Embed(title="Help is here!", color=0x8A8A8A)
      embed.add_field(name="Here is a list of what I am capable of:", value="Weather:\n!weather setting - you can set your default location\n!weather 'location' - you can search for the weather at a certain location\n\nBlackJack:\n!blackjack - play a game of BlackJack\n!bet 'amount' - You start a game against the dealer for a certain amount\n!stand - you think you have enough cards and want to see what the dealer has\n!hit - you want another card\n!double - double down on your bet and get one more card before the dealer shows its cards\n!credits - see the amount of money you still have left to play with\n!beg - beg the Dealer for more money, maybe he's in a good mood\n\nCalculator:\n!calc 'equation' - calculate a simple equation (+, -, *, /)\n\nReminder:\n!remindme - get personally reminded about something important!\n\nJoke:\n!joke - get an amazingly funny random joke\n\nCredits:\nIcons used are created by Freepik - Flaticon", inline=True)
      embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/906/906763.png")
     
      await message.channel.send(embed=embed)
      return
      
