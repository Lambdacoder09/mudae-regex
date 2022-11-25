# cogs / re.py
import re
from discord.ext import commands


class mm(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mm(self, ctx, *, args):
        rank_re = re.compile(r'(💞.*$)|(✅.*$)|(#(.*?)- )|(\(Soulkeys:.*\))', flags=re.MULTILINE)
        args = args.replace('**', '').replace('❌ ', '').replace('⭐ ', '')
        args = rank_re.sub("", args)
        new_string = re.sub("\n", " $", args).replace("  ", " ")

        count = len(new_string.split('$'))
        await ctx.send(f"Total number of characters: {count}\n```\n{new_string}\n```")


async def setup(client):
    await client.add_cog(mm(client))
