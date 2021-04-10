# Description: Cog that houses utilities commands for NBC Boterator

import app_logger
import config
import discord
import platform
import os
import psutil
import subprocess
import sys
import time

from datetime import datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from typing import Optional
from utils import tools

logger = app_logger.get_logger(__name__)


class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.suggest_channel = self.bot.get_channel(
            config.SUGGEST_CHANNEL_ID
        )

    def cog_unload(self):
        for h in logger.handlers:
            logger.removeHandler(h)

    def get_local_version():
        # Grab version num from a local file previously generated by the
        # GitHub release-please action
        with open("version.txt") as f:
            bot_version = f.readline()

        recent_commit = "Unknown"
        commit_date = "Unknown"

        try:
            git_log = subprocess.check_output(
                ["git", "log", "-n", "1", "--date=iso"]
            ).decode()

            for line in git_log.split("\n"):
                if line.startswith("commit"):
                    recent_commit = line.split(" ")[1]
                elif line.startswith("Date"):
                    commit_date = line[5:].strip()  # Might need to amend the splicing value
                    commit_date = commit_date.replace(" +", "+").replace(" ", "T")
                else:
                    pass
        except Exception as e:
            # ...
            raise e

        return bot_version, recent_commit, commit_date

    def get_remote_commits():
        pass

    @commands.command(aliases=["botinfo", "info"])
    async def about(self, ctx):
        # Grab version number generated by GitHub release-please action
        with open("version.txt") as f:
            bot_version = f.readline()
            logger.debug(
                "Parsed Bot Version (%s)", bot_version  # TODO: Strip newline character
            )

        # Get version info for library and python runtime
        disc_version = discord.__version__
        py_version = sys.version[0:5]

        # Get bots' total uptime
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        str_uptime = tools.seconds_to_str(
            delta_uptime.total_seconds()
        )

        # Calculate websocket latency
        web_latency = self.bot.latency * 1000

        # Calculate bot python process memory usage
        pid = os.getpid()
        py = psutil.Process(pid)
        bot_memory_usage = round(py.memory_info()[0]/(10**6), 2)

        embed = discord.Embed(
            title=f"About - {config.BOT_AUTHOR_NAME}",
            description="This is the server's custom discord bot, created for "
                        "the purpose of making everyone's lives easier. It's "
                        "fairly barebones feature-wise right now, but that'll "
                        "change as development continues."
                        f"\n\n{config.EMOJI_GITHUB} **[GitHub]"
                        f"({config.GITHUB_URL})**"
                        f"\n{config.EMOJI_YOUTUBE} **[YouTube Channel]"
                        f"({config.YT_CHANNEL_URL})**"
                        f"\n{config.EMOJI_CLOUD} **[Website (WIP)]"
                        f"({config.WEBSITE_URL})**"
                        f"\n{config.EMOJI_PLACARD} **[Bump us on disboard.org]"
                        f"({config.DISBOARD_URL})**"
                        f"\n{config.EMOJI_PLACARD} **[Vote for us on top.gg]"
                        f"({config.TOPGG_URL})**",
            colour=config.BOT_COLOUR
        )
        embed.set_thumbnail(
            url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Developer:",
            value="`Lukadd.16#8870`",
            inline=True
        )
        embed.add_field(
            name="Bot Version:",
            value=f"`{bot_version}`",
            inline=True
        )
        embed.add_field(
            name="Uptime:",
            value=f"`{str_uptime}`",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"`{py_version}`",
            inline=True
        )
        embed.add_field(
            name="Library Version:",
            value=f"`Discord.py {disc_version}`",
            inline=True
        )
        embed.add_field(
            name="Websocket Ping:",
            value="`{:.2f}ms`".format(web_latency),
            inline=True
        )
        embed.add_field(
            name="RAM Usage:",
            value=f"`{bot_memory_usage} MB`",
            inline=True
        )
        embed.add_field(
            name="PLACEHOLDER:",
            value="`placeholder`",
            inline=True
        )
        embed.add_field(
            name="Server OS:",
            value=f"`{platform.system()}`",
            inline=True
        )
        embed.set_footer(
            text=config.BOT_FOOTER
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
            logger.debug(
                "No member specified in %s command, defaulting to author",
                ctx.command
            )

        user_pfp = member.avatar_url_as(
            format=None,
            static_format="png",
            size=256
        )

        embed = discord.Embed(
            title=f"Avatar – `{member.name}#{member.discriminator}`",
            description=member.mention,
            colour=config.BOT_COLOUR,
            timestamp=ctx.message.created_at
        )
        embed.set_author(
            name=config.BOT_AUTHOR_CLICK,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_image(
            url=user_pfp
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url=f"{ctx.author.avatar_url}"
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["version", "whatsnew"])
    async def changelog(self, ctx):
        # Grab version num from a local file previously generated by the
        # GitHub release-please action
        with open("version.txt") as f:
            bot_version = f.readline()

        embed = discord.Embed(
            description=f"**Local Version:** [{bot_version}]"
                        f"({config.GITHUB_LATEST_URL})\n"
                        "> A full changelog can be viewed via the above "
                        "hyperlink.",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name="NBC Boterator Changelog",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(
            text=config.BOT_FOOTER
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["joinposition", "jpos"])
    @commands.guild_only()
    async def joinpos(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
            logger.debug(
                "No member specified in %s command, defaulting to author",
                ctx.command
            )

        member_join_position = tools.get_join_position(ctx, member)
        msg = f"*{member.name}* is member `#{member_join_position}` "\
              f"(out of {len(ctx.guild.members)})"

        await ctx.send(msg)

    @commands.command()
    async def ping(self, ctx):
        # Start stopwatch used for latency calculation
        start = time.perf_counter()
        logger.debug("Ping timer started")

        embed = discord.Embed(
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name="NBC Boterator Response Times",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Ping...",
            value="Message Round Trip: "
                  "\nDiscord Websocket: "
        )
        embed.set_footer(
            text=config.BOT_FOOTER
        )
        message = await ctx.send(embed=embed)

        # End stopwatch; Calculate cmd round-trip and websocket latencies
        end = time.perf_counter()
        logger.debug("Ping timer ended")
        duration = (end - start) * 1000
        web_latency = self.bot.latency * 1000

        embed = discord.Embed(
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_CLICK,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_thumbnail(
            url=self.bot.user.avatar_url
        )
        # :.2f cuts latency values down to two decimal places
        embed.add_field(
            name="Pong!",
            value="Message Round Trip: `{:.2f}ms`"
                  "\nDiscord Websocket: `{:.2f}ms`".format(
                      duration, web_latency
                  )
        )
        embed.set_footer(
            text=config.BOT_FOOTER
        )
        await message.edit(embed=embed)

    @commands.command(aliases=["pins", "pinfo"])
    async def pinned(self, ctx, channel: Optional[discord.TextChannel] = None):
        if channel is None:
            channel = ctx.channel

        # Retrieve all pinned messages as a List[Message]
        pinned_messages = await channel.pins()

        # Count # of pinned messages in the channel
        total_pins = len(pinned_messages)

        # Create response embed
        embed = discord.Embed(
            title="Pinned Messages In:",
            description=channel.mention,
            colour=config.BOT_COLOUR,
            timestamp=ctx.message.created_at
        )
        # embed.set_author(
        #     name="Pinned Messages In:",
        #     url=config.WEBSITE_URL,
        #     icon_url=self.bot.user.avatar_url
        # )
        embed.add_field(
            name="__Channel ID__",
            value=f"{channel.id}",
            inline=False
        )
        embed.add_field(
            name="__# of Pinned Messages__",
            value=f"{total_pins} (max permitted is 50)",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url=f"{ctx.author.avatar_url}"
        )

        # Retrieve most recent pinned message & relevant details about it
        # Embed field will be different depending on the existance of a
        # pinned message
        try:
            recent_pin = pinned_messages[0]

            # Escape markdown and channel/user/role mentions
            escaped = discord.utils.remove_markdown(recent_pin.clean_content)

            # Retrieve first few characters from message
            pin_brief = escaped[0:40]

            if pin_brief == "":
                # Message string is empty, which means the actual message
                # contains an embed or attachment
                pin_brief = "Cannot preview, message is an embed/attachment"
            elif len(escaped) > 40:
                # Message content is too long to display so we will
                # inform the user by tacking on (...)
                pin_brief += " ..."
            else:
                # Put quotes around message content
                pin_brief = "\"" + pin_brief + "\""

            # Retrieve message author
            pin_author = (
                recent_pin.author.mention
                + f" ({recent_pin.author.id})"
            )

            # Get info related to when this message was created
            pin_created = "{0} GMT `({1})`".format(
                # Date message was created
                tools.datetime_to_str(
                    recent_pin.created_at
                    ),
                # String describing how long ago this message was created
                tools.delta_datetime_to_str(
                    recent_pin.created_at
                    )
            )

            # If message has been edited
            if recent_pin.edited_at:
                # Get info related to when this message was edited
                pin_edited = "{0} GMT `({1})`".format(
                    # Date message was edited
                    tools.datetime_to_str(
                        recent_pin.edited_at
                        ),
                    # String describing how long ago this message was edited
                    tools.delta_datetime_to_str(
                        recent_pin.edited_at
                        )
                )
            else:
                pin_edited = "N/A"

            # Get discord.com/channels/ link to the message
            pin_url = recent_pin.jump_url

            embed.add_field(
                name="__Most Recent Pin__",
                value=f"**Author:** {pin_author}"
                      f"\n**Created:** {pin_created}"
                      f"\n**Modified:** {pin_edited}"
                      f"\n**Content:** {pin_brief}"
                      f"\n> [**Jump To Message**]({pin_url})",
                inline=False
            )
        except IndexError:  # Channel has no pinned messages
            embed.add_field(
                name="__Most Recent Pin__",
                value="The specified channel has no pinned messages",
                inline=False
            )

        await ctx.send(embed=embed)

    @pinned.error
    async def pinned_error(self, ctx, error):
        # Bot does not have access to the mentioned channel
        if isinstance(error, discord.Forbidden):
            embed = discord.Embed(
                title="ERROR - 403 Forbidden",
                description="I do not have access to view this channel. Please check my permissions and try again.",
                colour=config.BOT_ERR_COLOUR
            )
            embed.set_footer(
                text=config.BOT_FOOTER
            )
            await ctx.send(embed=embed)

    # Deprecated, remove entirely in a future release
    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(
            "I have been online for "
            f"{days}d, {hours}h, {minutes}m, {seconds}s, Sir"
        )

    @commands.command(aliases=["userinfo", "uinfo"])
    @commands.guild_only()
    async def whois(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
            logger.debug(
                "No member specified in %s command, defaulting to author",
                ctx.command
            )

        logger.debug("Debug Stack:")

        # Get creation date (in GMT) of the member's discord account
        # Method returns a datetime.datetime object
        snowflake = discord.utils.snowflake_time(member.id)

        # Convert snowflake into formatted string
        user_createdate = "{0} ({1} GMT)".format(
            tools.delta_datetime_to_str(snowflake),
            tools.datetime_to_str(snowflake)
        )
        logger.debug(
            "> (tools) Account Created On: %s", user_createdate
        )

        # Convert datetime that the user joined the guild into a
        # formatted string
        member_joindate = "{0} ({1} GMT)".format(
            tools.delta_datetime_to_str(member.joined_at),
            tools.datetime_to_str(member.joined_at)
        )
        logger.debug(
            "> (tools) Joined Guild On: %s", member_joindate
        )

        # Returns member's join position out of all guild members
        member_join_position = tools.get_join_position(
            ctx,
            member
        )
        logger.debug(
            "> (tools) Join Position in Guild: %s", member_join_position
        )

        # Variable will store an emoji if the member is a bot
        bot_identify = tools.do_bot_check(
            member
        )
        logger.debug("> (tools) User is a bot? %s", bot_identify)

        # Returns an emoji dynamic to member's online status
        status_emoji = tools.get_member_status(
            member
        )
        logger.debug("> (tools) User Status: %s", status_emoji)

        # Subtract by 1 to omit the @everyone role
        member_role_sum = len(member.roles) - 1
        logger.debug("> Role Count: %s", member_role_sum)

        # Check sum of member.roles list, if member has no roles
        # return None to prevent 400 Bad Request Error.
        # Else perform list manipulation logic.
        if member_role_sum == 0:
            member_role_list = None
        elif member_role_sum >= 1:
            # Separate each role by a single space
            member_role_list = ' '.join(
                [
                    r.mention for r in member.roles[:0:-1]
                ]
            )
        logger.debug("> List of Roles: %s", member_role_list)

        # TODO: Now that I understand how to get roles, make a system that loops
        # through user's roles (from highest to lowest) finding the first one
        # that has a colour other than the default invisible one

        embed = discord.Embed(
            # title=f"User Info – `{member.name}#{member.discriminator}`",
            description=f"{member.mention}{status_emoji}{bot_identify}",
            colour=config.BOT_COLOUR,
            timestamp=ctx.message.created_at
        )
        embed.set_author(
            name=f"{member.name}#{member.discriminator}",
            url=config.WEBSITE_URL,
            icon_url=member.avatar_url
        )
        embed.set_thumbnail(
            url=member.avatar_url
        )
        embed.add_field(
            name="User ID",
            value=f"```{member.id}```",
            inline=True
        )
        embed.add_field(
            name="Account Created",
            value=f"```{user_createdate}```",
            inline=False
        )
        embed.add_field(
            name="Joined Guild",
            value=f"```{member_joindate}```",
            inline=False
        )
        embed.add_field(
            name="Member #",
            value=f"```{member_join_position} of {len(ctx.guild.members)}```",
            inline=False
        )
        embed.add_field(
            name=f"Roles [{member_role_sum}]",
            value=f"{member_role_list}",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)

    # WIP
    @commands.command(aliases=["sinfo"], enabled=False)
    @commands.guild_only()
    async def serverinfo(self, ctx):
        embed = discord.Embed(
            title=f"Server Info - `{ctx.guild.name}`",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_CLICK,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        # Set thumbnail to be the server's icon
        # Should work with both animated and static
        embed.set_thumbnail(
            url=ctx.guild.icon_url
        )
        # Create list of features/info/stats that I want to include

        embed.set_footer(
            text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)

    # Users are only allowed to use this command once every 30 seconds
    # TODO: Should add JSON file + ability to blacklist users from sending
    #       suggestions (then do the same for global cmd blacklist)
    @commands.command()
    @commands.cooldown(1, 30, type=BucketType.user)
    @commands.guild_only()
    async def suggest(self, ctx, *, user_suggestion: str):
        if len(user_suggestion) >= 512:
            logger.info(
                "User Suggestion Too Long"
            )
            logger.info(
                "> Offending User: %s#%s",
                ctx.author.name,
                ctx.author.discriminator
            )

            embed = discord.Embed(
                title="ERROR",
                description="Your suggestion cannot be more than 512 "
                            "characters in length, please try to shorten it.",
                colour=config.BOT_ERR_COLOUR
            )
            embed.set_author(
                name=config.BOT_AUTHOR_CLICK,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.set_footer(
                text=config.BOT_FOOTER
            )
            await ctx.send(embed=embed)

            # Reset cmd cooldown for user to allow another attempt
            ctx.command.reset_cooldown(ctx)
            logger.info(
                "Resetting user cooldown to allow another attempt"
            )
            return

        else:
            embed = discord.Embed(
                title="SUCCESS",
                description="Your suggestion for the developer has been "
                            "received!\nThank you for your input.",
                colour=config.BOT_SUCCESS_COLOUR,
            )
            embed.set_author(
                name=config.BOT_AUTHOR_CLICK,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.set_footer(
                text=f"Invoked by {ctx.author.name}#"
                     f"{ctx.author.discriminator}",
                icon_url=ctx.author.avatar_url
            )
            await ctx.message.delete()
            await ctx.send(embed=embed)

        logger.info("Processing New Suggestion")

        # Send suggestion to appropriate channel along with relevant data
        embed = discord.Embed(
            title="NEW SUGGESTION",
            colour=config.BOT_COLOUR,
            timestamp=ctx.message.created_at
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Details:",
            value=f"User: `{ctx.author.name}#{ctx.author.discriminator}` "
                  f"(ID: `{ctx.author.id}`)"
                  f"\nChannel: `#{ctx.channel.name}` (ID: `{ctx.channel.id}`)"
                  f"\nServer: `{ctx.guild.name}` (ID: `{ctx.guild.id}`)",
            inline=False
        )
        embed.add_field(
            name="Suggestion:",
            value=f"{user_suggestion}",
            inline=False
        )
        embed.set_footer(
            text=f"Suggested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url=ctx.author.avatar_url
        )
        suggest_msg = await self.suggest_channel.send(embed=embed)
        logger.debug("Suggestion Sent To Channel")

        # Add reactions to allow public participation
        await suggest_msg.add_reaction(config.EMOJI_UPVOTE)
        await suggest_msg.add_reaction(config.EMOJI_DOWNVOTE)
        logger.debug("Reactions Added")


def setup(bot):
    bot.add_cog(UtilitiesCog(bot))
