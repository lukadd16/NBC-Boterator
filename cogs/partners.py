# Description: Cog with commands relevant to new server partnership system

import app_logger
import asyncio
import config
import discord
import json
import os

from datetime import datetime
from discord.ext import commands
from typing import Optional

logger = app_logger.get_logger(__name__)

# Command Structure:
# partner
#   - init (send_req)
#       > refresh (edit_req)
#   - add
#   - edit (msgID, field, value)
#       > msgID (discord.Message)
#           >> invite (discord.Invite)
#           >> rep (ID)
#           >> colour (hexcode)
#           >> banner (str URL)
#           >> website (str URL)

# For command invocation pretty sure allowed to separate each arg on a new line (will make my life easier, but won't make any difference on the back-end)


class Partners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_file_path = self._init_db()

    # TODO: Replace with custom checks when those are implemented
    async def cog_check(self, ctx):
        return commands.has_guild_permissions(administrator=True) and commands.guild_only()

    def cog_unload(self):
        for h in logger.handlers:
            logger.removeHandler(h)

    # Database configuration
    @staticmethod
    def _init_db() -> str:
        db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")
        db_dir = os.path.join(db_dir, "db")
        db_file_name = "partners.json"
        db_file_path = os.path.join(db_dir, db_file_name)
        logger.info("JSON File Path: {}".format(db_file_path))

        return db_file_path

    @commands.group(aliases=["partners"])
    async def partner(self, ctx):
        # Could use the base command to explain how to partner, etc. (could also add a link via MD to the requirements embed)
        # E.g. Want to partner with us? Just head on over to [this]() message to learn how!
        pass

    # Sends the requirements for partnership message to the set partners channel
    @partner.group()
    async def init(self, ctx):
        await ctx.trigger_typing()
        # Open DB file in Binary Read-Only mode
        # Binary mode so that special characters (e.g. é) display properly
        with open(self.db_file_path, "rb") as f:
            data = json.load(f)
            logger.debug("JSON Data Loaded")

        # Construct initial embed using data from our json file
        embed = discord.Embed(
            title="{}".format(data['requirementsEmbed']['title']),
            description="{}".format(data['requirementsEmbed']['description']),
            colour=config.DISC_DARK_EMBED_BG,
            timestamp=datetime.utcnow()  # This attribute is timezone aware
        )
        embed.add_field(
            name="{}".format(data['requirementsEmbed']['fields']['partnerReq']['name']),
            value="{}".format('\n'.join(map(str, data['requirementsEmbed']['fields']['partnerReq']['value']))),
            inline=False
        )
        embed.add_field(
            name="{}".format(data['requirementsEmbed']['fields']['howApply']['name']),
            value="{}".format('\n'.join(map(str, data['requirementsEmbed']['fields']['howApply']['value']))),
            inline=False
        )
        embed.add_field(
            name="{}".format(data['requirementsEmbed']['fields']['miscNotes']['name']),
            value="{}".format('\n'.join(map(str, data['requirementsEmbed']['fields']['miscNotes']['value']))),
            inline=False
        )
        embed.set_footer(
            text="{}".format(data['requirementsEmbed']['footer']['text']),
            icon_url=ctx.guild.icon_url
        )

        # Get discord.TextChannel object (via discord.Guild) for the partners channel we want to send to
        guild = discord.utils.get(
            self.bot.guilds,
            name=ctx.guild.name
        )
        channel = discord.utils.get(
            guild.text_channels,
            id=config.PARTNERS_CHANNEL_ID
        )

        req = await channel.send(embed=embed)
        logger.info(
            "Partnership Requirements Embed Sent (MSG ID: {})".format(
                req.id
            )
        )

        embed = discord.Embed(
            title="SUCCESS",
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Partnership Requirements Sent",
            value="**MSG ID:** {}".format(req.id),
            inline=False
        )
        embed.set_footer(
            text="Actioned by {}#{}".format(
                ctx.author.name,
                ctx.author.discriminator
            ),
            icon_url=ctx.author.avatar_url
        )
        await ctx.reply(embed=embed)

    @init.command()
    async def refresh(self, ctx):
        await ctx.trigger_typing()
        # Open DB file in Binary Read-Only mode
        # Binary mode is needed so that special characters (e.g. é)
        # will display properly
        with open(self.db_file_path, "rb") as f:
            data = json.load(f)
            logger.debug("JSON Data Loaded")

        # Construct new embed using updated data from our json file
        new_embed = discord.Embed(
            title="{}".format(data['requirementsEmbed']['title']),
            description="{}".format(data['requirementsEmbed']['description']),
            colour=config.BOT_COLOUR,
            timestamp=datetime.utcnow()
        )
        new_embed.add_field(
            name="{}".format(data['requirementsEmbed']['fields']['partnerReq']['name']),
            value="{}".format('\n'.join(map(str, data['requirementsEmbed']['fields']['partnerReq']['value']))),
            inline=False
        )
        new_embed.add_field(
            name="{}".format(data['requirementsEmbed']['fields']['howApply']['name']),
            value="{}".format('\n'.join(map(str, data['requirementsEmbed']['fields']['howApply']['value']))),
            inline=False
        )
        new_embed.add_field(
            name="{}".format(data['requirementsEmbed']['fields']['miscNotes']['name']),
            value="{}".format('\n'.join(map(str, data['requirementsEmbed']['fields']['miscNotes']['value']))),
            inline=False
        )
        new_embed.set_footer(
            text="{}".format(data['requirementsEmbed']['footer']['text']),
            icon_url=ctx.guild.icon_url
        )

        # Get discord.Message object (via discord.Guild and discord.TextChannel)
        # for the "requirements for partnership" message we want to edit
        guild = discord.utils.get(
            self.bot.guilds,
            name=ctx.guild.name
        )
        channel = discord.utils.get(
            guild.text_channels,
            id=config.PARTNERS_CHANNEL_ID
        )
        msg = await channel.fetch_message(
            config.PARTNERS_MSG_ID
        )

        await msg.edit(embed=new_embed)
        logger.info(
            "Partnership Requirements Embed Edited (MSG ID: {})".format(
                msg.id
            )
        )

        embed = discord.Embed(
            title="SUCCESS",
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Partnership Requirements Edited",
            value="**MSG ID:** {}".format(msg.id),
            inline=False
        )
        embed.set_footer(
            text="Actioned by {}#{}".format(
                ctx.author.name,
                ctx.author.discriminator
            ),
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)

    # For now going to lock to admins only
    # After/together with this I should create an inviteinfo command (alias = ii)
    # TODO: Local error handler? Or have I already covered most cases?
    @partner.command()
    async def add(self, ctx, invite: discord.Invite, rep: discord.Member,
                  colour: Optional[str] = None, banner: Optional[str] = None,
                  web: Optional[str] = None):
        # Handle optional attributes
        if colour is None:
            colour = discord.Embed.Empty  # Or discord.Colour.dark_theme() which would blend in with dark mode
            logger.info(
                "No colour specified, setting default discord.Embed.Empty value."
            )
        else:  # Convert string to desired base-16 integer
            colour = int(colour, 16)
            logger.debug(
                "Colour as Base-16 Integer: {}".format(colour)
            )
        if banner is None:
            banner = discord.Embed.Empty
            logger.info(
                "No banner specified, setting default discord.Embed.Empty value."
            )
        if web is None:
            web = discord.Embed.Empty

        # Confirm invite returns a valid guild
        if invite.guild is None:
            embed = discord.Embed(
                title="ERROR",
                description="A guild object could not be obtained from the "
                            "provided invite, perhaps it was for a Group DM?",
                colour=config.BOT_ERR_COLOUR,
                timestamp=datetime.utcnow()
            )
            embed.set_author(
                name=config.BOT_AUTHOR_NAME,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.set_footer(
                text="Offending Invite: {}".format(invite.url)
            )
            await ctx.message.delete()  # Delete command invokation
            await ctx.channel.send(embed=embed)
            logger.info(
                "No guild found, terminating command execution."
            )
            logger.info(
                "Offending Invite: {}".format(invite.url)
            )
            return

        embed = discord.Embed(
            title="PARTNERSHIP MENU",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Server Description",
            value="Please enter the accompanying server description/"
                  "advertisement for {}.".format(invite.guild.name),
            inline=False
        )
        embed.set_footer(
            text="Actioned by {}#{}".format(
                ctx.author.name,
                ctx.author.discriminator
            ),
            icon_url=ctx.author.avatar_url
        )
        desc_embed = await ctx.channel.send(embed=embed)

        # We only want a response from the user who invoked this command
        def check(m):
            return m.author == ctx.author

        # Get the server partner's description/advertisement
        try:
            logger.debug(
                "Awaiting input from author for partner description"
            )
            provided_desc = await self.bot.wait_for(
                "message",
                timeout=60.0,
                check=check
            )
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="WARNING",
                colour=config.BOT_ERR_COLOUR
            )
            embed.set_author(
                name=config.BOT_AUTHOR_NAME,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.add_field(
                name="Partner Add Cancelled",
                value="This action timed-out",
                inline=False
            )
            embed.set_footer(
                text="Actioned by {}".format(ctx.author),
                icon_url=ctx.author.avatar_url
            )
            await desc_embed.edit(embed=embed)
            logger.debug(
                "Action timed out"
            )
            return

        # Construct embed object
        embed = discord.Embed(
            title="{}".format(invite.guild.name),
            description="{}".format(provided_desc.content),
            colour=colour,
            url=web,
            timestamp=datetime.utcnow()
        )
        embed.add_field(
            name="{} Representative".format("\U0001f465"),
            value="{}".format(rep.mention)
        )
        embed.add_field(
            name="{} Invite".format("\U0001f517"),
            value="**{}**".format(invite.url)
        )
        embed.set_thumbnail(
            url=invite.guild.icon_url
        )
        embed.set_image(
            url=banner
        )
        embed.set_footer(
            text="Northbridge Café Partnership Program",
            icon_url=ctx.guild.icon_url
        )

        await provided_desc.delete()
        await ctx.message.delete()
        logger.debug(
            "Deleted message containing server description"
        )
        logger.debug(
            "Deleted command invokation"
        )

        # Get object of the channel we want to send to
        guild = discord.utils.get(
            self.bot.guilds,
            name=ctx.guild.name
        )
        channel = discord.utils.get(
            guild.text_channels,
            id=config.PARTNERS_CHANNEL_ID
        )
        logger.debug(
            "Fetched channel {}({}) from guild {}({})".format(
                channel.name,
                channel.id,
                guild.name,
                guild.id
            )
        )

        # Send the given information about the new partner to our
        # public #partners channel
        msg = await channel.send(embed=embed)
        logger.info(
            "New Partner Added By {} (MSG ID: {})".format(
                ctx.author,
                msg.id
            )
        )

        embed = discord.Embed(
            title="SUCCESS",
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Partner Added",
            value="**MSG ID:** {}".format(msg.id),
            inline=False
        )
        embed.set_footer(
            text="Actioned by {}#{}".format(
                ctx.author.name,
                ctx.author.discriminator
            ),
            icon_url=ctx.author.avatar_url
        )
        await desc_embed.edit(
            embed=embed
        )

    @partner.command()
    async def edit(self, ctx, message: int, invite: discord.Invite,
                   rep: discord.Member, colour: Optional[str] = None,
                   banner: Optional[str] = None, web: Optional[str] = None):
        # Handle optional attributes
        if colour is None:
            colour = discord.Embed.Empty  # Or discord.Colour.dark_theme() which would blend in with dark mode
            logger.info(
                "No colour specified, setting default discord.Embed.Empty value."
            )
        else:  # Convert string to desired base-16 integer
            colour = int(colour, 16)
            logger.debug(
                "Colour as Base-16 Integer: {}".format(colour)
            )
        if banner is None:
            banner = discord.Embed.Empty
            logger.info(
                "No banner specified, setting default discord.Embed.Empty value."
            )
        if web is None:
            web = discord.Embed.Empty

        # Confirm invite returns a valid guild
        if invite.guild is None:
            embed = discord.Embed(
                title="ERROR",
                description="A guild object could not be obtained from the "
                            "provided invite, perhaps it was for a Group DM?",
                colour=config.BOT_ERR_COLOUR,
                timestamp=datetime.utcnow()
            )
            embed.set_author(
                name=config.BOT_AUTHOR_NAME,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.set_footer(
                text="Offending Invite: {}".format(invite.url)
            )
            await ctx.message.delete()  # Delete command invokation
            await ctx.channel.send(embed=embed)
            logger.info(
                "No guild found, terminating command execution."
            )
            logger.info(
                "Offending Invite: {}".format(invite.url)
            )
            return

        embed = discord.Embed(
            title="PARTNERSHIP MENU",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Server Description",
            value="Please enter the accompanying server description/"
                  "advertisement for {}.".format(invite.guild.name),
            inline=False
        )
        embed.set_footer(
            text="Actioned by {}#{}".format(
                ctx.author.name,
                ctx.author.discriminator
            ),
            icon_url=ctx.author.avatar_url
        )
        desc_embed = await ctx.channel.send(embed=embed)

        # We only want a response from the user who invoked this command
        def check(m):
            return m.author == ctx.author

        # Get the updated description/advertisement for the specified
        # server partner
        try:
            logger.debug(
                "Awaiting input from author for updated partner description"
            )
            provided_desc = await self.bot.wait_for(
                "message",
                timeout=60.0,
                check=check
            )
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="WARNING",
                colour=config.BOT_ERR_COLOUR
            )
            embed.set_author(
                name=config.BOT_AUTHOR_NAME,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.add_field(
                name="Partner Edit Cancelled",
                value="This action timed-out",
                inline=False
            )
            embed.set_footer(
                text="Actioned by {}".format(ctx.author),
                icon_url=ctx.author.avatar_url
            )
            await desc_embed.edit(embed=embed)
            logger.debug(
                "Action timed out"
            )
            return

        # Construct embed object
        new_embed = discord.Embed(
            title="{}".format(invite.guild.name),
            description="{}".format(provided_desc.content),
            colour=colour,
            url=web,
            timestamp=datetime.utcnow()
        )
        new_embed.add_field(
            name="{} Representative".format("\U0001f465"),
            value="{}".format(rep.mention)
        )
        new_embed.add_field(
            name="{} Invite".format("\U0001f517"),
            value="**{}**".format(invite.url)
        )
        new_embed.set_thumbnail(
            url=invite.guild.icon_url
        )
        new_embed.set_image(
            url=banner
        )
        new_embed.set_footer(
            text="Northbridge Café Partnership Program",
            icon_url=ctx.guild.icon_url
        )

        await provided_desc.delete()
        await ctx.message.delete()
        logger.debug(
            "Deleted message containing server description"
        )
        logger.debug(
            "Deleted command invokation"
        )

        # Get object of the message we want to edit
        guild = discord.utils.get(
            self.bot.guilds,
            name=ctx.guild.name
        )
        channel = discord.utils.get(
            guild.text_channels,
            id=config.PARTNERS_CHANNEL_ID
        )
        msg = await channel.fetch_message(
            message
        )
        logger.debug(
            "Fetched message with ID {} from channel {}({}) in guild {}({})".format(
                msg.id,
                channel.name,
                channel.id,
                guild.name,
                guild.id
            )
        )

        # Edit the specified partner from our public #partners channel
        # with the updated information
        await msg.edit(embed=new_embed)
        logger.info(
            "Partner '{}' Edited By {} (MSG ID: {})".format(
                invite.guild.name,
                ctx.author,
                msg.id
            )
        )

        embed = discord.Embed(
            title="SUCCESS",
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Partner Edited",
            value="**MSG ID:** {}".format(msg.id),
            inline=False
        )
        embed.set_footer(
            text="Actioned by {}#{}".format(
                ctx.author.name,
                ctx.author.discriminator
            ),
            icon_url=ctx.author.avatar_url
        )
        await desc_embed.edit(
            embed=embed
        )


def setup(bot):
    bot.add_cog(Partners(bot))
