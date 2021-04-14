# Description: Cog with commands relevant to new server partnership system

import app_logger
import asyncio
import config
import discord
import json
import os

from datetime import datetime
from discord.ext import commands
from discord.ext.commands import ColourConverter, InviteConverter, MemberConverter
from typing import Optional, Union

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


class InviteValueError(ValueError):
    """Raise when the provided invite was of the correct format but did not point to a valid guild"""
    def __init__(self, message: str, invite: discord.Invite):
        self.message = message
        self.invite = invite  # The offending invite that caused the error
        super(InviteValueError, self).__init__(message, invite)


class Partners(commands.Cog):
    # Embed descriptions can be up to 2048 characters in length
    # Ref: https://discordjs.guide/popular-topics/embeds.html
    MAX_DESCRIPTION_LENGTH = 2048

    def __init__(self, bot):
        self.bot = bot
        self.db_file_path = self._init_db()
        self.fields = {
            0: ["description", "desc"],
            1: ["invite", "inv"],
            2: ["representative", "rep"],
            3: ["colour", "color"],
            4: ["banner", "thumb"],
            5: ["website", "web"]
        }

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

    def validate_description(self, ctx, desc):
        if desc is None:
            logger.info(
                "No description specified, sending error message to author context."
            )
            embed = discord.Embed(
                title="ERROR",
                description="Partner description cannot be blank.",
                colour=config.BOT_ERR_COLOUR,
                timestamp=datetime.utcnow()
            )
            embed.set_author(
                name=config.BOT_AUTHOR_NAME,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            ctx.reply(embed=embed)
            return

        if len(desc) > self.MAX_DESCRIPTION_LENGTH:
            logger.info(
                "Provided description is too long, sending error message to author context."
            )
            embed = discord.Embed(
                title="ERROR",
                description="Partner description is too long ({}/{}).".format(len(desc), self.MAX_DESCRIPTION_LENGTH),
                colour=config.BOT_ERR_COLOUR,
                timestamp=datetime.utcnow()
            )
            embed.set_author(
                name=config.BOT_AUTHOR_NAME,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            ctx.reply(embed=embed)
            return

        return desc

    def validate_invite(self, ctx, inv):
        if inv is None:
            logger.info(
                "No invite specified, sending error message to author context."
            )
            embed = discord.Embed(
                title="ERROR",
                description="Invite field cannot be blank.",
                colour=config.BOT_ERR_COLOUR,
                timestamp=datetime.utcnow()
            )
            embed.set_author(
                name=config.BOT_AUTHOR_NAME,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            ctx.reply(embed=embed)
            return

        try:
            inv = await InviteConverter().convert(ctx, inv)
        except:  # Whichever error was associated with failed conversion
            pass  # Send error message
            return

        # Confirm invite points to a valid guild
        if inv.guild is None:
            raise InviteValueError("Invite has no guild associated with it", inv)

        return inv

    def validate_representative(self, ctx, rep):
        if rep is None:
            logger.info(
                "No representative specified, sending error message to author context."
            )
            pass  # Send error message; Missing required arg
            return

        try:
            pass  # MemberConverter
        except:  # Error for failed conversion
            pass  # Send error message
            return

        return rep

    def validate_colour(self, ctx, colour):
        if colour is None:
            logger.info(
                "No colour specified, returning DARK_EMBED_BG constant."
            )
            return config.DISC_DARK_EMBED_BG

        try:
            colour = await ColourConverter().convert(ctx, colour)
        except:  # Error for failed conversion
            pass  # Send error message
            return

        return colour

    # Does not actually validate that URL actually points to a file, but rather the existence of the arg.
    def validate_banner(self, ctx, banner):
        if banner is None:
            logger.info(
                "No banner specified, returning default discord.Embed.Empty value."
            )
            return discord.Embed.Empty

        return banner

    # Does not actually validate that URL actually points to a website, but rather the existence of the arg.
    def validate_website(self, ctx, web):
        if web is None:
            logger.info(
                "No website specified, returning default discord.Embed.Empty value."
            )
            return discord.Embed.Empty

        return web

    @staticmethod
    def hex(decimal: Union[str, int]) -> str:
        """Converts a decimal value into its uppercase hex value with the leading 0x
        character sequence stripped."""
        if isinstance(decimal, str):
            return hex(int(decimal)).lstrip("0x").upper()
        if isinstance(decimal, int):
            return hex(decimal).lstrip("0x").upper()
        raise ValueError("You must pass either an int or a str")

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

    @commands.group(aliases=["partners"], invoke_without_command=True)
    async def partner(self, ctx):
        # Could use the base command to explain how to partner, etc. (could also add a link via MD to the requirements embed)
        # E.g. Want to partner with us? Just head on over to [this]() message to learn how!
        await ctx.send(
            "You did not specify a subcommand. Valid subcommands are:"
            "\n>>> `init`"
            "\n`init refresh`"
            "\n`add`"
            "\n`edit`"
        )

    # Sends the requirements for partnership message to the set partners channel
    @partner.group(invoke_without_command=True)
    async def init(self, ctx):
        # If the refresh subcommand was specified, prevent the bare init command from continuing.
        # TODO: figure out if there's a native way to handle this behaviour.
        # if ctx.invoked_subcommand is not None:
        #     return

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
            colour=config.DISC_DARK_EMBED_BG,
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

    # TODO: After/together with this I should create an inviteinfo command (alias = ii)
    # TODO: Add global error handler for 403 Forbidden and 404 Not Found errors (latter of which can occur when the msgID does not exist in the partners channel)
    @partner.command()
    async def add(self, ctx, invite: discord.Invite, rep: discord.Member,
                  colour: Optional[ColourConverter] = None, banner: Optional[str] = None,
                  web: Optional[str] = None):
        # Confirm invite points to a valid guild
        if invite.guild is None:
            raise InviteValueError("Invite has no guild associated with it", invite)

        # Handle optional parameters and populate them with an appropriate
        # default value (such as discord.Embed.Empty) if a value was not provided.
        banner = self.validate_banner(ctx, banner)
        web = self.validate_website(ctx, web)

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

        # We only want a response from the user who invoked the command
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
        target = self.get_channel(ctx)

        logger.debug(
            "Fetched channel #{0.name} ({0.id}) from guild {1.name} ({1.id})".format(
                target,
                target.guild
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
    async def edit(self, ctx, message: int, field: str, *, value=None):
        # Get Message object for the existing partner embed we want to edit
        target = await self.get_msg(ctx, message)
        logger.debug(
            "Fetched message with ID {0.id} from channel {1.name} ({1.id}) in guild {2.name} ({2.id})".format(
                target,
                target.channel,
                target.guild
            )
        )

        logger.debug("Field arg = {}".format(field))
        logger.debug("Value arg = {}".format(value))

        # TODO: encapsulate all data validation and conversions in static methods (like already existing check_web and check_banner)
        if any(field in ele for ele in self.fields.values()):  # Valid field was provided
            if field in self.fields.get(0):  # Embed Description
                # Perform data validation on value arg
                value = self.validate_description(ctx, value)

                # Call method from current context to edit partner description
                # Note: ctx.invoke() ignores all checks and converters of the command being called
                # Ref: https://discordpy.readthedocs.io/en/stable/ext/commands/api.html?highlight=context%20invoke#discord.ext.commands.Context.invoke
                await ctx.invoke(self.bot.get_command("_edit_description"), target=target, new_desc=value)  # TODO: going to experiment with passing desc directly to edit command (on new line)
            elif field in self.fields.get(1):  # Embed Invite Field
                # if value is None:
                # else:
                #     value = await InviteConverter().convert(ctx, value)  # TODO: ctx invoking ignores checks and converters, so must perform manually prior to calling meth
                # print(value)

                # Validate value arg contains has a non-default value

                # Perform data validation on value arg
                value = self.validate_invite(ctx, value)

                # Call method to edit partner invite
                await ctx.invoke(self.bot.get_command("_edit_invite_field"), target=target, new_invite=value)
            elif field in self.fields.get(2):  # Embed Representative Field

                # Perform data validation
                value = await MemberConverter().convert(ctx, value)

                # Call method to edit partner representative
                await ctx.invoke(self.bot.get_command("_edit_representative_field"), target=target, new_rep=value)
            elif field in self.fields.get(3):  # Embed Colour
                # Perform data validation
                value = self.validate_colour(ctx, value)
                # Call method to edit partner (embed) colour
                await ctx.invoke(self.bot.get_command("_edit_embed_colour"), target=target, new_colour=value)
            elif field in self.fields.get(4):  # Embed Thumbnail
                # Perform data validation
                value = self.validate_banner(ctx, value)
                # Call method to edit partner banner
                await ctx.invoke(self.bot.get_command("_edit_embed_thumbnail"), target=target, new_banner=value)
            else:  # Embed URL
                # Perform data validation
                value = self.validate_website(ctx, value)
                # Call method to edit partner embed website
                await ctx.invoke(self.bot.get_command("_edit_embed_url"), target=target, new_website=value)
        else:  # Invalid field was specified
            await ctx.send(
                "You did not specify a valid field to edit. Valid options are:"
                f"\n>>> `{self.fields.get(0)}`"
                f"\n`{self.fields.get(1)}`"
                f"\n`{self.fields.get(2)}`"
                f"\n`{self.fields.get(3)}`"
                f"\n`{self.fields.get(4)}`"
                f"\n`{self.fields.get(5)}`"
            )

    @commands.command()
    async def _edit_description(self, ctx, target: discord.Message, new_desc: str) -> None:
        # Get embed attached to the target message
        embed = target.embeds[0]

        # Convert embed to a mutable dictionary
        data = embed.to_dict()

        # Obtain the existing description
        cur_desc = data["description"]  # TODO: use [] access syntax

        # Set the description in the dictionary to the new one
        data["description"] = new_desc

        # Update timestamp with the current time in required ISO8601 format
        data["timestamp"] = datetime.utcnow().isoformat()

        # Convert the dictionary to a discord.Embed object
        new_embed = discord.Embed.from_dict(data)

        # Edit the target message with our new embed
        await target.edit(embed=new_embed)

        # Action complete, report status to context author
        embed = discord.Embed(
            title="SUCCESS: Partner Description Updated",
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="OLD",  # TODO: underline?
            value="```{}```".format(cur_desc),
            inline=True
        )
        embed.add_field(
            name="NEW",
            value="```{}```".format(new_desc),
            inline=True
        )
        embed.set_footer(
            text="Actioned by {0.name}#{0.discriminator}".format(
                ctx.author
            ),
            icon_url=ctx.author.avatar_url
        )
        await ctx.reply(embed=embed)

        # await provided_desc.delete()
        # await ctx.message.delete()
        # logger.debug(
        #     "Deleted author input message containing server description"
        # )
        # logger.debug(
        #     "Deleted command invocation"
        # )

        # # Get Message object for the existing partner embed we want to edit
        # target = await self.get_msg(ctx, message)
        # logger.debug(
        #     "Fetched message with ID {0.id} from channel {1.name} ({1.id}) in guild {2.name} ({2.id})".format(
        #         target,
        #         target.channel,
        #         target.guild
        #     )
        # )

        # await target.edit(embed=new_embed)
        # logger.info(
        #     "Partner '{0.name}' Edited By {1.author} (MSG ID: {2.id})".format(
        #         invite.guild,
        #         ctx,
        #         target
        #     )
        # )

    @commands.command()
    async def _edit_invite_field(self, ctx, target: discord.Message, new_invite: discord.Invite) -> None:
        # Get embed attached to the target message
        embed = target.embeds[0]

        # Convert embed to a mutable dictionary
        data = embed.to_dict()

        # Obtain existing invite
        cur_invite = data["fields"][1]["value"]  # TODO: test syntax

        # Set the value for the invite field in the dictionary to the new one
        new_invite = "**{}**".format(new_invite.url)  # Match existing bold text formatting
        data["fields"][1]["value"] = new_invite

        # Update timestamp with the current time in required ISO8601 format
        data["timestamp"] = datetime.utcnow().isoformat()

        # Convert the dictionary to a discord.Embed object
        new_embed = discord.Embed.from_dict(data)

        # Edit the target message with our new embed
        await target.edit(embed=new_embed)

        # Action complete, report status to context author
        embed = discord.Embed(
            title="SUCCESS: Partner Invite Updated",
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="OLD",
            value="```{}```".format(cur_invite),  # TODO: obtained invite from old goes here
            inline=True
        )
        embed.add_field(
            name="NEW",
            value="```{}```".format(new_invite),
            inline=True
        )
        embed.set_footer(
            text="Actioned by {0.name}#{0.discriminator}".format(
                ctx.author
            ),
            icon_url=ctx.author.avatar_url
        )
        await ctx.reply(embed=embed)

    @commands.command()
    async def _edit_representative_field(self, ctx, target: discord.Message, new_rep: discord.Member) -> None:
        # Get embed attached to the target message
        embed = target.embeds[0]

        # Convert embed to a mutable dictionary
        data = embed.to_dict()

        # Obtain existing representative (as string)
        cur_rep = data["fields"][0]["value"]

        # # Convert rep to a Member object
        # cur_rep = await MemberConverter().convert(ctx, cur_rep)

        # Set the value for the representative field in the dictionary to the new one
        data["fields"][0]["value"] = new_rep.mention

        # Update timestamp
        data["timestamp"] = datetime.utcnow().isoformat()

        # Convert the dictionary to a discord.Embed object
        new_embed = discord.Embed.from_dict(data)

        # Edit the target message with our new embed
        await target.edit(embed=new_embed)

        # Action complete, report status to context author
        embed = discord.Embed(
            title="SUCCESS: Partner Representative Updated",
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="OLD",
            value="```{0.name}#{0.discriminator} ({0.id})```".format(cur_rep),  # TODO: obtained rep from old goes here
            inline=True
        )
        embed.add_field(
            name="NEW",
            value="```{0.name}#{0.discriminator} ({0.id})```".format(new_rep),
            inline=True
        )
        embed.set_footer(
            text="Actioned by {0.name}#{0.discriminator}".format(
                ctx.author
            ),
            icon_url=ctx.author.avatar_url
        )
        await ctx.reply(embed=embed)

    @commands.command()
    async def _edit_embed_colour(self, ctx, target: discord.Message, new_colour: discord.Colour) -> None:
        # Get embed attached to the target message
        embed = target.embeds[0]

        # Convert embed to a mutable dictionary
        data = embed.to_dict()

        # Obtain existing colour
        cur_colour = self.hex(data["colour"])

        # Set the embed's colour in the dictionary to the new one
        data["colour"] = new_colour.value  # Value attr returns the base 10 decimal that represents the colour object

        # Update timestamp
        data["timestamp"] = datetime.utcnow().isoformat()

        # Convert the dictionary to a discord.Embed object
        new_embed = discord.Embed.from_dict(data)

        # Edit the target message with our new embed
        await target.edit(embed=new_embed)

        # Action complete, report status to context author
        embed = discord.Embed(
            title="SUCCESS: Partner Embed Colour Updated",
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="OLD",
            value="```{}```".format(cur_colour),  # TODO: obtained colour from old goes here
            inline=True
        )
        embed.add_field(
            name="NEW",
            value="```{}```".format(self.hex(new_colour.value)),
            inline=True
        )
        embed.set_footer(
            text="Actioned by {0.name}#{0.discriminator}".format(
                ctx.author
            ),
            icon_url=ctx.author.avatar_url
        )
        await ctx.reply(embed=embed)

    @commands.command()
    async def _edit_embed_thumbnail(self, ctx, target: discord.Message, new_banner: str) -> None:
        # Get embed attached to the target message
        embed = target.embeds[0]

        # Convert embed to a mutable dictionary
        data = embed.to_dict()

        # Obtain URL of existing banner (thumbnail)
        # TODO: access thumbnail attr of the embed (and from thumbnail, url)
        cur_banner = data["thumbnail"]["url"]

        # Set thumbnail URL in the dictionary to the new one
        # TODO: use built-in set_thumbnail() meth
        data["thumbnail"]["url"] = new_banner

        # Update timestamp
        # TODO: not sure how going to manage this without embed as dict
        data["timestamp"] = datetime.utcnow().isoformat()

        # Convert the dictionary to a discord.Embed object
        new_embed = discord.Embed.from_dict(data)

        # Edit the target message with our new embed
        await target.edit(embed=new_embed)

        # Action complete, report status to context author
        embed = discord.Embed(
            title="SUCCESS: Partner Banner Updated",
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="OLD",
            value="```{}```".format(cur_banner),  # TODO: obtained url from old goes here
            inline=True
        )
        embed.add_field(
            name="NEW",
            value="```{}```".format(new_banner),
            inline=True
        )
        embed.set_footer(
            text="Actioned by {0.name}#{0.discriminator}".format(
                ctx.author
            ),
            icon_url=ctx.author.avatar_url
        )
        await ctx.reply(embed=embed)

    @commands.command()
    async def _edit_embed_url(self, ctx, target: discord.Message, new_website: str) -> None:
        # Get embed attached to the target message
        embed = target.embeds[0]

        # Convert embed to a mutable dictionary
        data = embed.to_dict()

        # Obtain existing title URL
        cur_website = data["url"]

        # Set the embed's URL to the new one
        data["url"] = new_website

        # Update timestamp
        data["timestamp"] = datetime.utcnow().isoformat()

        # Convert the dictionary to a discord.Embed object
        new_embed = discord.Embed.from_dict(data)

        # Edit the target message with our new embed
        await target.edit(embed=new_embed)

        # Action complete, report status to context author
        embed = discord.Embed(
            title="SUCCESS: Partner Website Updated",
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="OLD",
            value="```{}```".format(cur_website),  # TODO: obtained URL from old goes here
            inline=True
        )
        embed.add_field(
            name="NEW",
            value="```{}```".format(new_website),
            inline=True
        )
        embed.set_footer(
            text="Actioned by {0.name}#{0.discriminator}".format(
                ctx.author
            ),
            icon_url=ctx.author.avatar_url
        )
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Partners(bot))
