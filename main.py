# main.py
import os

import discord
from discord.ext import commands
from discord.ext import tasks


class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            help_command=commands.DefaultHelpCommand(dm_help=True)
        )

    async def setup_hook(self):  # overwriting a handler
        print(f"\033[31mLogged in as {client.user}\033[39m")
        cogs_folder = f"{os.path.abspath(os.path.dirname(__file__))}/cogs"
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
        print("Loaded cogs")
        # start the task to run in the background
        self.my_background_task.start()

    @tasks.loop(seconds=60, count=1)  # task runs every 60 seconds
    async def my_background_task(self):
        server_count = str(len(self.guilds))
        activity = discord.Activity(type=discord.ActivityType.watching, name=f" {server_count} servers")
        await self.change_presence(activity=activity)
        self.my_background_task.stop()

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


client = Client()
client.run(os.getenv("TOKEN"))
