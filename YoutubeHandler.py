from discord.ext import commands
import youtube_dl

client = commands.Bot(command_prefix = '!')


@client.command(pass_context=True)
async def join(ctx):
  channel = ctx.message.author.voice.voice_channel
  await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
  guild = ctx.message.guild
  voice_client = client.voice_client_in(guild)
  await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
  guild = ctx.message.guild
  voice_client = client.voice_client_in(guild)
  player = await voice_client.create_ytdl_player(url)
  player[guild.id] = player
  player.start()

#https://www.youtube.com/watch?v=MbhXIddT2YY