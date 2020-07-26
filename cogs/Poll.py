import sys
sys.path.insert(0, '../')
import discord
from discord.ext import commands
from EventTopic import Lunch
import time
from datetime import datetime, timedelta
from YelpAPI import Yelp
import re


"""
Handles the polling.
"""
class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.options = []
        self.current = None
        self.reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣']
        self.event = None
        self.yelp = Yelp()

    """
    Creates a new poll object.
    """
    @commands.command()
    async def create_poll(self, ctx, poll):
        if poll.lower() == "lunch":
            self.event = Lunch()
            await ctx.send("Lunch poll created")
        else:
            await ctx.send("Not a valid poll type")

    """
    Adds an poll option.
    """
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
    async def add_yelp(self, ctx, option):
        if len(option) != 22:
            await ctx.send("not a valid yelp business id")
        else:
            req = self.yelp.id_search(option)
            business = self.yelp.parse_business(req)
            if business not in self.options:
                self.options.append(business)
    """
    Removes a poll option.
    """
    @commands.command()
    async def del_option(self, ctx, option):
        if option in self.options:
            self.options.remove(option)
            await ctx.send(f"removed {option}")
        else:
            await ctx.send(f"{option} does not exist")

    """
    Display the options
    """
    @commands.command()
    async def show_options(self, ctx):
        option_str = " ".join(self.options)
        print(option_str)
        await ctx.send(f"{option_str}")

    """
    Poll the chat
    """
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
            if isinstance(option, dict):
                description += '\n {} {}'.format(self.reactions[count],
                                                  option["name"])
            else:
                description += '\n {} {}'.format(self.reactions[count],
                                                  option)
            count += 1
        print(f"desc {description}")
        embed = discord.Embed(title=self.event.get_title_poll(),
                              description=''.join(description))
        message = await ctx.send(embed=embed)
        for reaction in self.reactions[:len(poll_options)]:
            await message.add_reaction(reaction)
        embed.set_footer(text='Message ID: {}'.format(message.id))
        await message.edit(embed=embed)
        self.event.set_id(message.id)
        # self.events.append(lunch)

    """
    Fetches the embeded poll, counts the votes, and calls show results.
    """
    @commands.command()
    async def count_votes(self, ctx):
        votes = {}
        winners = []
        message = await ctx.fetch_message(self.event.get_id())
        embed_desc = message.embeds[0].description.strip()
        # embed_desc = embed_desc.replace("\n", "")
        print(embed_desc)
        temp_list = embed_desc.splitlines()
        temp_list = [x.strip() for x in temp_list]
        print(temp_list)
        print(temp_list[0][0:1])
        # temp_list = re.split("1⃣'2⃣'3⃣'4⃣'5⃣'", embed_desc)
        # print(temp_list)
        options = {temp_list[x][0:2]: temp_list[x][2:] for x in range(0, len(
            temp_list))}
        for reaction in message.reactions:
            # print(reaction)
            # print(reaction.emoji)
            if reaction.emoji in options:
                reacters = await reaction.users().flatten()
                votes[reaction.emoji] = len(reacters)
                # print(reaction)

        print(votes)
        max_value = max(votes.values())
        print(max_value)
        max_keys = [key for key, value in votes.items() if value == max_value]
        for i, j in options.items():
            if i in max_keys:
                winners.append(j.strip())
        await self.show_results(ctx, winners)

    """
    Counts the votes using the poll id
    """
    @commands.command()
    async def count_votes_manual(self, ctx, poll_id):
        votes = {}
        winners = []
        message = await ctx.fetch_message(self.self.event.get_id())
        print(message)
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

    """
    Display the winner as an embed.
    """
    async def show_results(self, ctx, winners):
        if len(winners) > 1:
            ctx.send("Its a tie")
        else:
            self.event.set_winner(winners[0])
            print(winners[0])
            embed = discord.Embed(title="Poll finished",
                                  description=self.event.get_title_results())
            for option in self.options:
                print(option)
                if isinstance(option, dict) and option["name"] == winners[0]:
                    embed = self.yelp_embed(option, embed)
            print(self.event.get_winner())
            await ctx.send(embed=embed)
        await self.set_reminder(ctx, embed)

    """
    Adds fields if option is an yelp option.
    """
    def yelp_embed(self, business, embed):
        # embed = discord.Embed(title=business["name"],
        #                       description=self.event.get_title_results())
        embed.set_image(url=business["image"])
        embed.add_field(name="Name", value=business["name"],
                        inline=True)
        embed.add_field(name="Link", value=business["url"],
                        inline=True)
        embed.add_field(name="Address", value=business["address"],
                        inline=True)
        return embed

    """
    Sets the reminder for lunch
    """
    @commands.command()
    async def set_reminder(self, ctx, embed):
        if self.event is None:
            await ctx.send("No poll created")
            return
        alarm = self.event.get_alarm()
        form = "%H:%M"
        print("set_reminder")
        # curr = datetime.strftime(datetime.now(), form)
        print(datetime.now())
        print(timedelta(0, 10))
        curr = datetime.now() #+ timedelta(0, 10*60)
        print(curr)
        print(alarm)
        # diff = datetime.strptime(curr)
        t1 = datetime.strptime(alarm, "%H:%M")
        t2 = datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M")
        diff = (t1 - t2).total_seconds() - 10 * 60
        print(f"diff {diff}")
        time.sleep(diff)
        print("reminder")
        print(self.event.get_title_results())
        embed.title = "Reminder"
        await ctx.send(embed=embed)


# Have a timer that automatically scores the polls, then clears the poll
# Have an optional arg for the id for manual execution
# Set alarm for lunch
# Title, description

def setup(client):
    client.add_cog(Poll(client))
