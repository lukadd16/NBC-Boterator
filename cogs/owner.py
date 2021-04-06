# Description: Cog that houses owner-only commands (inspired by EvieePy)

import app_logger
import config
import discord

from datetime import datetime
from discord.ext import commands
from importlib import reload as importlib_reload
from typing import Optional
from utils import tools

logger = app_logger.get_logger(__name__)


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self._last_result = None

    def cog_unload(self):
        for h in logger.handlers:
            logger.removeHandler(h)

    # Overwrite cog_check method
    # Commands within this cog can only be used by the bot owner
    async def cog_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            raise commands.NotOwner()
        return True

    # Load an individual cog; use dot path notation -> Ex: jj load cogs.help
    @commands.command(aliases=["load", "loadcog"])
    async def cload(self, ctx, *, cog: str):
        # Convert input to proper path.of.cog format
        # In our case the root folder is named cogs
        cog = "cogs.{}".format(cog)

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            logger.info(f"Loaded cog ({cog})")
            await ctx.send("**`SUCCESS`**")

    # Unload an individual cog
    @commands.command(aliases=["unload", "unloadcog"])
    async def cunload(self, ctx, *, cog: str):
        cog = "cogs.{}".format(cog)

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            logger.info(f"Unloaded cog ({cog})")
            await ctx.send("**`SUCCESS`**")

    # Reload an individual cog, config file or tools.py module into memory
    @commands.group(aliases=["reload"])
    async def creload(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "You did not specify a subcommand. Valid subcommands "
                "are:\n>>> `all`\n`cog`\n`config`\n`tools`"
            )

    # Reload all cogs + tools.py module + config file
    # Useful when pushing non-breaking changes to the production server that
    # span across multiple files
    @creload.command()
    async def all(self, ctx):
        try:
            for extension in config.BOT_EXTENSIONS:
                self.bot.reload_extension(extension)
            importlib_reload(config)
            importlib_reload(tools)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            logger.info(
                "Reloaded configuration file, tools module & all cogs"
            )
            await ctx.send("**`SUCCESS`**")

    @creload.command()
    async def cog(self, ctx, *, cog: str):
        cog = "cogs.{}".format(cog)

        try:
            self.bot.reload_extension(cog)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            logger.info(f"Reloaded cog ({cog})")
            await ctx.send("**`SUCCESS`**")

    # Reloads the bot's config file into memory without needing to restart the
    # bot (finally!)
    @creload.command()
    async def config(self, ctx):
        try:
            importlib_reload(config)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            logger.info("Reloaded configuration file")
            await ctx.send("**`SUCCESS`**")

    # Reloads the tools.py module into memory
    @creload.command()
    async def tools(self, ctx):
        try:
            importlib_reload(tools)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            logger.info("Reloaded tools module")
            await ctx.send("**`SUCCESS`**")

    # Gracefully shutdown the bot; calculate & report uptime
    @commands.command(aliases=["kill", "terminate"])
    async def shutdown(self, ctx, *, reason: Optional[str] = None):
        await ctx.send("Shutting down...")

        if reason is None:
            reason = "Manual Shutdown Triggered - No reason provided"

        logger.info("Manual Shutdown Triggered")

        # Calculate time elapsed since boot
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        delta_uptime_seconds = delta_uptime.total_seconds()

        # Convert delta into human readable format
        total_uptime = tools.seconds_to_str(delta_uptime_seconds)

        # Report uptime & shutdown
        embed = discord.Embed(
            title=f"Status: {config.EMOJI_OFFLINE}",
            description=f"`{self.bot.user}` has been disconnected",
            colour=config.DISC_OFFLINE_COLOUR,
            timestamp=ctx.message.created_at
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
            icon_url=self.bot.user.avatar_url
        )
        await self.bot.status_channel.send(embed=embed)

        print("\n[BT] Disconnected Gracefully")
        await self.bot.logout()

    # Manually send status embed message for use when announcing planned
    # downtime, known issues, etc.
    @commands.command()
    async def status(self, ctx, status: str, *, reason: str):
        # TODO: Move to tools.py
        if status.lower() == "online":
            status = config.EMOJI_ONLINE
            embed_colour = config.DISC_ONLINE_COLOUR
        elif status.lower() == "idle":
            status = config.EMOJI_IDLE
            embed_colour = config.DISC_IDLE_COLOUR
        elif status.lower() == "dnd":
            status = config.EMOJI_DND
            embed_colour = config.DISC_DND_COLOUR
        elif status.lower() == "offline":
            status = config.EMOJI_OFFLINE
            embed_colour = config.DISC_OFFLINE_COLOUR
        elif status.lower() == "stream":
            status = config.EMOJI_STREAM
            embed_colour = config.DISC_STREAM_COLOUR
        else:
            raise commands.BadArgument()

        embed = discord.Embed(
            title=f"Status: {status}",
            description=f"{reason}",
            colour=embed_colour,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(
            text="NBC Boterator Dev Team",
            icon_url=self.bot.user.avatar_url
        )
        await self.bot.status_channel.send(embed=embed)
        await ctx.send("**`SUCCESS`**")

        logger.info(
            "Status Report with following details sent:"
        )
        logger.info(
            f"> Discord Status: {status.upper()}"
        )
        logger.info(
            f"> Reason: {reason}"
        )

    # If and when DB is added, manual SQL execution command can be put here


def setup(bot):
    bot.add_cog(OwnerCog(bot))
