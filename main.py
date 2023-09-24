import os
import discord
from discord.ext import commands, tasks
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            help_command=commands.DefaultHelpCommand(dm_help=True)
        )

    async def on_ready(self):
        logging.info(f"Logged in as {self.user}")
        await self.load_extensions()

    async def load_extensions(self):
        cogs_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "cogs")
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py"):
                try:
                    self.load_extension(f"cogs.{filename[:-3]}")
                    logging.info(f"Loaded cog: {filename[:-3]}")
                except Exception as e:
                    logging.error(f"Failed to load cog {filename[:-3]}: {e}")

    @tasks.loop(seconds=60, count=1)
    async def update_bot_status(self):
        server_count = len(self.guilds)
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"{server_count} servers")
        await self.change_presence(activity=activity)
        self.update_bot_status.stop()

    @update_bot_status.before_loop
    async def before_update_bot_status(self):
        await self.wait_until_ready()

def main():
    bot = MyBot()
    bot.run(os.getenv("TOKEN"))

if __name__ == "__main__":
    main()
