# Description: Cog that houses utilities commands for NBC Boterator

# Logging ideas:
# - Log bulk deletes regardless of what bot they are from (if they are from jarvis then log event differently because the perpetrator would be known)
# - Log role mentions (see link bookmarked in toolbar that refers to discord.Message, see if can intertwine this with on_message event)
# - Figure out how to handle which channel to send logs to

import discord
import os
import logging
import platform
import psutil
import sys
import time

from utils import botUtils
from datetime import datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

# NEXT STEP: figure out how I can get different named loggers for each cog that all use the same file
# logger = logging.getLogger("JB.main")

class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Move all repeated lines of code to utils folder so that all I need to do is call it once, using one line of code

    # Keep ping command and add extra ping types to it (like MrBot)

    # Make a system command that gives info about the server the bot is running on (meh)

    @commands.command(aliases=["botinfo", "info"])  # TODO: add section at bottom that links to our website and to bot's src
    async def about(self, ctx):
        # Get version info for library and python runtime
        d_version = discord.__version__
        p_version = sys.version[0:5]

        # Get bots' total uptime (as a good skill, should try to put this into its own method)
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        # hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        # minutes, seconds = divmod(remainder, 60)
        # days, hours = divmod(hours, 24)

        friendly_uptime = botUtils.convert_seconds_friendly(delta_uptime.total_seconds())

        # Calculate websocket latency
        web_latency = self.bot.latency * 1000

        # Total users and guilds the bot can see
        # total_users = len(self.bot.users)  # NOT NEEDED
        # total_guilds = len(self.bot.guilds)  # NOT NEEDED

        pid = os.getpid()
        py = psutil.Process(pid)
        bot_memory_usage = round(py.memory_info()[0]/(10**6), 2)
        # print('memory use:', memoryUse)

        embed = discord.Embed(
            title='Bot Info',
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=self.bot.config.BOT_AUTHOR_CLICK,
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name='Developer: ',
            value='`Lukadd.16#8870`',
            inline=True
        )
        embed.add_field(
            name='Bot Version:',
            value=f'`{self.bot.config.BOT_VERSION}`',
            inline=True
        )
        embed.add_field(
            name='Uptime: ',
            value=f'`{friendly_uptime}`',
            inline=True
        )
        embed.add_field(
            name='Python Version: ',
            value=f'`{p_version}`',
            inline=True
        )
        embed.add_field(
            name='Library Version: ',
            value=f'`Discord.py {d_version}`',
            inline=True
        )
        embed.add_field(
            name='Websocket Ping: ',
            value='`{:.2f}ms`'.format(web_latency),
            inline=True
        )
        embed.add_field(
            name='RAM Usage: ',
            value=f'`{bot_memory_usage} MB`',
            inline=True
        )
        embed.add_field(
            name='PLACEHOLDER: ',
            value=f'`placeholder`',
            inline=True
        )
        embed.add_field(
            name='Server OS: ',
            value=f'`{platform.system()}`',
            inline=True
        )
        embed.set_footer(
            text=self.bot.config.BOT_FOOTER
        )
        await ctx.channel.send(embed=embed)

    # WIP, scraping admin idea instead for if the staff member
    # (defined as kick+ban perms basically) also has send perms to the channel
    # they are specifying, then they are allowed to use this command
    @commands.command(aliases=["announcement"], enabled=False)
    @commands.guild_only()
    async def announce(self, ctx, target_channel: discord.TextChannel, *, user_message: str):  # How to properly split arguments?
        embed = discord.Embed(
            description=f'{user_message}',
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_footer(
            text=f'{ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url
        )
        await target_channel.send(embed=embed)

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        user_pfp = member.avatar_url_as(
            format=None,
            static_format='png',
            size=256
        )

        embed = discord.Embed(
            title=f'Avatar – ``{member.name}#{member.discriminator}``',
            description=member.mention,
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=self.bot.config.BOT_AUTHOR_CLICK,
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_image(
            url=user_pfp
        )
        embed.set_footer(
            text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',
            icon_url=f'{ctx.author.avatar_url}'
        )

        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["version", "whatsnew"])
    async def changelog(self, ctx):
        # Remove beta version field and replace with only one "Current Version" or similar that has a variable for version number that changes depending on if this instance is a beta version or not
        # (better idea) In the config file for the beta version only, just set the BOT_VERSION value to the BETAVERSION value and then all that's needed to be done here is just use that one variable

        embed = discord.Embed(
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=self.bot.config.BOT_AUTHOR_CLICK,
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        # embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name="Version:",
            value=self.bot.config.BOT_VERSION,
            inline=True
        )
        # embed.add_field(
        #    name="Beta Version:",
        #    value=self.bot.config.BOT_BETAVERSION,
        #    inline=True
        # )
        embed.add_field(
            name="New Features/Fixes with this Version:",
            value=f"```{self.bot.config.BOT_FEATURES}```",  # Use code block
            inline=False
        )
        embed.set_footer(
            text=self.bot.config.BOT_FOOTER
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["joinposition", "jpos"])
    async def joinpos(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        member_join_position = botUtils.get_join_position(ctx, member)
        msg = f"*{member.name}* is member `#{member_join_position}` "\
              f"(out of {len(ctx.guild.members)})"

        # embed = discord.Embed(
        #     colour=self.bot.config.BOT_COLOUR
        # )
        # embed.set_author(
        #     name=self.bot.config.BOT_AUTHOR_CLICK,
        #     url=self.bot.config.BOT_URL,
        #     icon_url=self.bot.user.avatar_url
        # )
        # embed.set_thumbnail(
        #     url=self.bot.user.avatar_url
        # )
        # embed.add_field(
        #     name='Join Position:',
        #     value=f'{member_join_position} of {len(ctx.guild.members)}'
        # )
        # embed.set_footer(
        #     text=self.bot.config.BOT_FOOTER
        # )

        await ctx.channel.send(msg)

    @commands.command()
    async def ping(self, ctx):
        # Start timer used for latency calculation
        start = time.perf_counter()
        self.bot.logger.debug("Ping timer started")

        embed = discord.Embed(
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=self.bot.config.BOT_AUTHOR_CLICK,
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_thumbnail(
            url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Ping...",
            value='Message Round Trip: \nDiscord Websocket: '
        )
        embed.set_footer(
            text=self.bot.config.BOT_FOOTER
        )
        message = await ctx.channel.send(embed=embed)

        # Calculate round trip and websocket latencies
        end = time.perf_counter()
        self.bot.logger.debug("Ping timer ended")
        duration = (end - start) * 1000
        web_latency = self.bot.latency * 1000

        embed = discord.Embed(
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=self.bot.config.BOT_AUTHOR_CLICK,
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_thumbnail(
            url=self.bot.user.avatar_url
        )
        # :.2f cuts latency values down to two decimal places
        embed.add_field(
            name="Pong!",
            value='Message Round Trip: ``{:.2f}ms``'
                  '\nDiscord Websocket: ``{:.2f}ms``'.format(duration, web_latency)
        )
        embed.set_footer(
            text=self.bot.config.BOT_FOOTER
        )
        await message.edit(embed=embed)
        self.bot.logger.debug("Ping response sent")

    # Deprecated, remove entirely from a future release
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
    async def whois(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        # Get various info about user
        # snowflake_time is outputted in the form of datetime.datetime
        user_createdate = discord.utils.snowflake_time(member.id)

        # Convert account creation time to readable format
        user_createdate_friendly = user_createdate.strftime(
            "%a, %b %d, %Y %H:%M %p"
        )

        # Convert guild join time to readable format
        member_joindate_friendly = member.joined_at.strftime(
            "%a, %b %d, %Y %H:%M %p"
        )

        # Returns member's join position out of total guild members
        member_join_position = botUtils.get_join_position(ctx, member)

        # Function will return an emoji if the user is a bot;
        bot_identify = botUtils.do_bot_check(member)

        # Function will return an emoji based on user's set status
        status_emoji = botUtils.get_member_status(member)

        # Subtract by 1 to omit the @everyone role
        member_role_sum = len(member.roles) - 1

        # Check sum of member.roles list, if there are no roles
        # (excluding @everyone) return None to prevent 400 Bad Request Error.
        # Otherwise perform list manipulation logic.
        if member_role_sum == 0:
            member_role_list = None
        elif member_role_sum >= 1:
            # Separate each role by a single space
            member_role_list = ' '.join(
                [
                    r.mention for r in member.roles[:0:-1]
                ]
            )

        # Now that I understand how to get roles, make a system that loops
        # through user's roles (from highest to lowest) finding the first one
        # that has a colour other than the default invisible one

        embed = discord.Embed(
            title=f'User Info – ``{member.name}#{member.discriminator}``'
                  f'{status_emoji}',
            description=f'{member.mention + bot_identify}',
            colour=self.bot.config.BOT_COLOUR
            # timestamp=datetime.now()
        )
        embed.set_author(
            name=self.bot.config.BOT_AUTHOR_CLICK,
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_thumbnail(
            url=(member.avatar_url)
        )
        embed.add_field(
            name='Account Created:',
            value=f'{user_createdate_friendly} GMT',
            inline=True
        )
        embed.add_field(
            name='Joined Guild:',
            value=f'{member_joindate_friendly} GMT',
            inline=True
        )
        embed.add_field(
            name='Join Position:',
            value=f'{member_join_position} of {len(ctx.guild.members)}',
            inline=True
        )
        embed.add_field(
            name='User ID:',
            value=f'{member.id}',
            inline=True
        )
        embed.add_field(
            name='Nickname:',
            value=f'{member.nick}',
            inline=True
        )
        embed.add_field(
            name=f'Roles [{member_role_sum}]:',
            value=f"{member_role_list}",
            inline=False
        )
        embed.set_footer(
            text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',
            icon_url=(ctx.author.avatar_url)
        )
        await ctx.channel.send(embed=embed)

    # WIP
    @commands.command(aliases=["sinfo"], enabled=True)
    @commands.guild_only()
    async def serverinfo(self, ctx):
        embed = discord.Embed(
            title=f'Server Info - `{ctx.guild.name}`',
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=self.bot.config.BOT_AUTHOR_CLICK,
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        # Set thumbnail to be the server's icon
        # Should work with both animated and static
        embed.set_thumbnail(
            url=ctx.guild.icon_url
        )
        # Create list of features/info/stats that I want to include

        embed.set_footer(
            text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',
            icon_url=(ctx.author.avatar_url)
        )
        await ctx.channel.send(embed=embed)

    # Users are only allowed to use this command once every 5 minutes
    # Way to reset the cooldown if they trigger an error?
    @commands.command()
    @commands.cooldown(1, 300, type=BucketType.user)
    @commands.guild_only()
    async def suggest(self, ctx, *, user_suggestion: str):
        suggest_channel = self.bot.get_channel(
            self.bot.config.SUGGEST_CHANNEL_ID
        )
        if len(user_suggestion) >= 512:
            embed = discord.Embed(
                title='ERROR',
                description='Your suggestion cannot be more than 512 characters in length, please try to shorten it.',
                colour=self.bot.config.BOT_ERR_COLOUR
            )
            embed.set_author(
                name=self.bot.config.BOT_AUTHOR_CLICK,
                url=self.bot.config.BOT_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.set_footer(
                text=self.bot.config.BOT_FOOTER
            )
            await ctx.channel.send(embed=embed)
            # Reset the cooldown for the user to allow them to try again
            ctx.command.reset_cooldown(ctx)
            return

        else:
            embed = discord.Embed(
                title='SUCCESS',
                description='Your suggestion for the developer has been '
                            'received!\nThank you for contributing to the bot.',
                colour=self.bot.config.BOT_SUCCESS_COLOUR
            )
            embed.set_author(
                name=self.bot.config.BOT_AUTHOR_CLICK,
                url=self.bot.config.BOT_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.set_footer(
                text=f'Sent by {ctx.author.name}#{ctx.author.discriminator}',
                icon_url=ctx.author.avatar_url
            )
            await ctx.message.delete()
            await ctx.channel.send(embed=embed)

        # Info about the user who sent in the suggestion
        embed = discord.Embed(
            title='NEW SUGGESTION',
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=self.bot.config.BOT_AUTHOR_NAME,
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name='Details:',
            value=f'User: `{ctx.author.name}#{ctx.author.discriminator}` '
                  f'(ID: {ctx.author.id})'
                  f'\nChannel: `#{ctx.channel.name}` (ID: {ctx.channel.id})'
                  f'\nServer: `{ctx.guild.name}` (ID: {ctx.guild.id})',
            inline=False
        )
        embed.add_field(
            name='Suggestion:',
            value=f'{user_suggestion}',
            inline=False
        )
        embed.set_footer(
            text=f'Sent by {ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url
        )
        await suggest_channel.send(embed=embed)

        # Add checkmark and reject reactions to the message after it has sent (for the public to vote on)

def setup(bot):
    bot.add_cog(UtilitiesCog(bot))
    # print(os.getcwd())
