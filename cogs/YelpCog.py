import discord
from discord.ext import commands
import sys

sys.path.insert(0, '../')
from YelpAPI import Yelp


class YelpCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.yelp = Yelp()

    @commands.command()
    async def yelp_business_name(self, ctx, term):
        description = []
        req = self.yelp.business_search(term)
        businesses = self.yelp.get_info(req)
        for info in businesses:
            description += '\n {} - Yelp ID:{}'.format(info["name"],
                                                       info["id"])
        print(description)
        await ctx.send("".join(description))

    @commands.command()
    async def yelp_business_id(self, ctx, bus_id):
        req = self.yelp.id_search(bus_id)
        business = self.yelp.parse_business(req)
        print(business["url"])
        embed = discord.Embed(title=business["name"],
                              description=business["address"])
        embed.add_field(name="link", value=business["url"], inline=True)
        embed.set_image(url=business["image"])
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(YelpCog(client))
