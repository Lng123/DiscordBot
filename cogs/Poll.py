import discord
from discord.ext import commands
import sys
sys.path.insert(0, '../')
from EventTopic import Lunch


class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.options = None
        self.events = []
        self.current = None
        self.reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣']

    @commands.command()
    async def poll(self, ctx, question, *options):
        count = 0
        description = []
        for option in options:
            description += '\n {} {}'.format(self.reactions[count], option)
            count += 1
        embed = discord.Embed(title=question, description=''.join(description))
        message = await ctx.send(embed=embed)
        for reaction in self.reactions[:len(options)]:
            await message.add_reaction(reaction)
        embed.set_footer(text='Message ID: {}'.format(message.id))
        await message.edit(embed=embed)
        lunch = Lunch()
        lunch.set_id(message.id)
        self.events.append(lunch)

    @commands.command()
    async def count_votes(self, ctx):
        votes = {}
        winners = []
        message = await ctx.fetch_message(self.events[0].get_id())
        embed_desc = message.embeds[0].description.strip()
        embed_desc = embed_desc.replace("\n", "")
        print(embed_desc)
        temp_list = embed_desc.split(" ")
        # print(temp_list)
        options = {temp_list[x]: temp_list[x + 1] for x in range(0, len(
            temp_list), 2)}
        print(options)
        for reaction in message.reactions:
            # print(reaction)
            # print(reaction.emoji)
            if reaction.emoji in options:
                reacters = await reaction.users().flatten()
                votes[reaction.emoji] = len(reacters)
                # print(reaction)
                # print(reacters)
        max_value = max(votes.values())
        max_keys = [key for key, value in votes.items() if value == max_value]
        for i, j in options.items():
            print(f"key: {i}")
            print(f"key: {j}")
            print(max_keys)
            if i in max_keys:
                winners.append(j)

        await self.showResults(ctx, winners)

    async def showResults(self, ctx, winners):
        embed = discord.Embed(title="Poll finished", description=f"{winners} "
                                                                 f"have "
                                                                 f"the most "
                                                                 f"votes")
        await ctx.send(embed=embed)
        if len(winners) > 0:
            print("Its a tie")


# Have a timer that automatically scores the polls, then clears the poll
# Have an optional arg for the id for manual execution
def setup(client):
    client.add_cog(Poll(client))
