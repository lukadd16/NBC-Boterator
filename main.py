# Project Name: NBC Boterator
# Author: Lukadd.16#8870

import app_logger
import config
import discord

from discord.ext import commands
from datetime import datetime
from utils import tools

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

logger = app_logger.get_logger(__name__)

# Define Discord API intents that the bot needs
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
        self.status_channel = None
        self.log_channel = None
        # self.partners_channel = None
        self.launch_time = datetime.utcnow()
        self.bot_status = None
        self.db_ready = False
        self.db = None  # Unused

        self.default_presence = discord.Activity(
            type=discord.ActivityType.listening,
            name=f"{config.BOT_PREFIX}help"
        )

        # TODO: Add db_connect() method call here
        self.bot_startup()

    def bot_startup(self):
        logger.debug("Loading cogs...")

        # Load cogs defined in our config file
        for extension in config.BOT_EXTENSIONS:
            try:
                self.load_extension(extension)
                print(f"[COG] SUCCESS - {extension}")

            except commands.ExtensionNotFound:
                print(f"[COG] FAILED - {extension}")
                logger.error(f"Failed to load cog ({extension})")

        # self.login(config.BOT_TOKEN)
        # self.connect()

    async def bot_close(self):
        # Calculate time elapsed since boot
        delta_uptime = datetime.utcnow() - self.launch_time
        delta_uptime_seconds = delta_uptime.total_seconds()

        # Convert delta into human readable format
        total_uptime = tools.seconds_to_str(delta_uptime_seconds)

        reason = "Manual Shutdown Triggered Via Keyboard Interrupt"

        # Report uptime & shutdown
        embed = discord.Embed(
            title=f"Status: {config.EMOJI_OFFLINE}",
            description=f"`{self.user}` has been disconnected",
            colour=config.DISC_OFFLINE_COLOUR,
            timestamp=datetime.utcnow()
        )
        embed.add_field(
            name="Reason:",
            value=f"{reason}",
            inline=True
        )
        embed.add_field(
            name="Total Uptime was:",
            value=f"{total_uptime}",
            inline=True
        )
        embed.set_footer(
            text="NBC Boterator Dev Team",
            icon_url=self.app_info.icon_url
        )
        await self.status_channel.send(embed=embed)

        print("\n[BT] Interrupt Shutdown Successful")
        await self.logout()

    def run(self):
        try:
            self.loop.run_until_complete(
                self.start(
                    config.APP_TOKEN
                )
            )
        except KeyboardInterrupt:
            logger.critical(
                "Keyboard Interrupt Detected"
            )
            self.loop.run_until_complete(
                self.bot_close()
            )
        except discord.LoginFailure:
            logger.critical(
                "Invalid Token"
            )
        except Exception as e:
            logger.critical(
                "Encountered Fatal Exception",
                e,
                exc_info=True  # Append exception information to log message
            )
        finally:
            logger.warning(
                ">>>SHUTTING DOWN<<<"
            )
            self.loop.run_until_complete(
                self.logout()
            )

    # Perform a few tasks when the bot is ready to accept commands
    async def on_ready(self):
        logger.debug("on_ready event triggered")

        # Retrieve information about this Discord application
        self.app_info = await self.application_info()

        # Retrieve the IDs for the discord logging and status channels from our
        # config file and assign them to previously declared class variables
        self.status_channel = self.get_channel(config.STATUS_CHANNEL_ID)

        logger.info(" - ")
        logger.info("Client is ready.")
        logger.info(f"Logged in as {self.user.name} - ID: {self.user.id}")
        logger.info(f"Discord.py Version - {discord.__version__}")
        logger.info(
            "Owner - %s#%s",
            self.app_info.owner.name,
            self.app_info.owner.discriminator
        )
        logger.info(f"Prefix - {config.BOT_PREFIX}")
        logger.info(" - ")

        print(f"\n[BT] Logged in as: {self.user.name} - {self.user.id}")
        print(f"[BT] Library Version: {discord.__version__}")

        print("\n[BT] I have access to the following guilds (as of bootup):")
        for guild in self.guilds:
            print(guild.name)

        await self.change_presence(
            status=discord.Status.online,
            activity=self.default_presence
        )

        # Report bootup to status channel
        embed = discord.Embed(
            title=f"Status: {config.EMOJI_ONLINE}",
            description=f"`{self.user}` has successfully connected to Discord",
            colour=config.DISC_ONLINE_COLOUR,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(
            text="NBC Boterator Dev Team",
            icon_url=self.app_info.icon_url
        )
        await self.status_channel.send(embed=embed)

        # Connect to DB (refer to MrBot code)
        # try:
        # [Insert code here]

        # Insert database checks here for server configs
        # (checks being to see if bot joined any new servers during downtime)
        # After checks complete, change db_ready to True
        # except: [Insert database connection failed error, exception as e]

    async def on_resume(self):
        # await self.status_channel.send(
        #     f"`{self.user}'s` connection has been resumed."
        # )
        logger.warning("on_resume event triggered")

    async def on_disconnect(self):
        logger.warning("on_disconnect event triggered")

    # Guild events that we respond to
    async def on_guild_join(self, guild):
        logger.info(
            f"I have been added to {guild} with {guild.member_count} members"
        )

    async def on_guild_remove(self, guild):
        logger.info(
            f"I have been removed from {guild} :("
        )


NBCBoterator().run()
