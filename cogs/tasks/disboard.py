import asyncio
import configparser
import os
from contextlib import suppress
from datetime import datetime

import discord
import discord.utils
from discord.ext import commands

import app_logger
import config

logger = app_logger.get_logger(__name__)


class Disboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = self.init_db()
        self.last_bump_at = None
        self.last_notif_msg = None  # Store the ID of the most recently sent bump notification embed
        self.bump_delay = 7200  # Disboard restricts bumps to once every two hours

    def cog_unload(self):
        for h in logger.handlers:
            logger.removeHandler(h)

    # Database configuration
    @staticmethod
    def init_db():
        # Construct the file path to our .INI file
        cwd = os.getcwd()
        db_dir = os.path.join(cwd, "data", "db")
        db_file_name = "settings.ini"
        db_file_path = os.path.join(db_dir, db_file_name)
        logger.info("INI File Path: {}".format(db_file_path))

        # Initialize a new ConfigParser using the obtained file path
        conf = configparser.ConfigParser()
        try:
            with open(db_file_path) as f:
                conf.read_file(f)
        except IOError:
            logger.warning("The .INI settings file could not be configured.")
            conf = None

        return conf

    # Get the TextChannel that we will be sending bump notification messages to
    def _get_notif_channel(self) -> discord.TextChannel:
        # Get the TextChannel we want to send the notification to
        target_channel = discord.utils.get(
            self.bot.get_all_channels(),
            guild__name="Northbridge Café",
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

        if description is not None:
            # Check if the string indicating server bump completed is in the embed's description
            if config.DISBOARD_SUCCESS in description.lower():
                # A user just bumped the server, keep track of the current time (which would be when
                # the server was last bumped at) and call our method to send the notification message (in two hours time)
                logger.info("Server was bumped")
                self.last_bump_at = datetime.utcnow()

                # Attempt to delete the previous notification message that was sent by the bot
                try:
                    await self.last_notif_msg.delete()
                    logger.info("Deleted most recent bump notification")
                except discord.NotFound as ex:
                    logger.error("The message referenced by last_notif_msg could not be found", ex, exc_info=True)
                except discord.Forbidden as ex:
                    logger.error("Deleting the previous bump notification is Forbidden", ex, exc_info=True)
                except discord.HTTPException as ex:
                    logger.error("HTTPException occurred while trying to delete the previous bump notification", ex, exc_info=True)
                except AttributeError as ex:
                    logger.error("AttributeError when trying to call .delete() on the last_notif_msg field, perhaps it is None?", ex, exc_info=True)
                    logger.debug(f"Contents of last_notif_msg: {self.last_notif_msg}")
                except Exception as ex:
                    logger.error("An uncaught exception occurred while trying to call .delete()", ex, exc_info=True)

                logger.info("Calling future !d bump notification")
                await self.send_notif_msg()
        else:
            return

    async def send_notif_msg(self):
        # We want to wait two hours before sending the message
        await asyncio.sleep(self.bump_delay)

        logger.debug("Server can be bumped")
        logger.debug("Last server bump occurred at: {}".format(self.last_bump_at))

        # Send message to the #bot-commands channel notifying members that the server can now be bumped
        target = self._get_notif_channel()
        embed = discord.Embed(
            title="{0} Beep Boop {0}".format(config.EMOJI_ROBOT),
            description="The server can now be bumped"
                        "\n> How do I bump? Type `!d bump`, simple!",
            colour=2406327,  # This is the embed colour (as a base-10 int) that the disboard bot uses
            timestamp=self.last_bump_at
        )
        embed.set_footer(
            text="Most Recent Bump",
            icon_url=target.guild.icon_url
        )
        msg = await target.send(embed=embed)

        # Store ID of the message we just sent
        self.last_notif_msg = msg

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        author = message.author
        guild = message.guild
        embeds = message.embeds

        # We want to ignore messages from the bot itself (to avoid infinite recursion)
        if author.id == self.bot.user.id:
            return

        # Ensure we are only listening to the bot's home guild
        if guild.id != config.HOME_SERVER_ID:
            return

        # Load state of config settings
        notify_enabled = self.settings["disboard"].getboolean("notify-enabled")
        # bump_event_active = self.settings["disboard"].getboolean("bump-event-active")

        # If the message has an embed, check its description to see if it matches the one indicating the server bump was successful
        if len(embeds) > 0 and notify_enabled is True:
            embed = embeds[0]
            as_dict = embed.to_dict()
            await self.check_description(as_dict)

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
