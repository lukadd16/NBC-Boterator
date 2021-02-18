# Put repeatedly used lines of code here, such as uptime calculation,
# ping calc, determining user status and returning the appropriate emoji,
# future guild tasks, etc.

import app_logger
import config

logger = app_logger.get_logger(__name__)


# Used in cmd cooldown + bot uptime calculation, takes seconds value as arg.
# Returned Formatting: 1d 9h 8m 7s
def fmt_seconds_friendly(second):
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    days = round(day)
    hours = round(hour)
    minutes = round(minute)
    seconds = round(second)
    if minutes == 0:
        return "%02ds" % (seconds)
    if hours == 0:
        return "%02dm %02ds" % (minutes, seconds)
    if days == 0:
        return "%02dh %02dm %02ds" % (hours, minutes, seconds)
    return "%02dd %02dh %02dm %02ds" % (days, hours, minutes, seconds)


# Meant for when passing raw datetimes that include year, month, day, etc.
# Returned Formatting: Wed, Jul 1, 1987 17:44 PM GMT
def fmt_time_friendly(time):
    return time.strftime("%a, %b X%d, %Y %H:%M %p").replace("X0", "X").replace("X", "")


# In weeks format for whois and serverinfo, maybe rename it to something else
# def get_time_friendly():
#     pass


# Return an emoji defined in the config file depending on the status of the
# passed user; currently being used in the whois command
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


# Return an emoji defined in the config file depending on whether the passed
# user is a bot or not; currently being used in the whois command
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
    )