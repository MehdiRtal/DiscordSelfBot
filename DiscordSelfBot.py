import discord
import json
from discord.ext import commands

with open('config.json', 'r') as f:
  data = json.load(f)

token = data['token']
client = commands.Bot(command_prefix=".", self_bot=True)

@client.event
async def on_connect():
  print("Logged in as: {}".format(client.user))

@client.group(name='stream', aliases=['s'], invoke_without_command=True)
async def stream(ctx):
  await ctx.message.delete()
  await client.change_presence(activity=discord.Streaming(name=data['stream']['name'], url=data['stream']['url']))
  print("Status is set as: Streaming")

@stream.command(name='name')
async def name(ctx, *, arg):
  await ctx.message.delete()
  data['stream']['name'] = arg
  with open('config.json', 'w') as f:
    json.dump(data, f, indent = 4)
  print("Stream name is: {} ".format(arg))

@stream.command(name='url')
async def url(ctx, arg):
  await ctx.message.delete()
  data['stream']['url'] = "https://www.twitch.tv/" + arg
  with open('config.json', 'w') as f:
    json.dump(data, f, indent = 4)
  print("Stream url is: {} ".format("https://www.twitch.tv/" + arg))

@client.command(name='online', aliases=['on'])
async def online(ctx):
  await ctx.message.delete()
  await client.change_presence(status=discord.Status.online, activity=None)
  print("Status is set as: Online")

@client.command(name='offline', aliases=['off'])
async def offline(ctx):
  await ctx.message.delete()
  await client.change_presence(status=discord.Status.offline, activity=None)
  print("Status is set as: Offline")

@client.command(name='delete', aliases=['del', 'd'])
async def delete(ctx, arg: int):
  async for msg in ctx.channel.history(limit=arg+1):
    try:
      await msg.delete()
    except: pass
  print("{} messages deleted".format(arg))

client.run(token, bot=False)
