# Project Name: NBC Boterator
# Author: Lukadd.16#8870
# Changelog: 1.0.0 - Initial Release, heavily based upon my now defunct
#                    JARVIS Bot Project

import config
import discord
import logging
import os

from discord.ext import commands
from datetime import datetime
from utils import botUtils

# Bot Logs Guide:
# BT = Bot status message
# DB = Database status messages
# DEBUG = Detailed information, of interest only when diagnosing problems
# INFO = Confirmation that things are working as expected
# WARNING = An indication that something unexpected happened, or indicative of
#           some problem in the near future (e.g. ‘disk space low’).
#           The software is still working as expected.
# ERROR = Due to a more serious problem, the software has not been able to
#         perform some function.
# CRITICAL = A serious error, indicating that the program itself may be unable
#            to continue running.

# If it does not exist already, create a directory where we will store logs
# generated by the logging module
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

# TODO: Figure out how want to manage log files, keep appending to same file?
#       Create new file at each boot up? Or implement "rotating" logger where
#       new log file is created whenever old one reaches certain size or age.

# Define required Discord API intents
intents = discord.Intents.default()
intents.members = True
intents.presences = True

class NBCBoterator(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.BOT_PREFIX),
            help_command=None,
            intents=intents,
            reconnect=True
        )

        self.app_info = None
        self.config = config
        self.myutils = botUtils
        self.status_channel = None
        self.log_channel = None
        self.log_file_name = None
        self.launch_time = datetime.utcnow()
        self.bot_status = None
        self.db_ready = False
        self.db = None  # Unused

        self.default_presence = discord.Activity(
            type=discord.ActivityType.listening,
            name=f"{self.config.BOT_PREFIX}help"
        )

        # TODO: Add db_connect() method call here
        self.bot_startup()

    # Using static log file name for now, in future set up a custom
    # FileHandler that rotates the file (after it reachs a certain size)
    def bot_startup(self):
        log_file_name = "NBC_Primary.log"
        self.log_file_path = os.path.join(log_dir, f"{log_file_name}")

        # Fetch logger string level defined in our config file
        level_text = self.config.LOG_LEVEL.upper()

        # Define logging levels that correspond with string
        # stored in our config file
        logging_levels = {
            "CRITICAL": logging.CRITICAL,
            "ERROR": logging.ERROR,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
        }

        # Convert string to a level used by the logging module,
        # if the string does not match any defined in logging_levels
        # then use INFO as a fallback
        log_level = logging_levels.get(level_text)
        if log_level is None:
            level_text = "INFO"
            log_level = logging.INFO

        # Instantiate logger
        self.logger = logging.getLogger("NBC.main")
        self.logger.setLevel(log_level)
        handler = logging.FileHandler(
            filename=f"{self.log_file_path}",
            encoding="utf-8",
            mode="a"
        )
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] [%(name)s]: %(message)s"
            )
        )
        self.logger.addHandler(handler)
        self.logger.debug(
            "Sucessfully configured logging module with the "
            "following parameters:"
        )
        self.logger.debug(f"> Logging Level: {level_text}")
        self.logger.debug(f"> File Path: {self.log_file_path}")

        # Load cogs defined in our config file
        for extension in self.config.BOT_EXTENSIONS:
            try:
                self.load_extension(extension)
                print(f"[COG] SUCCESS - {extension}")

            except commands.ExtensionNotFound:
                print(f"[COG] FAILED - {extension}")

        # self.login(config.BOT_TOKEN)
        # self.connect()

    def bot_close(self):
        self.status_channel.send(
            f"`{self.user}` has been manually interrupted via keystroke"
        )
        delta_uptime = datetime.utcnow() - self.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        self.status_channel.send(
            f"Total Uptime was: `{days}d, {hours}h, {minutes}m, {seconds}s`"
        )
        print("\n[BT] Interrupt Shutdown Successful")
        self.logout()

    def run(self):
        try:
            self.loop.run_until_complete(
                self.start(
                    self.config.BOT_TOKEN
                )
            )
        except KeyboardInterrupt:
            self.logger.critical(
                "Keyboard Interrupt Detected"
            )
        except discord.LoginFailure:
            self.logger.critical(
                "Invalid Token"
            )
        except Exception as e:
            self.logger.critical(
                "Fatal Exception",
                e,
                exc_info=True  # Append exception information to log message
            )
        finally:
            self.logger.warning(
                ">>>SHUTTING DOWN<<<"
            )
            self.loop.run_until_complete(
                self.logout()
            )

    # Perform a few tasks when the bot is ready to accept commands
    async def on_ready(self):
        # Retrieve application info from Discord
        self.app_info = await self.application_info()

        # Retrieve the IDs for the discord logging and status channels from our
        # config file and assign them to previously declared class variables
        self.status_channel = self.get_channel(self.config.STATUS_CHANNEL_ID)
        self.log_channel = self.get_channel(self.config.EVENTS_CHANNEL_ID)

        self.logger.info(" - ")
        self.logger.info("Client is ready.")
        self.logger.info(f"Logged in as {self.user.name} - ID: {self.user.id}")
        self.logger.info(f"Discord.py Version - {discord.__version__}")
        self.logger.info("Owner(s) - WIP")
        self.logger.info(f"Prefix - {self.config.BOT_PREFIX}")
        self.logger.info(" - ")

        print(f"\n[BT] Logged in as: {self.user.name} - {self.user.id}")
        print(f"[BT] Library Version: {discord.__version__}")

        print("\n[BT] I have access to the following guilds (as of bootup):")
        for guild in self.guilds:
            print(guild.name)

        await self.change_presence(
            status=discord.Status.online,
            activity=self.default_presence
        )

        await self.status_channel.send(
            f"`{self.user}` has successfully connected to Discord"
        )

        # Connect to DB (refer to MrBot code)
        # try:
        # [Insert code here]

        # Insert database checks here for server configs
        # (checks being to see if bot joined any new servers during downtime)
        # After checks complete, change db_ready to True
        # except: [Insert database connection failed error, exception as e]

    async def on_resume(self):
        await self.status_channel.send(
            f"`{self.user}'s` connection has been resumed."
        )
        print("\n[BT] Connection Resumed")

    async def on_disconnect(self):
        print("\n[BT] Disconnected")

    # Guild events that we respond to
    async def on_guild_join(self, guild):
        await self.log_channel.send(
            f"`{self.user}` has been added to `{guild}` with"
            "`{guild.member_count} members`"
        )

    async def on_guild_remove(self, guild):
        await self.log_channel.send(
            f"`{self.user}` has been removed from `{guild}` :("
        )


NBCBoterator().run()
