import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix= '.')

@client.event
async def on_ready():
    print("Bot is ready")
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