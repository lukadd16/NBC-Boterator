# Description: Cog that creates a task which changes the bot's status on a timed interval

# TODO: Test that the presences are being changed in order

import asyncio
import discord
import discord.utils

from discord.ext import commands, tasks

class StatusLoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.presence_index = 0  # For use in the counted loop
        self.presence_updater.start()  # Ignore the error, it works
        # self.home_server = bot.get_guild(bot.config.HOME_SERVER_ID)  # CBA to figure this out

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
        self.bot.logger.debug("Changing Bot Presence")

        if self.presence_index == (len(presences) - 1):
            self.presence_index = 0
            self.bot.logger.debug("Resetting counter")
        else:
            self.presence_index += 1
            # self.bot.logger.debug(self.presence_index)

        await self.bot.change_presence(activity=presences[self.presence_index])

    @tasks.loop(seconds=900, reconnect=True)
    async def presence_updater(self):
        self.bot.logger.debug("Switching to next presence.")
        await self.set_presence()

    @presence_updater.before_loop
    async def before_loop_presence(self):
        await self.bot.wait_until_ready()

        # await self.set_presence()

        await asyncio.sleep(5)
        self.bot.logger.debug("Starting presence loop.")

    # Could potentially get rid of this entire cog and replace it with an
    # events cog (for updating bot's stats to listing sites maybe?)
    # async def activity_updater(self):
    #     await self.bot.wait_until_ready()
    #     while True:
    #         if self.activity_index + 1 >= len(self.bot.config.activity):
    #             self.activity_index = 0
    #         else:
    #             self.activity_index = self.activity_index + 1
    #         await self.bot.change_presence(
    #             activity=discord.Game(
    #                 name=self.bot.config.activity[self.activity_index]
    #             )
    #         )
    #         await asyncio.sleep(12)

    # def cog_unload(self):
    #     self.bot.change_status.cancel()

    # @change_status.before_loop
    # async def before_change_status(self):
    #     await self.bot.wait_until_ready()

    # @change_status.after_loop
    # async def after_change_status(self):
    #     await self.bot.change_status()

def setup(bot):
    bot.add_cog(StatusLoop(bot))
