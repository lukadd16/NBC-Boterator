# Description: Global error handler
# Adapted from https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612

import app_logger
import config
import discord
import sys
import traceback

# from cogs.partners import InviteValueError  # Fact: bot only handles this error when error_handler gets reloaded once since error_handler is the first cog to be loaded at startup (while when reloading partners is already loaded)
from datetime import datetime
from discord.ext import commands
from utils import tools, errors

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
        ignored_exc = (commands.CommandNotFound,)

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

        # elif isinstance(error, commands.BadColourArgument):
        #     await ctx.send(
        #         f"I was not able to obtain a colour from the given value `{error.argument}`. This argument must be provided as a 3-digit hex shortcut (#fff) or 6-digit hex number (#ffffff)."
        #     )

        elif isinstance(error, commands.BadInviteArgument):
            pass

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
                str_cooldown_left = tools.seconds_to_str(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for the "
                    f"entire bot, retry in `{str_cooldown_left}`.",
                    delete_after=error.retry_after
                )
            elif error.cooldown.type == commands.BucketType.user:
                str_cooldown_left = tools.seconds_to_str(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for you, "
                    f"retry in `{str_cooldown_left}`.",
                    delete_after=error.retry_after
                )
            elif error.cooldown.type == commands.BucketType.guild:
                str_cooldown_left = tools.seconds_to_str(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for this "
                    f"server, retry in `{str_cooldown_left}`.",
                    delete_after=error.retry_after
                )
            elif error.cooldown.type == commands.BucketType.channel:
                str_cooldown_left = tools.seconds_to_str(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for this "
                    f"channel, retry in `{str_cooldown_left}`.",
                    delete_after=error.retry_after
                )
            elif error.cooldown.type == commands.BucketType.member:
                str_cooldown_left = tools.seconds_to_str(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for you, "
                    f"retry in `{str_cooldown_left}`.",
                    delete_after=error.retry_after
                )
            elif error.cooldown.type == commands.BucketType.category:
                str_cooldown_left = tools.seconds_to_str(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for this "
                    f"category of channels, retry in `{str_cooldown_left}`.",
                    delete_after=error.retry_after
                )
            # TODO: Fix so that the role on cooldown is mentioned (if possible)
            elif error.cooldown.type == commands.BucketType.role:
                str_cooldown_left = tools.seconds_to_str(
                    error.retry_after
                )

                await ctx.send(
                    f"The command `{ctx.command}` is on cooldown for your "
                    f"role, retry in `{str_cooldown_left}`.",
                    delete_after=error.retry_after
                )

        elif isinstance(error, errors.InviteValueError):
            embed = discord.Embed(
                title="ERROR",
                description="{}".format(error.message),
                colour=config.BOT_ERR_COLOUR,
                timestamp=datetime.utcnow()
            )
            embed.set_author(
                name=config.BOT_AUTHOR_NAME,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.set_footer(
                text="Offending Invite: {}".format(error.invite.url)
            )
            # await ctx.message.delete()  # Delete command invocation
            await ctx.reply(embed=embed)
            logger.error(
                "InviteValueError encountered, terminating command execution and sending message ({}) to context.".format(
                    error.message
                )
            )
            logger.info(
                "Offending Invite: {}".format(error.invite.url)
            )

        elif isinstance(error, errors.DataValidationError):
            embed = discord.Embed(
                title="ERROR",
                description="{}".format(error.message),
                colour=config.BOT_ERR_COLOUR,
                timestamp=datetime.utcnow()
            )
            embed.set_author(
                name=config.BOT_AUTHOR_NAME,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            await ctx.reply(embed=embed)
            logger.info(
                "DataValidationError encountered, terminating command execution and sending message ({}) to context.".format(
                    error.message
                )
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
