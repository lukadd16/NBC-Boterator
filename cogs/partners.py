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
        self.partner_channel = self.bot.get_channel(
            config.PARTNERS_CHANNEL_ID
        )
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
        pass

    # This'll be the command that sends the initial requirements embed, should also add one called edit_requirements (which'll retrieve the embed from ID, create an embed object using data from partners.json which we will assume has been editted)
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

        partner_msg = await self.partner_channel.send(embed=embed)
        await ctx.send("**`SUCCESS`**` (ID: {})".format(  # Copy this + logger format for official.py commands where need the ID of the embeds sent
                partner_msg.id
            )
        )
        logger.info(
            "Partnership Requirements Embed Sent (MSG ID: {})".format(
                partner_msg.id
            )
        )

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

        # Retrieve necessary details about the message we want to edit
        guild = discord.utils.get(
            self.bot.guilds,
            name="Jarvis Bot"
        )
        channel = discord.utils.get(
            guild.text_channels,
            id=config.PARTNERS_CHANNEL_ID
        )
        msg = await channel.fetch_message(
            config.PARTNERS_MSG_ID
        )

        await msg.edit(embed=new_embed)
        await ctx.send("**`SUCCESS`**")
        logger.info(
            "Partnership Requirements Embed Edited (MSG ID: {})".format(
                msg.id
            )
        )

    # For now going to lock to admins only
    @partner.command()
    @commands.has_guild_permissions(administrator=True)
    async def add(self, ctx):
        pass

    @partner.command()
    @commands.has_guild_permissions(administrator=True)
    async def edit(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Partners(bot))
