# Description: Cog that houses owner-only commands (inspired by EvieePy)

import discord

from datetime import datetime
from discord.ext import commands
from importlib import reload as importlib_reload
from typing import Optional
from utils import botUtils


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    # Overwrite cog_check method
    # Commands within this cog can only be used by the bot owner
    async def cog_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            raise commands.NotOwner()
        return True

    # Load an individual cog; use dot path notation -> Ex: jj load cogs.help
    @commands.command(aliases=["load", "loadcog"])
    async def cload(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**")

    # Unload an individual cog
    @commands.command(aliases=["unload", "unloadcog"])
    async def cunload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**")

    # Reload an individual cog, config file or botUtils.py module into memory
    @commands.group(aliases=["reload"])
    async def creload(self, ctx):
        # Handle user input
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "You did not specify a subcommand. Valid subcommands "
                "are:\n>>> `all`\n`cog`\n`config`\n`utils`"
            )

    # Reload all cogs + botUtils.py module + config file
    # Useful when pushing non-breaking changes to the production server that
    # span across multiple files
    @creload.command()
    async def all(self, ctx):
        try:
            for extension in self.bot.config.BOT_EXTENSIONS:
                self.bot.reload_extension(extension)
            importlib_reload(self.bot.config)
            importlib_reload(botUtils)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**")

    @creload.command()
    async def cog(self, ctx, *, cog: str):
        try:
            self.bot.reload_extension(cog)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**")

    # Reloads the bot's config file into memory without needing to restart the
    # bot (finally!)
    @creload.command()
    async def config(self, ctx):
        try:
            importlib_reload(self.bot.config)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**")

    # Reloads the botUtils.py module into memory
    @creload.command()
    async def utils(self, ctx):
        try:
            importlib_reload(botUtils)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**")

    # TODO: Convert keyboard interrupt event to embed as well
    # TODO: Add owner command (name TBD) with same embed structure
    #       & status + reason args but for use in announcing planned downtime,
    #       known issues, etc.
    # Gracefully shutdown the bot; calculate & report uptime
    @commands.command(aliases=["kill", "terminate"])
    async def shutdown(self, ctx, *, reason: Optional[str] = None):
        await ctx.send("Shutting down...")

        if reason is None:
            reason = "Manual Shutdown Triggered - No reason provided"

        # Calculate time elapsed since boot
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        delta_uptime_seconds = delta_uptime.total_seconds()

        # Convert delta into human readable format
        total_uptime = botUtils.convert_seconds_friendly(delta_uptime_seconds)

        # Report uptime & shutdown
        embed = discord.Embed(
            title=f"Status: {self.bot.config.BOT_EMOJI_OFFLINE}",
            description=f"{reason}",
            colour=self.bot.config.DISC_OFFLINE_COLOUR,
            timestamp=ctx.message.created_at
        )
        # embed.set_thumbnail(
        #     url=self.bot.avatar_url
        # )
        embed.add_field(
            name="Total Uptime was:",
            value=f"{total_uptime}",
            inline=True
        )
        embed.set_footer(
            text="NBC Boterator Dev Team",
            icon_url=self.bot.icon_url
        )
        await ctx.channel.send(embed=embed)

        print("\n[BT] Disconnected Gracefully")
        await self.bot.logout()

    # If and when DB is added, manual SQL execution command can be put here


def setup(bot):
    bot.add_cog(OwnerCog(bot))
