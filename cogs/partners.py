# Description: Cog with commands relevant to new server partnership system

import app_logger
import asyncio
import config
import discord
import json
import os

from datetime import datetime
from discord.ext import commands

logger = app_logger.get_logger(__name__)

# Two commands: addpartner, editpartner
#   - Haven't decided but would make more sense that addpartner resolves server name, server icon, those things from the provided invite
#   --> Args using invite method: self, ctx, invite, description (or type this in an interactive menu later?), banner = None (which can be different from server banner), colour: str = discord.Embed.empty (when asking in interactive menu, either say default or type the hex code), ???
#   --> Args using manual method: self, ctx, title, description, banner, colour, invite, ???
#
#   - editpartner would take msgID as an arg, then interactive menu will ask which part want to edit (type 1 for all, 2 for title, 3 for desc, etc.)
#   --> Remember, not sending a new embed, merely editing the one that is already there (figure out how retrieving the embed will work)

# Reference "refresh" command for how to edit an existing embed

# Could integrate ext.Menus reaction menu functionality into the confirmation at the end (e.g. "Here is a preview of the embed, does everything look good? Please react below.")
# Didn't work last time I tried, but will attempt to use emoji check for final confirmation (not sure what want behaviour to be yet though)

# Add logger events where necessary

db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")
db_dir = os.path.join(db_dir, "db")
db_file_name = "partners.json"
db_file_path = os.path.join(db_dir, db_file_name)
logger.info("JSON File Path: {}".format(db_file_path))


