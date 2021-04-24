import functools
import threading
import time

import app_logger
import asyncio
import config
import configparser
import discord
import discord.utils
import os

from discord.ext import commands, tasks

logger = app_logger.get_logger(__name__)


class Disboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = self._init_db()

    def cog_unload(self):
        for h in logger.handlers:
            logger.removeHandler(h)

    # Database configuration
    def _init_db(self):
        # Construct the file path to our .INI file
        cwd = os.getcwd()
        db_dir = cwd + r"\data\db"
        db_file_name = "settings.ini"
        db_file_path = os.path.join(db_dir, db_file_name)
        logger.info("INI File Path: {}".format(db_file_path))

        # Initialize a new ConfigParser using the obtained file path
        conf = configparser.ConfigParser()
        try:
            with open(db_file_path) as f:
                conf.read_file(f)
        except IOError:
            logger.warning("The .INI settings file could not be configured, this cog will not function properly.")
            conf = None

        return conf

    # Get the TextChannel that we will be sending bump notification messages to
    def _get_notif_channel(self) -> discord.TextChannel:
        # Get the TextChannel we want to send the notification to
        target_channel = discord.utils.get(
            self.bot.get_all_channels(),
            guild__name="Jarvis Bot",
            id=config.BOTS_CHANNEL
        )
        logger.debug(
            "Fetched channel {0.name} with ID {0.id} in guild {1.name} ({1.id})".format(
                target_channel,
                target_channel.guild
            )
        )
        return target_channel

    async def check_description(self, embed: dict):
        try:
            description = embed.get("description")
        except KeyError:
            return

        # Check if the string indicating server bump completed is in the embed's description
        if config.DISBOARD_SUCCESS in description.lower():
            # A user just bumped the server, call our method to send the notification message (in two hours time)
            logger.info("Calling future !d bump notification")
            await self.send_notif_msg()

    async def send_notif_msg(self):
        # We want to wait two hours before sending the message
        await asyncio.sleep(15)  # TODO: change delay to 7200 seconds after testing

        logger.debug("Server can be bumped")

        # Send message to the #bot-commands channel notifying members that the server can now be bumped
        await self._get_notif_channel().send("*Beep Boop* {0} The server can now be bumped {0}".format(config.EMOJI_ROBOT))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        author = message.author
        origin = message.channel
        embeds = message.embeds

        # Load state of config settings
        notify_enabled = self.settings["disboard"].getboolean("notify_enabled")
        bump_event_active = self.settings["disboard"].getboolean("bump_event_active")

        # We want to ignore messages from the bot itself (to avoid infinite recursion)
        # if author.id is self.bot.user.id:
        #     return

        # If the message has an embed, check its description to see if it matches the one indicating the server bump was successful
        if embeds is not None and notify_enabled is True:
            embed = embeds[0]
            as_dict = embed.to_dict()
            await self.check_description(as_dict)

        # Checks for the bump event would go here...

    # Will send an embed in #bot-commands that is identical to the one disboard's bot would send upon successful bump of the server
    @commands.command()
    async def send_fake_bump(self, ctx):
        # Fetch the message containing the embed we are going to copy

        guild = discord.utils.get(  # Temporary
            self.bot.guilds,
            name="Northbridge Café"
        )
        target = discord.utils.get(
            guild.text_channels,
            id=676502452694155324
        )

        disboard_msg = await target.fetch_message(835144761194315776)

        # Get the discord.Embed object from the message
        embed = disboard_msg.embeds[0]

        # Send this embed to the target channel
        await self._get_notif_channel().send(embed=embed)


def setup(bot):
    bot.add_cog(Disboard(bot))
