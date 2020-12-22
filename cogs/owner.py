# Description: Cog that houses owner only commands (inspired by EvieePy)

from datetime import datetime
from discord.ext import commands
from importlib import reload as importlib_reload
from utils import botUtils

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    # Load an individual cog; use dot path notation -> Ex: jj load cogs.help
    @commands.command(aliases=["load", "loadcog"])
    @commands.is_owner()
    async def bog_load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    # Unload an individual cog; use dot path notation
    @commands.command(aliases=["unload", "unloadcog"])
    @commands.is_owner()
    async def bog_unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    # Reload an individual cog; use dot path notation
    @commands.command(aliases=["reload", "reloadcog"])
    @commands.is_owner()
    async def bog_reload(self, ctx, *, cog: str):
        try:
            self.bot.reload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    # Reloads the bot's config file into memory without needing to restart the
    # bot (finally!)
    @commands.command()
    @commands.is_owner()
    async def reloadconf(self, ctx):
        try:
            importlib_reload(self.bot.config)
        except Exception as e:
            await ctx.send(f'**`ERROR`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    # Reloads the bot's botUtils module into memory
    @commands.command()
    @commands.is_owner()
    async def reloadutils(self, ctx):
        try:
            importlib_reload(botUtils)
        except Exception as e:
            await ctx.send(f'**`ERROR`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    # Reload all cogs, utils & config file, useful when pushing non-breaking
    # changes to the production server that span across multiple cogs
    @commands.command(aliases=["reload_all", "rall"])
    @commands.is_owner()
    async def bog_reload_all(self, ctx):
        try:
            for extension in self.bot.config.BOT_EXTENSIONS:
                self.bot.reload_extension(extension)
            importlib_reload(self.bot.config)
            importlib_reload(botUtils)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    # Gracefully shutdown the bot; calculate and report uptime
    @commands.command(aliases=["kill", "terminate"])
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        await self.bot.status_channel.send(
            f"`{self.bot.user}` has been disconnected"
        )
        # Very hacky way of doing it but it'll do for now
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        delta_uptime_seconds = delta_uptime.total_seconds()

        # hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        # minutes, seconds = divmod(remainder, 60)
        # days, hours = divmod(hours, 24)
        await self.bot.status_channel.send(
            'Total Uptime was: '
            f'`{botUtils.convert_seconds_friendly(delta_uptime_seconds)}`'
        )
        print("\n[BT] Disconnected Gracefully")
        await self.bot.logout()

    # If and when DB is added, manual SQL execution command can be put here

def setup(bot):
    bot.add_cog(OwnerCog(bot))
