import discord
from discord.ext import commands


class Activity(commands.Cog):

    def __init__(self, Client):
        self.Client = Client

    @commands.Cog.listener()
    async def on_guild_join(self):
        await self.set_activity()

    @commands.Cog.listener()
    async def on_guild_remove(self):
        await self.set_activity()

    async def set_activity(self):
        server_count = str(len(self.Client.guilds))
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"{server_count} servers")
        await self.Client.change_presence(activity=activity)


async def setup(Client):
    await Client.add_cog(Activity(Client))
