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

@client.command()
async def poll(ctx, question, *options):
    if len(options) == 2 and "yes" in options and "no" in options:
        count = 0
        description = []
        reactions = ['✅', '❌']

        for option in options:
            description += '\n {} {}'.format(reactions[count], option)
            count += 1
        embed = discord.Embed(title=question, description=''.join(description))

        react_message = await ctx.send(embed=embed)

        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)



client.run(os.environ["DISCORD_API_TOKEN"])