import MessageProvider

class DiscordMessageProvider(MessageProvider.MessageProvider):

  async def provideMsg(self, message):
    await self.provideMessage(message)