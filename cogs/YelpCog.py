import discord
from discord.ext import commands


class YelpCog(commands.Cog):
    def __init__(self, client):
        pass

    @commands.command()
    def yelp_find(self):
        pass


def setup(client):
    client.add_cog(YelpCog(client))