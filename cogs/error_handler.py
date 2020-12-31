# Description: Global error handler

import discord
import sys
import traceback

from utils import botUtils
from discord.ext import commands

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, event_method, *args, **kwargs):
        self.bot.logger.error("Ignoring exception in %s.", event_method)
        self.bot.logger.error("Unexpected exception:", exc_info=sys.exc_info())

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # If command has a local error handler, allow it to process the error
        if hasattr(ctx.command, "on_error"):
            return

        # Get the original exception or if nothing is found keep the exception
        error = getattr(error, "original", error)

        # Check for various error types and return a custom reponse
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(
                f"I could not find the required `{error.param}` parameter. "
                f"Run `{ctx.prefix}help {ctx.command}` for more information "
                "on how to use this command."
            )

        if isinstance(error, commands.TooManyArguments):
            return await ctx.send(
                "Too many arguments were passed to the command "
                f"`{ctx.invoked_with}`. Run `{ctx.prefix}help {ctx.command}` "
                "for more information on how to use this command."
            )

        if isinstance(error, commands.BadArgument):
            return await ctx.send(
                "A bad argument was passed to the command "
                f"`{ctx.invoked_with}`."
            )

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.PrivateMessageOnly):
            return await ctx.send(
                f"The command `{ctx.invoked_with}` can only be used in DMs."
            )

        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send(
                    f"The command `{ctx.invoked_with}` cannot be used in DMs. "
                    "Please try again in a public channel."
                )
            except discord.Forbidden:
                return

        if isinstance(error, commands.NotOwner):
            return await ctx.send(
                f"The command `{ctx.invoked_with}` can only be used by my "
                f"owner `{self.bot.app_info.owner.name}#"
                f"{self.bot.app_info.owner.discriminator}`."
            )

        if isinstance(error, commands.MissingPermissions):
            missing_perms = ""
            for perm in error.missing_perms:
                missing_perms += f"\n> {perm}"
            return await ctx.send(
                "You are missing the following permissions required to run "
                f"the command `{ctx.invoked_with}`:\n{missing_perms}"
            )

        if isinstance(error, commands.BotMissingPermissions):
            missing_perms = ""
            for perm in error.missing_perms:
                missing_perms += f"\n> {perm}"
            return await ctx.send(
                f"Uh oh! I am missing some discord permissions needed to "
                f"execute the command `{ctx.invoked_with}`. Please ensure "
                "that the following perms are enabled on my role:"
                f"\n{missing_perms}"
            )

        if isinstance(error, commands.DisabledCommand):
            return await ctx.send(
                f"The command `{ctx.command}` is currently disabled."
            )

        # TODO: Get bot to delete the error after cooldown has passed
        #       Move botUtils.. to variable in outside if statement
        #       Move return to end of outside if statement (or each inner)
        #       Assign ctx.send to a variable, asyncio.sleep for {botUtils}
        #       await variable.delete afterwards
        if isinstance(error, commands.CommandOnCooldown):
            if error.cooldown.type == commands.BucketType.default:
                return await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for the "
                    "entire bot, retry in `"
                    f"{botUtils.convert_seconds_friendly(error.retry_after)}`."
                )
            if error.cooldown.type == commands.BucketType.user:
                return await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for you, "
                    "retry in `"
                    f"{botUtils.convert_seconds_friendly(error.retry_after)}`."
                )
            if error.cooldown.type == commands.BucketType.guild:
                return await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for this "
                    "server, retry in `"
                    f"{botUtils.convert_seconds_friendly(error.retry_after)}`."
                )
            if error.cooldown.type == commands.BucketType.channel:
                return await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for this "
                    "channel, retry in `"
                    f"{botUtils.convert_seconds_friendly(error.retry_after)}`."
                )
            if error.cooldown.type == commands.BucketType.member:
                return await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for you, "
                    "retry in `"
                    f"{botUtils.convert_seconds_friendly(error.retry_after)}`."
                )
            if error.cooldown.type == commands.BucketType.category:
                return await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for this "
                    "category of channels, retry in `"
                    f"{botUtils.convert_seconds_friendly(error.retry_after)}`."
                )
            # TODO: Fix so that the role on cooldown is mentioned (if possible)
            if error.cooldown.type == commands.BucketType.role:
                return await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for your "
                    "role, retry in `"
                    f"{botUtils.convert_seconds_friendly(error.retry_after)}`."
                )

        # Print the error and traceback if it doesnt match any of the above
        # TODO: Print traceback to logger perhaps?
        print(f"\n[BT] Ignoring exception in command {ctx.command}:")
        traceback.print_exception(type(error), error, error.__traceback__)

    # An example of command specific errors
    # @commands.command(name='repeat', aliases=['mimic', 'copy'])
    # async def do_repeat(self, ctx, *, inp: str):
    #     await ctx.send(inp)

    # @do_repeat.error
    # async def do_repeat_handler(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         if error.param.name == 'inp':
    #             await ctx.send("You forgot to give me input to repeat!")

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
