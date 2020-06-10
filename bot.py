import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix= '.')

#Check for events
@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_member_join(member):
    print(f"{member} has joined the server")

@client.event
async def on_member_remove(member):
    print(f"{member} has left the server")

@client.command()
async def ping(ctx):
    await ctx.send(f"{round(client.latency * 1000)}ms")

@client.command()
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
# import discord
#
# class MyClient(discord.Client):
#     async def on_ready(self):
#         print('Logged on as {0}!'.format(self.user))
#
#     async def on_message(self, message):
#         print('Message from {0.author}: {0.content}'.format(message))
#
# client = MyClient()


client.run(os.environ["DISCORD_API_TOKEN"])