class Partners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.partner_channel = self.bot.get_channel(
        #     config.PARTNERS_CHANNEL_ID
        # )
        # self.partner_msg = self.partner_channel.fetch_message(
        #     config.PARTNERS_MSG_ID
        # )

    def cog_unload(self):
        for h in logger.handlers:
            logger.removeHandler(h)

    @commands.group(aliases=["partners"])
    @commands.has_guild_permissions()
    async def partner(self, ctx):
        # Could use the base command to explain how to partner, etc. (could also add a link via MD to the requirements embed)
        # E.g. Want to partner with us? Just head on over to [this]() message to learn how!
        pass

    @partner.command(aliases=["send", "sreq"])
    @commands.has_guild_permissions(administrator=True)
    async def send_requirements(self, ctx):
        with open(db_file_path, "rb") as f:
            data = json.load(f)
            logger.debug("JSON Data Loaded")

        # Construct initial embed using data from our json file
        embed = discord.Embed(
            title="{}".format(data['requirementsEmbed']['title']),
            description="{}".format(data['requirementsEmbed']['description']),
            colour=config.BOT_COLOUR,
            timestamp=datetime.utcnow()  # This attr is timezone aware
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

        # Get object of the channel we want to send to
        guild = discord.utils.get(
            self.bot.guilds,
            name=ctx.guild.name
        )
        channel = discord.utils.get(
            guild.text_channels,
            id=config.PARTNERS_CHANNEL_ID
        )
        msg = await channel.send(embed=embed)

        logger.info(
            "Partnership Requirements Embed Sent (MSG ID: {})".format(
                msg.id
            )
        )

        embed = discord.Embed(
            title="SUCCESS",
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Partnership Requirements Sent",
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
        await ctx.channel.send(embed=embed)

    @partner.command(aliases=["refresh", "ereq"])
    @commands.has_guild_permissions(administrator=True)
    async def edit_requirements(self, ctx):
        with open(db_file_path, "rb") as f:
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
            url=config.BOT_URL,
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
        await ctx.channel.send(embed=embed)

    # For now going to lock to admins only
    # After/together with this I should create an inviteinfo command (alias = ii)
    @partner.command()
    @commands.has_guild_permissions(administrator=True)
    async def add(self, ctx, invite: discord.Invite, rep: discord.Member, colour: str = None, banner: str = None):  # Remember that colour codes need to be 0x...
        # Handle NoneType attributes
        if banner is None:
            banner = discord.Embed.Empty
        if colour is None:
            colour = discord.Embed.Empty  # Or discord.Colour.dark_theme() which would blend in with dark mode
        else:  # Convert string to valid integer type
            colour = int(colour, 16)


        # Will resolve guild name, server icon, etc. from the invite itself
        # Handle various errors appropriately in own local err handler

        # Args using invite method: self, ctx, invite, description (or type this in an interactive menu later?), banner = None (which can be different from server banner), colour: str = discord.Embed.empty (when asking in interactive menu, either say default or type the hex code), ???

        # Embed description will be for the description blurb I was provided with
        # And on second thought, desc as a param isn't feasible considering that descriptions will be more than just sentences.

        # Banner param should be provided as a URL (ideally a cdn.discordapp.com one)

        # Embed fields: Representative, Invite
        # Embed thumbnail will be the guild icon
        # Embed image will be the guild banner (that I am provided with)

        # Embed footer: Northbridge Cafe Partnership Program, timestamp=datetime.utcnow()

        # Retrieve guild that the invite points to
        # invite_guild = invite.guild

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
                url=config.BOT_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.set_footer(
                text="Offending Invite: {}".format(invite.url)
            )
            await ctx.message.delete()  # Delete command invokation
            await ctx.channel.send(embed=embed)
            return

        # Retrieve other information about the guild
        # guild_name = guild.name
        # guild_icon = guild.icon_url

        # Retrieve partnership representative member
        # rep_member = discord.utils.get(ctx.guild.members, id=rep_id)

        # utils.get() will return None if could not find a member with that ID
        # if rep_member is None:
        #     embed = discord.Embed(
        #         title="ERROR",
        #         description="I could not find a member with a matching uID, "
        #                     "please try again.",
        #         colour=config.BOT_ERR_COLOUR,
        #         timestamp=datetime.utcnow()
        #     )
        #     embed.set_author(
        #         name=config.BOT_AUTHOR_NAME,
        #         url=config.BOT_URL,
        #         icon_url=self.bot.user.avatar_url
        #     )
        #     embed.set_footer(
        #         text="Offending uID: {}".format(rep_id)
        #     )
        #     await ctx.message.delete()  # Delete command invokation
        #     await ctx.channel.send(embed=embed)
        #     return

        # In theory discord.Member type should already attempt to use MemberConverter() to get the proper type

        embed = discord.Embed(
            title="PARTNERSHIP MENU",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Server Description",
            value="Please enter the accompanying server description/ad for {}.".format(invite.guild.name),
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

        def check(m):
            return m.author == ctx.author

        # Get partner server description
        try:
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
                url=config.BOT_URL,
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
            return

        # TODO: Could provide option to link related website in the embed's title
        # Construct embed object
        embed = discord.Embed(
            title="{}".format(invite.guild.name),
            description="{}".format(provided_desc.content),
            colour=colour,
            timestamp=datetime.utcnow()
        )
        embed.add_field(
            name="{} Representative".format("\U0001f465"),
            # value="{} {}".format("\U0001f465", rep.mention)
            value="{}".format(rep.mention)
        )
        embed.add_field(
            name="{} Invite".format("\U0001f517"),
            # value="{} **{}**".format("\U0001f517", invite.url)  # TODO: Experiment with the spacing
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

        await provided_desc.delete()  # Delete author message containing server description
        await ctx.message.delete()  # Delete command invokation

        # Get object of the channel we want to send to
        guild = discord.utils.get(
            self.bot.guilds,
            name=ctx.guild.name
        )
        channel = discord.utils.get(
            guild.text_channels,
            id=config.PARTNERS_CHANNEL_ID
        )
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
            url=config.BOT_URL,
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
    @commands.has_guild_permissions(administrator=True)
    async def edit(self, ctx, message: int, invite: discord.Invite, rep: discord.Member, colour: str = None, banner: str = None):
        # Handle NoneType attributes
        if banner is None:
            banner = discord.Embed.Empty
        if colour is None:
            colour = discord.Embed.Empty  # Or discord.Colour.dark_theme() which would blend in with dark mode
        else:  # Convert string to valid integer type
            colour = int(colour, 16)

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
                url=config.BOT_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.set_footer(
                text="Offending Invite: {}".format(invite.url)
            )
            await ctx.message.delete()  # Delete command invokation
            await ctx.channel.send(embed=embed)
            return

        embed = discord.Embed(
            title="PARTNERSHIP MENU",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Server Description",
            value="Please enter the accompanying server description/ad for {}.".format(invite.guild.name),
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

        def check(m):
            return m.author == ctx.author

        # Get partner server description
        try:
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
                url=config.BOT_URL,
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
            return

        # TODO: Could provide option to link related website in the embed's title
        # Construct embed object
        new_embed = discord.Embed(
            title="{}".format(invite.guild.name),
            description="{}".format(provided_desc.content),
            colour=colour,
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

        await provided_desc.delete()  # Delete author message containing server description
        await ctx.message.delete()  # Delete command invokation

        # Get object of the channel we want to send to
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
            url=config.BOT_URL,
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
