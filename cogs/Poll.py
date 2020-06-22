import discord
from discord.ext import commands
import sys
sys.path.insert(0, '../')
from EventTopic import Lunch
import time
from datetime import datetime, timedelta


class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.options = []
        self.current = None
        self.reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣']
        self.event = None

    @commands.command()
    async def create_poll(self, ctx, poll):
        if poll.lower() == "lunch":
            self.event = Lunch()
            await ctx.send("Lunch poll created")
        else:
            await ctx.send("Not a valid poll type")

    @commands.command()
    async def add_option(self, ctx, *options):
        if (len(options) + len(self.options)) > len(self.reactions):
            await ctx.send(f"Too many options, the limit of options is "
                           f"{len.options}")
        else:
            for option in options:
                if option not in self.options:
                    self.options.append(option)

    @commands.command()
    async def del_option(self, ctx, option):
        if option in self.options:
            self.options.remove(option)
            await ctx.send(f"removed {option}")
        else:
            await ctx.send(f"{option} does not exist")

    @commands.command()
    async def show_options(self, ctx):
        option_str = " ".join(self.options)
        await ctx.send(f"{option_str}")

    @commands.command()
    async def poll(self, ctx, *options):
        if self.event is None:
            await ctx.send("No poll has been created")
            return
        count = 0
        description = []
        poll_options = ""
        if options:
            poll_options = options
        else:
            poll_options = self.options
        for option in poll_options:
            description += '\n {} {}'.format(self.reactions[count], option)
            count += 1
        print(description)
        embed = discord.Embed(title=self.event.get_title_poll(),
                              description=''.join(description))
        message = await ctx.send(embed=embed)
        for reaction in self.reactions[:len(poll_options)]:
            await message.add_reaction(reaction)
        embed.set_footer(text='Message ID: {}'.format(message.id))
        await message.edit(embed=embed)
        self.event.set_id(message.id)
        # self.events.append(lunch)

    @commands.command()
    async def count_votes(self, ctx):
        votes = {}
        winners = []
        message = await ctx.fetch_message(self.event.get_id())
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
            if i in max_keys:
                winners.append(j)
        await self.show_results(ctx, winners)

    @commands.command()
    async def count_votes_manual(self, ctx, poll_id):
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
            if i in max_keys:
                winners.append(j)
        await self.show_results(ctx, winners)

    async def show_results(self, ctx, winners):

        if len(winners) > 1:
            ctx.send("Its a tie")
        else:
            self.event.set_winner(winners[0])
            print(winners[0])
            print(self.event.get_winner())
            embed = discord.Embed(title="Poll finished",
                                  description=self.event.get_title_results())
            await ctx.send(embed=embed)
        await self.set_reminder(ctx)

    @commands.command()
    async def set_reminder(self, ctx):
        if self.event is None:
            await ctx.send("No poll created")
            return
        alarm = self.event.get_alarm()
        form = "%H:%M"
        print("set_reminder")
        # curr = datetime.strftime(datetime.now(), form)
        print(datetime.now())
        print(timedelta(0, 10))
        curr = datetime.now() + timedelta(0, 10)
        print(curr)
        print(alarm)
        # diff = datetime.strptime(curr)
        t1 = datetime.strptime(alarm, "%H:%M")
        t2 = datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M")
        diff = (t1 - t2).total_seconds()
        print(diff)
        time.sleep(diff)
        print("reminder")
        print(self.event.get_title_results())
        embed = discord.Embed(title="Reminder",
                              description=self.event.get_title_results())
        await ctx.send(embed=embed)
# Have a timer that automatically scores the polls, then clears the poll
# Have an optional arg for the id for manual execution
# Set alarm for lunch
# Title, description
def setup(client):
    client.add_cog(Poll(client))
