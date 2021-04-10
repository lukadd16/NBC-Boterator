# Put repeatedly used lines of code here, such as uptime calculation,
# ping calc, determining user status and returning the appropriate emoji,
# future guild tasks, etc.

import app_logger
import config

from datetime import datetime
from typing import TypeVar

logger = app_logger.get_logger(__name__)

# Number of seconds within various units of time
SEC_IN_DAY = 86400
SEC_IN_HR = 3600
SEC_IN_MIN = 60

# Custom param type, both int and float values can be passed to _divmod()
_N2 = TypeVar('_N2', int, float)


# Custom implementation of builtin divmod()
# Although the resultant value from the floor divion (a//b) performed by divmod is a whole number, it may not always be an int.
# This method returns the floor division result as an integer but leaves the remainder as a floating point number.
def _divmod(a: _N2, b: _N2):
    floordiv, remainder = divmod(a, b)
    return int(floordiv), remainder


# Converts a time in seconds to a string with a specific format
# Returned Formatting: 1d 9h 8m 7s
def seconds_to_str(seconds):
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    days = round(days)
    hours = round(hours)
    minutes = round(minutes)
    seconds = round(seconds)
    if minutes == 0:
        return "%02ds" % seconds
    if hours == 0:
        return "%02dm %02ds" % (minutes, seconds)
    if days == 0:
        return "%02dh %02dm %02ds" % (hours, minutes, seconds)
    return "%02dd %02dh %02dm %02ds" % (days, hours, minutes, seconds)


# Converts a datetime object to a human-readable string
# Returned Formatting: Wed, Jul 1, 1987 05:44 PM GMT
def datetime_to_str(time: datetime):
    return time.strftime("%a, %b X%d, %Y %I:%M %p").replace("X0", "X").replace("X", "")


# Returns how long ago a particular datetime object occurred
# Example: Sat, Apr 3, 2021 04:25 PM GMT (3 days ago)
def delta_datetime_to_str(start_time: datetime):
    # Find the difference in time between today and the
    # start_time (which points to a date in the past)
    # Operation returns a timedelta object
    time_delta = datetime.utcnow() - start_time

    # Calculate how many days separates this delta
    days, remainder = _divmod(time_delta.total_seconds(), SEC_IN_DAY)
    # Calculate how many hours separates this delta
    hours, remainder = _divmod(remainder, SEC_IN_HR)
    # Calculate how many minutes and seconds separates this delta
    minutes, seconds = _divmod(remainder, SEC_IN_MIN)

    return _formatted_delta(days, hours, minutes, seconds)


# Helper method; Contains the comparison logic that determines how a calculated delta should be formatted as a string
def _formatted_delta(days: int, hours: int, minutes: int, seconds: float):
    if days > 1:
        return "{0} days ago".format(days)
    if days == 1:
        return "{0} day ago".format(days)
    if hours > 1:
        return "{0} hours ago".format(hours)
    if hours == 1:
        return "{0} hour ago".format(hours)
    if minutes > 1:
        return "{0} minutes ago".format(minutes)
    if minutes == 1:
        return "{0} minute ago".format(minutes)

    return "{0} seconds ago".format(int(seconds))


# Returns the emoji (defined in the config file) that corresponds to the
# status of a passed in discord.Member object
# TODO: Redundant elif and else
def get_member_status(member):
    if f"{member.status}".lower() == "online":
        return f"{config.EMOJI_ONLINE}"
    elif f"{member.status}".lower() == "idle":
        return f"{config.EMOJI_IDLE}"
    elif f"{member.status}".lower() == "dnd":
        return f"{config.EMOJI_DND}"
    elif f"{member.status}".lower() == "offline":
        return f"{config.EMOJI_OFFLINE}"
    else:
        return f"{config.EMOJI_STREAM}"


# Returns either an emoji or an empty string to indicate whether or not
# the passed in discord.Member object is a bot
# TODO: Redundant else statement
def do_bot_check(member):
    if member.bot is True:
        return f"{config.EMOJI_BOT_TAG}"
    else:
        return ""


# Calculate a member's join position via comparing their join date to other
# members; currently being used in the whois and joinpos commands
def get_join_position(ctx, member):
    return sum(
        m.joined_at < member.joined_at
        for m in ctx.guild.members
        if m.joined_at is not None
    ) + 1  # Add +1 to prevent 0 of X situation when user is the "zeroth" member (server creator)
