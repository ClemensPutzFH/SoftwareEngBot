import MessageHandler
import discord
import datetime

class ReminderHandler(MessageHandler.MessageHandler):
  def __init__(self):
    self.userReminderSetup = []
    self.userReminderList = []

  async def onMessage(self, message):
    await self.reminder_save_date(message)
    
    if message.content == "!remindme":
      today = datetime.date.today()
      print("Today's date:", today)
      embed=discord.Embed(title="Missing message", color=0xbe8eb4)
      embed.add_field(name="Error", value="You have not specified a reminder message :cry:", inline=True)
      return embed
      
    elif message.content.startswith('!remindme'):
      await self.reminder_setting_msg(message)
    
    #print("Setup List: " + self.userReminderSetup)
    #print("Reminder list: " + self.userReminderList)

  async def reminder_setting_msg(self, msg):
    self.userReminderSetup.append([msg.author.id, msg.content[9:]])
    print(self.userReminderSetup)

    embed=discord.Embed(title=f"{msg.author.name}, enter your Date for notification.", color=0xbe8eb4)
    embed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/512/1792/1792931.png')
    embed.add_field(name="Date format", value=f"yyyy-mm-dd hh:mm", inline=True)

    await msg.channel.send(embed=embed)

  async def reminder_save_date(self, msg):
    # format: YYYY-MM-TT HH:MM
    # preset timezone +01:00
    timezone_offset = 1
    
    for i in self.userReminderSetup:
      if i[0] == msg.author.id:
        try:
          reminddate = datetime.datetime.fromisoformat(msg.content)
        except:
          embed=discord.Embed(title="Wrong date format", color=0xbe8eb4)
          embed.add_field(name="Error", value="The date you have given isn't formatted correctly :cry:", inline=True)
          await msg.channel.send(embed=embed)
          return

        # subtract given time from current time -> creates timedelta object -> check if result is negative
        if (reminddate - (datetime.datetime.utcnow() + datetime.timedelta(hours=timezone_offset))).total_seconds() < 0:
          embed=discord.Embed(title="Reminder is in the past", color=0xbe8eb4)
          embed.add_field(name="Error", value="The date you have given is in the past :cry:", inline=True)
          await msg.channel.send(embed=embed)
          return
        
        self.userReminderList.append([msg.author.id, reminddate, i[1]])
        self.userReminderSetup.remove([i[0], i[1]])