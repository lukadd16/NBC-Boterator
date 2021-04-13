# Description: Cog with commands relevant to new server partnership system

import app_logger
import asyncio
import config
import discord
import json
import os

from datetime import datetime
from discord.ext import commands
from discord.ext.commands import ColourConverter
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


class PColour(commands.Converter):
    async def convert(self, ctx, argument: str):
        print("REACH")
        if argument is None:  # TODO: will never get called
            print("REACH IF")
            colour = config.DISC_DARK_EMBED_BG
            logger.info(
                "No colour specified, returning DARK_EMBED_BG constant."
            )
        else:
            print("REACH ELSE")
            colour = await ColourConverter.convert(ctx, argument)  # Use built-in discord.py converter
            print("REACH POST CONVERT")
            logger.debug(
                "Colour Post-Conversion: {}".format(colour)
            )
        return colour

# BANNER AND WEBSITE DON'T FIT THE USE CASE OF CONVERTERS (since we're not really manipulating the arg at all)

# class PBanner(commands.Converter):
#     async def convert(self, ctx, argument: str):
#         print(argument)
#
#         if argument is None:
#             logger.info(
#                 "No banner specified, returning default discord.Embed.Empty value."
#             )
#             return discord.Embed.Empty
#
#
# # TODO: Not sure if need to explicitly pass argument back if not manipulating it
# class PWebsite(commands.Converter):
#     async def convert(self, ctx, argument: str):
#         print(argument)
#
#         if argument is None:
#             logger.info(
#                 "No website specified, returning default discord.Embed.Empty value."
#             )
#             return discord.Embed.Empty
#         # else:
#         #     return None


