class MessageProvider:
  def __init__(self):
    self.messageHandlerList = []

  def addMessageHandler(self, messageHandler):
    self.messageHandlerList.append(messageHandler)

  def removeMessageHandler(self, messageHandler):
    self.messageHandlerList.remove(messageHandler)

  async def provideMessage(self, message):
    for handler in self.messageHandlerList:
      await handler.onMessage(message)