import MessageHandler

class CalculateHandler(MessageHandler.MessageHandler):
  def __init__(self):
        pass

  async def onMessage(self, message):
    if message.content.startswith("!calc"):
        calc_list = message.content.split()
        
        calculation = self.calculate(calc_list)
        await message.channel.send(calculation)
        
  def calculate(self, calc_list):
   
    if len(calc_list) != 4:
      output = "Error! incorrect Format. Please input calculation as !calc x + y"
      return output
    try:
      float(calc_list[1])
      float(calc_list[3])
    except ValueError:
      output = "Error! incorrect Format. Please input calculation as !calc number + number. If you want to enter a comma separated value, use . instead of ,"
      return output

    varx = float(calc_list[1])
    vary = float(calc_list[3])
    operator = calc_list[2]
   

    if operator == "+":
      output = varx + vary
      return output

    elif operator == "-":
      output = varx - vary
      return output

    elif operator == "*":
      output = varx * vary
      return output

    elif operator == "/":
        if vary == 0:
          return "Error! Division by 0 not possible!"
        else:
          output = varx / vary
          return output

    elif operator != "+" and "-" and "/" and "*":
      output = "Error! Incorrect Format. Please use one of the following operations '+', '-', '*', '/' "
      return output
  
    else: 
      output = "Error! incorrect Format. Please input calculation as !calc x + y"
      return output