class InviteValueError(ValueError):
    """Raise when the provided invite was of the correct format but did not point to a valid guild"""
    def __init__(self, message: str, invite: discord.Invite):
        self.message = message
        self.invite = invite  # The offending invite that caused the error
        super(InviteValueError, self).__init__(message, invite)


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

    # Returns a discord.TextChannel object for the #partners channel defined in our config file
    def get_channel(self, ctx) -> discord.TextChannel:
        guild = discord.utils.get(
            self.bot.guilds,
            name=ctx.guild.name
        )
        target_channel = discord.utils.get(
            guild.text_channels,
            id=config.PARTNERS_CHANNEL_ID
        )
        return target_channel

    # Returns a discord.Message object for a message in the #partners channel
    # whose ID matches the one passed in.
    async def get_msg(self, ctx, mid: int) -> discord.Message:
        part_channel = self.get_channel(
            ctx
        )
        target_msg = await part_channel.fetch_message(
            mid
        )
        return target_msg

    @staticmethod
    def check_banner_arg(banner):
        if banner is None:
            logger.info(
                "No banner specified, returning default discord.Embed.Empty value."
            )
            return discord.Embed.Empty
        else:
            return banner

    @staticmethod
    def check_web_arg(website):
        if website is None:
            logger.info(
                "No website specified, returning default discord.Embed.Empty value."
            )
            return discord.Embed.Empty
        else:
            return None

    # NOTE: declaring a cog-level error handler like this effectively overrides my global one
    #       By doing so none of my already defined handlers such as NotOwner get called (and would have to be rewritten here)
    #       So instead, just going to add the necessary handlers to the global one

    # async def cog_command_error(self, ctx, error):
    #     if isinstance(error, InviteValueError):
    #         embed = discord.Embed(
    #             title="ERROR",
    #             description="A guild object could not be obtained from the "
    #                         "provided invite, perhaps it was for a Group DM?",
    #             colour=config.BOT_ERR_COLOUR,
    #             timestamp=datetime.utcnow()
    #         )
    #         embed.set_author(
    #             name=config.BOT_AUTHOR_NAME,
    #             url=config.WEBSITE_URL,
    #             icon_url=self.bot.user.avatar_url
    #         )
    #         embed.set_footer(
    #             text="Offending Invite: {}".format(error.invite.url)
    #         )
    #         await ctx.message.delete()  # Delete command invocation
    #         await ctx.send(embed=embed)
    #         logger.info(
    #             "No guild found, terminating command execution."
    #         )
    #         logger.info(
    #             "Offending Invite: {}".format(error.invite.url)
    #         )
    #
    #     elif isinstance(error, discord.Forbidden):
    #         pass
    #
    #     elif isinstance(error, discord.NotFound):
    #         pass

    @commands.group(aliases=["partners"])
    async def partner(self, ctx):
        # Could use the base command to explain how to partner, etc. (could also add a link via MD to the requirements embed)
        # E.g. Want to partner with us? Just head on over to [this]() message to learn how!
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "You did not specify a subcommand. Valid subcommands are:"
                "\n>>> `init`"
                "\n`init refresh`"
                "\n`add`"
                "\n`edit`"
            )

    # Sends the requirements for partnership message to the set partners channel
    @partner.group()
    async def init(self, ctx):
        # If the refresh subcommand was specified, prevent the bare init command from continuing.
        # TODO: figure out if there's a native way to handle this behaviour.
        if ctx.invoked_subcommand is not None:
            return

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

        # Get TextChannel object for the channel we want to send the embed to
        target = self.get_channel(ctx)

        req_msg = await target.send(embed=embed)
        logger.info(
            "Partnership Requirements Embed Sent (MSG ID: {})".format(
                req_msg.id
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
            value="**MSG ID:** {}".format(req_msg.id),
            inline=False
        )
        embed.set_footer(
            text="Actioned by {0.name}#{0.discriminator}".format(
                ctx.author
            ),
            icon_url=ctx.author.avatar_url
        )
        await ctx.reply(embed=embed)

    @init.command()
    async def refresh(self, ctx):
        await ctx.trigger_typing()
        # Open DB file in Binary Read-Only mode
        # Binary mode is needed so that special characters (e.g. é) will display properly
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

        # Get Message object for the "requirements for partnership" message we want to edit
        target = await self.get_msg(ctx, config.PARTNERS_MSG_ID)

        await target.edit(embed=new_embed)
        logger.info(
            "Partnership Requirements Embed Edited (MSG ID: {})".format(
                target.id
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
            value="**MSG ID:** {}".format(target.id),
            inline=False
        )
        embed.set_footer(
            text="Actioned by {0.name}#{0.discriminator}".format(
                ctx.author
            ),
            icon_url=ctx.author.avatar_url
        )
        await ctx.reply(embed=embed)

    # For now going to lock to admins only
    # After/together with this I should create an inviteinfo command (alias = ii)
    # TODO: Add cog-level error handler for 403 Forbidden and 404 Not Found errors (latter of which can occur when the msgID does not exist in the partners channel)
    @partner.command()
    async def add(self, ctx, invite: discord.Invite, rep: discord.Member,
                  colour: Optional[ColourConverter] = None, banner: Optional[str] = None,
                  web: Optional[str] = None):
        # Confirm invite points to a valid guild
        if invite.guild is None:
            raise InviteValueError("Invite has no guild associated with it", invite)  # TODO: test this, do I need to have a message arg?

        # Handle optional parameters and populate them with an appropriate
        # default value (such as discord.Embed.Empty) if a value was not provided.
        banner = self.check_banner_arg(banner)
        web = self.check_web_arg(web)

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
            text="Actioned by {0.name}#{0.discriminator}".format(
                ctx.author
            ),
            icon_url=ctx.author.avatar_url
        )
        desc_embed = await ctx.reply(embed=embed)

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

        # Construct embed containing info related to the partner
        embed = discord.Embed(
            title="{}".format(invite.guild.name),
            description="{}".format(provided_desc.content),
            colour=colour,
            url=web,
            timestamp=datetime.utcnow()
        )
        embed.add_field(
            name="{} Representative".format(config.PARTNER_EMOJI_REP),
            value="{}".format(rep.mention)
        )
        embed.add_field(
            name="{} Invite".format(config.PARTNER_EMOJI_INVITE),
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
            "Deleted author input message containing server description"
        )
        logger.debug(
            "Deleted command invocation"
        )

        # Get TextChannel object for the channel we want to send the embed to
        target = self.get_channel(ctx)  # TODO: test this

        logger.debug(
            "Fetched channel {0.name}({0.id}) from guild {1.name}({1.id})".format(
                target,
                target.guild,  # TODO: test this
            )
        )

        # Send the given information about the new partner to our public #partners channel
        partner_msg = await target.send(embed=embed)
        logger.info(
            "New Partner Added By {} (MSG ID: {})".format(
                ctx.author,
                partner_msg.id
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
            value="**MSG ID:** {}".format(partner_msg.id),
            inline=False
        )
        embed.set_footer(
            text="Actioned by {}#{}".format(
                ctx.author.name,
                ctx.author.discriminator
            ),
            icon_url=ctx.author.avatar_url
        )
        await desc_embed.edit(embed=embed)

    @partner.command()
    async def edit(self, ctx, message: int, invite: discord.Invite,
                   rep: discord.Member, colour: Optional[PColour] = None,
                   banner: Optional[str] = None, web: Optional[str] = None):
        # Confirm invite points to a valid guild
        if invite.guild is None:
            raise InviteValueError("Invite has no guild associated with it", invite)

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
            "Deleted author input message containing server description"
        )
        logger.debug(
            "Deleted command invocation"
        )

        # Get Message object for the existing partner embed we want to edit
        target = await self.get_msg(ctx, message)
        logger.debug(
            "Fetched message with ID {0.id} from channel {1.name}({1.id}) in guild {2.name}({2.id})".format(  # TODO: test this
                target,
                target.channel,
                target.guild
            )
        )

        # Edit the specified partner from our public #partners channel with the updated details
        await target.edit(embed=new_embed)
        logger.info(
            "Partner '{0.name}' Edited By {1.author} (MSG ID: {2.id})".format(  # TODO: test this
                invite.guild,
                ctx,
                target
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
            value="**MSG ID:** {}".format(target.id),
            inline=False
        )
        embed.set_footer(
            text="Actioned by {}#{}".format(
                ctx.author.name,
                ctx.author.discriminator
            ),
            icon_url=ctx.author.avatar_url
        )
        await desc_embed.edit(embed=embed)


def setup(bot):
    bot.add_cog(Partners(bot))
