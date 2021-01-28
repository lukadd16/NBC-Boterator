# Description: Global error handler
# Adapted from https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612

import app_logger
import discord
import sys
import traceback

from utils import botUtils
from discord.ext import commands

logger = app_logger.get_logger(__name__)


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        for h in logger.handlers:
            logger.removeHandler(h)

    @commands.Cog.listener()
    async def on_error(self, event_method, *args, **kwargs):
        logger.error("Ignoring exception in %s.", event_method)
        logger.error("Unexpected exception:", exc_info=sys.exc_info())

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # If command has a local error handler, allow it to process the error.
        if hasattr(ctx.command, "on_error"):
            return

        # Prevents any cogs with a local cog_command_error() from being
        # handled by on_command_error()
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        # Command error types that we want to ignore
        ignored_exc = (commands.CommandNotFound)

        # Check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found, keep the exception passed to on_command_error().
        error = getattr(error, "original", error)

        # Any error types in ignored_exc will return and exit the function.
        if isinstance(error, ignored_exc):
            return

        # Check for various error types and return a custom reponse
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"I could not find the required `{error.param}` parameter. "
                f"Run `{ctx.prefix}help {ctx.command}` for more information "
                "on how to use this command."
            )

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send(
                "Too many arguments were passed to the command "
                f"`{ctx.invoked_with}`. Run `{ctx.prefix}help {ctx.command}` "
                "for more information on how to use this command."
            )

        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                "A bad argument was passed to the command "
                f"`{ctx.invoked_with}`."
            )

        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.send(
                f"The command `{ctx.invoked_with}` can only be used in DMs."
            )

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.send(
                    f"The command `{ctx.invoked_with}` cannot be used in DMs. "
                    "Please try again in a public channel."
                )
            except discord.Forbidden:
                pass

        elif isinstance(error, commands.NotOwner):
            return await ctx.send(
                f"The command `{ctx.invoked_with}` can only be used by my "
                f"owner `{self.bot.app_info.owner.name}#"
                f"{self.bot.app_info.owner.discriminator}`."
            )

        elif isinstance(error, commands.MissingPermissions):
            missing_perms = ""
            for perm in error.missing_perms:
                missing_perms += f"\n> {perm}"
            await ctx.send(
                "You are missing the following permissions required to run "
                f"the command `{ctx.invoked_with}`:{missing_perms}"
            )

        elif isinstance(error, commands.BotMissingPermissions):
            missing_perms = ""
            for perm in error.missing_perms:
                missing_perms += f"\n> {perm}"
            await ctx.send(
                f"Uh oh! I am missing some discord permissions needed to "
                f"execute the command `{ctx.invoked_with}`. Please ensure "
                "that the following perms are enabled on my role:"
                f"{missing_perms}"
            )

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(
                f"The command `{ctx.command}` is currently disabled."
            )

        elif isinstance(error, commands.CommandOnCooldown):
            if error.cooldown.type == commands.BucketType.default:
                cooldown_left = botUtils.convert_seconds_friendly(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for the "
                    f"entire bot, retry in `{cooldown_left}`.",
                    delete_after=cooldown_left
                )
            elif error.cooldown.type == commands.BucketType.user:
                cooldown_left = botUtils.convert_seconds_friendly(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for you, "
                    f"retry in `{cooldown_left}`.",
                    delete_after=cooldown_left
                )
            elif error.cooldown.type == commands.BucketType.guild:
                cooldown_left = botUtils.convert_seconds_friendly(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for this "
                    f"server, retry in `{cooldown_left}`.",
                    delete_after=cooldown_left
                )
            elif error.cooldown.type == commands.BucketType.channel:
                cooldown_left = botUtils.convert_seconds_friendly(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for this "
                    f"channel, retry in `{cooldown_left}`.",
                    delete_after=cooldown_left
                )
            elif error.cooldown.type == commands.BucketType.member:
                cooldown_left = botUtils.convert_seconds_friendly(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for you, "
                    f"retry in `{cooldown_left}`.",
                    delete_after=cooldown_left
                )
            elif error.cooldown.type == commands.BucketType.category:
                cooldown_left = botUtils.convert_seconds_friendly(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for this "
                    f"category of channels, retry in `{cooldown_left}`.",
                    delete_after=cooldown_left
                )
            # TODO: Fix so that the role on cooldown is mentioned (if possible)
            elif error.cooldown.type == commands.BucketType.role:
                cooldown_left = botUtils.convert_seconds_friendly(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for your "
                    f"role, retry in `{cooldown_left}`.",
                    delete_after=cooldown_left
                )

        # Any errors not explicitly defined above are handled here
        else:
            print(f"\n[BT] Ignoring exception in command {ctx.command}:")
            traceback.print_exception(type(error), error, error.__traceback__)
            logger.error(
                "***Encountered an unforeseen error in a command***"
            )
            logger.error(
                "Offending Command: %s", ctx.command
            )
            logger.error(
                "Error Type: %s", type(error)
            )
            logger.error(
                "The Actual Error: %s", error
            )
            logger.error(
                "Traceback:"
            )
            for i in traceback.format_tb(error.__traceback__):
                logger.error(i)

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
