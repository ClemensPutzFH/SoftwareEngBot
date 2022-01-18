import MessageHandler
import discord

class CalculateHandler(MessageHandler.MessageHandler):
  def __init__(self):
        pass

  async def onMessage(self, message):
    if message.content.startswith("!calc "):
        await self.calculate(message)
        
  async def calculate(self, message):
    msg = message.content[6:]
    if " " in msg:
      calc_list = msg.split(" ")
    elif "+" in msg:
      calc_list = msg.split("+")
      calc_list.append("+")
      calc_list[1], calc_list[2] = calc_list[2], calc_list[1]
    elif "-" in msg:
      calc_list = msg.split("-")
      calc_list.append("-")
      calc_list[1], calc_list[2] = calc_list[2], calc_list[1]
    elif "*" in msg:
      calc_list = msg.split("*")
      calc_list.append("*")
      calc_list[1], calc_list[2] = calc_list[2], calc_list[1]
    elif "/" in msg:
      calc_list = msg.split("/")
      calc_list.append("/")
      calc_list[1], calc_list[2] = calc_list[2], calc_list[1]

    if len(calc_list) != 3:
      embed=discord.Embed(title="Error!", color=0x8A8A8A)
      embed.add_field(name="Incorrect format", value="Please input calculation as \"!calc x + y\" or \"!calc x+y\"", inline=True)
      await message.channel.send(embed=embed)
      return

    try:
      varx = float(calc_list[0])
      vary = float(calc_list[2])
    except ValueError:
      embed=discord.Embed(title="Error!", color=0x8A8A8A)
      embed.add_field(name="Incorrect format", value="Please input calculation as \"!calc number + number\". If you want to enter a comma separated value, use \".\" instead of \",\"", inline=True)
      await message.channel.send(embed=embed)
      return

    operator = calc_list[1]
   
    if operator == "+" or operator == "-" or operator == "*" or operator == "/":
      if operator == "+":
        output = varx + vary
      elif operator == "-":
        output = varx - vary
      elif operator == "*":
        output = varx * vary
      elif operator == "/":
          if vary == 0:
            embed=discord.Embed(title="Error!", color=0x8A8A8A)
            embed.add_field(name="Division by zero", value="I'm good but not that good", inline=True)
            await message.channel.send(embed=embed)
            return
          else:
            output = varx / vary
      embed=discord.Embed(title="Solution", color=0x8A8A8A)
      embed.add_field(name="Your solution", value=f"{str(varx)} {operator} {str(vary)} = {output}", inline=True)
      await message.channel.send(embed=embed)
    else:
      embed=discord.Embed(title="Error!", color=0x8A8A8A)
      embed.add_field(name="Incorrect format", value="Please input calculation as \"!calc x + y\" or \"!calc x+y\"", inline=True)
      await message.channel.send(embed=embed)