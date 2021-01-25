# Description: Cog that creates a task to change bot status on a timed interval

import app_logger
import asyncio
import discord
import discord.utils

from discord.ext import commands, tasks

logger = app_logger.get_logger(__name__)


class StatusLoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.presence_index = 0  # For use in the counted loop
        self.presence_updater.start()  # Ignore the error, it works
        # self.home_server = bot.get_guild(bot.config.HOME_SERVER_ID)

    def cog_unload(self):
        for h in logger.handlers:
            logger.removeHandler(h)

        self.presence_updater.cancel()

    async def set_presence(self):
        home_server = self.bot.get_guild(self.bot.config.HOME_SERVER_ID)

        presences = [
            discord.Activity(
                type=discord.ActivityType.listening,
                name=f"prefix {self.bot.config.BOT_PREFIX}"
            ),
            discord.Activity(
                type=discord.ActivityType.listening,
                name=f"{self.bot.config.BOT_PREFIX}help"
            ),
            discord.Activity(
                type=discord.ActivityType.watching,
                name="Dyno kinda sus"
            ),
            discord.Activity(
                type=discord.ActivityType.watching,
                name="Northbridge Café"
            ),
            discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(home_server.members)} Members"
            ),
            discord.Activity(
                type=discord.ActivityType.playing,
                name="Plague Inc."
            ),
            discord.Activity(
                type=discord.ActivityType.playing,
                name="northbridgecafe.tk"
            )
        ]
        logger.debug("Bot Presence Set")

        if self.presence_index == (len(presences) - 1):
            self.presence_index = 0
            logger.debug("Resetting counter")
        else:
            self.presence_index += 1
            logger.debug("Current Presence Index: %s", self.presence_index)

        await self.bot.change_presence(activity=presences[self.presence_index])

    @tasks.loop(seconds=900, reconnect=True)
    async def presence_updater(self):
        logger.info("Switching to next presence")
        await self.set_presence()

    @presence_updater.before_loop
    async def before_loop_presence(self):
        await self.bot.wait_until_ready()

        # await self.set_presence()

        await asyncio.sleep(5)
        logger.debug("Starting presence loop")


def setup(bot):
    bot.add_cog(StatusLoop(bot))
