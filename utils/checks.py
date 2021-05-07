from builtins import any

from discord.ext import commands
from discord.ext.commands.context import Context

import app_logger
import config
from errors import NotStaff

logger = app_logger.get_logger(__name__)

# This will house custom decorator checks such as is_admin, is_mod,
# is_heirarchy (e.g. to handle case when moderation command is run by a user that has a role lower than the mentioned user; doing it this way also prevents 403 Forbidden error from being thrown (within the method itself))
# and any others that logically make sense

# Brainstorming Cases:
# - User attempting to perform action on user with a higher role (name: is_heirarchy or has_heirarchy)
# >>> Simple Impl: keep to only staff-related actions, so only compare heirarchy relative to staff roles
# >>> Moderate Impl: compare heirarchy compared to all roles (need to obtain ordered list somehow)

# Don't forget that check (decorators) can have arguments!


# TODO: Error throws need to be nested inside the predicate
# async def predicate(ctx):
#     if not await ctx.bot.is_owner(ctx.author):
#         raise NotOwner('You do not own this bot.')
#     return True

# The accompanying custom error classes should derive from commands.CommandError (so that `on_command_error()` picks it up)


def staff_heirarchy():
    """
    Primarily for use with moderation-related commands. XX.
    """
    pass


def is_bot_owner():
    """
    Returns true if invoking author is the owner of this bot.
    This just calls the built-in is_owner() check.
    """
    return commands.is_owner()


def is_server_owner():
    """
    Returns true if invoking author is the owner of the server (either
    guild owner from Discord's perspective or has Owner role).
    """
    async def predicate(ctx: Context):
        if not (ctx.author == ctx.guild.owner) or any(config.OWNER_ROLE in role.id for role in ctx.author.roles):
            raise NotStaff("The command `{}` can only be used by the server owner.".format(ctx.invoked_with))

        return True

    return commands.check(predicate)


def is_administrator():
    """
    Returns true if invoking author is an administrator in the home server
    (either has administrator permission or has the Administrator role).
    """
    async def predicate(ctx: Context):
        if not ctx.author.guild_permissions.administrator or any(config.ADMIN_ROLE in role.id for role in ctx.author.roles):
            raise NotStaff("The command `{}` can only be used by an Administrator.".format(ctx.invoked_with))
        return True

    return commands.check(predicate)


def is_executive():
    """
    Returns true if invoking author is an executive (determined by role).
    """
    async def predicate(ctx: Context):
        if not any(config.EXEC_HOIST_ROLE in role.id for role in ctx.author.roles):
            raise NotStaff("The command `{}` can only be used by an Executive.".format(ctx.invoked_with))
        return True

    return commands.check(predicate)


def is_head_moderator():
    """
    Returns true if invoking author is a Head Moderator (role).
    """
    async def predicate(ctx: Context):
        if not any(config.HEAD_MOD_ROLE in role.id for role in ctx.author.roles):
            raise NotStaff("The command `{}` can only be used by a Head Moderator.".format(ctx.invoked_with))
        return True

    return commands.check(predicate)


def is_moderator():
    """
    Returns true if invoking author is a Moderator (role).
    """
    async def predicate(ctx: Context):
        if not any(config.MOD_ROLE in role.id for role in ctx.author.roles):
            raise NotStaff("The command `{}` can only be used by a Moderator.".format(ctx.invoked_with))
        return True

    return commands.check(predicate)

# def is_moderator_or_higher():
#     """
#     Returns true if invoking author is a Moderator or above (role).
#     """
#     async def predicate(ctx: Context):
#         if not any(config.MOD_ROLE in role.id for role in ctx.author.roles):
#             raise NotStaff("The command `{}` can only be used by Server Moderators.".format(ctx.invoked_with))
#         return True
#
#     return commands.check(predicate)

# is_head_mod_or_higher, is_admin_or_higher, etc.

# TODO: overlooked something, often want to NOT allow a trial moderator to run a specific command.
#       Would be much cleaner to have a single decorator for this (potentially with args) rather than chaining multiple together.

def is_trial_moderator():
    """
    Returns true if invoking author is a Trial Moderator (role).
    """
    async def predicate(ctx: Context):
        if not any(config.TRIAL_ROLE in role.id for role in ctx.author.roles):
            raise NotStaff("The command `{}` can only be used by Trial Moderators.".format(ctx.invoked_with))
        return True

    return commands.check(predicate)


def is_staff():
    """
    Returns true if invoking author is a staff member (role).
    """
    async def predicate(ctx: Context):
        return any(config.STAFF_HOIST_ROLE in role.id for role in ctx.author.roles)

    return commands.check(predicate)


def is_muted():
    """
    Returns true if invoking author is muted (for the
    interim, only checks for presence of the muted role).
    """
    async def predicate(ctx: Context):
        return any(config.MUTED_ROLE in role.id for role in ctx.author.roles)

    return commands.check(predicate)
