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
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command does not exist.")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the amount of messages to delete.")

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.environ["DISCORD_API_TOKEN"])