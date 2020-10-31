# -----------------------------------------------------------------------------------------------
# Description: Error Handler forked from internet (creds to MrBot)
# -----------------------------------------------------------------------------------------------

import discord
import sys
import traceback

from utils import botUtils
from discord.ext import commands

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()  # TODO: Test this
    async def on_error(self, event_method, *args, **kwargs):
        self.bot.logger.error("Ignoring exception in %s.", event_method)
        self.bot.logger.error("Unexpected exception:", exc_info=sys.exc_info())

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # If command has a local error handler, let that one process the error
        if hasattr(ctx.command, "on_error"):
            return

        # Get the original exception or if nothing is found keep the exception
        error = getattr(error, "original", error)

        # Check for various error types and return a custom reponse
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(
                f"You missed the `{error.param}` parameter. Run `{ctx.prefix}"
                f"help {ctx.command}` for more information on how to use this command."
            )

        if isinstance(error, commands.TooManyArguments):
            return await ctx.send(f"You passed too many arguments to the command `{ctx.command}`. Run `{ctx.prefix}help {ctx.command}` for more information on how to use this command.")

        if isinstance(error, commands.BadArgument):
            return await ctx.send(f"You passed a bad argument to the command `{ctx.command}`.")

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.PrivateMessageOnly):
            return await ctx.send(f"The command `{ctx.command}` can only be used in DMs.")

        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send(f"The command `{ctx.command}` cannot be used in DMs.")
            except discord.Forbidden:
                return

        if isinstance(error, commands.NotOwner):
            return await ctx.send(f"The command `{ctx.command}` can only be used by my owner.")

        if isinstance(error, commands.MissingPermissions):
            missing_perms = ""
            for perm in error.missing_perms:
                missing_perms += f"\n> {perm}"
            return await ctx.send(f"You don't have the following permissions required to run the command `{ctx.command}`.\n{missing_perms}")

        if isinstance(error, commands.BotMissingPermissions):
            missing_perms = ""
            for perm in error.missing_perms:
                missing_perms += f"\n> {perm}"
            return await ctx.send(f"I am missing the following permissions to run the command `{ctx.command}`.\n{missing_perms}")

        if isinstance(error, commands.DisabledCommand):
            return await ctx.send(f"The command `{ctx.command}` is currently disabled.")

        if isinstance(error, commands.CommandOnCooldown):
            if error.cooldown.type == commands.BucketType.default:
                return await ctx.send(f"The command `{ctx.command}` is on cooldown for the whole bot, retry in `{botUtils.convert_seconds_friendly(error.retry_after)}`.")
            if error.cooldown.type == commands.BucketType.user:
                return await ctx.send(f"The command `{ctx.command}` is on cooldown for you, retry in `{botUtils.convert_seconds_friendly(error.retry_after)}`.")
            if error.cooldown.type == commands.BucketType.guild:
                return await ctx.send(f"The command `{ctx.command}` is on cooldown for this guild, retry in `{botUtils.convert_seconds_friendly(error.retry_after)}`.")
            if error.cooldown.type == commands.BucketType.channel:
                return await ctx.send(f"The command `{ctx.command}` is on cooldown for this channel, retry in `{botUtils.convert_seconds_friendly(error.retry_after)}`.")
            if error.cooldown.type == commands.BucketType.member:  # Different from user apparently
                return await ctx.send(f"The command `{ctx.command}` is on cooldown for you, retry in `{botUtils.convert_seconds_friendly(error.retry_after)}`.")
            if error.cooldown.type == commands.BucketType.category:
                return await ctx.send(f"The command `{ctx.command}` is on cooldown for this category of channels, retry in `{botUtils.convert_seconds_friendly(error.retry_after)}`.")
            if error.cooldown.type == commands.BucketType.role:  # TODO: Edit this so that the role on cooldown is actually mentioned (if possible)
                return await ctx.send(f"The command `{ctx.command}` is on cooldown for your role, retry in `{botUtils.convert_seconds_friendly(error.retry_after)}`.")

        # Print the error and traceback if it doesnt match any of the above.
        print(f"\n[BT] Ignoring exception in command {ctx.command}:")
        traceback.print_exception(type(error), error, error.__traceback__)
        # Print traceback to logger perhaps? Or maybe to an actual channel

    # An example of command specific errors
    # @commands.command(name='repeat', aliases=['mimic', 'copy']) # Use the following as templates
    # async def do_repeat(self, ctx, *, inp: str):
    #     await ctx.send(inp)

    # @do_repeat.error
    # async def do_repeat_handler(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         if error.param.name == 'inp':
    #             await ctx.send("You forgot to give me input to repeat!")

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
