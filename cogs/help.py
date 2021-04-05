# Description: Cog that contains the re-designed help command for NBC Boterator

import app_logger
import config
import discord
import os

from discord.ext import commands

logger = app_logger.get_logger(__name__)

# File path for owner-only help command text file
txt_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")
txt_dir = os.path.join(txt_dir, "txt")
file_name = "owner-help.txt"
txt_file_path = os.path.join(txt_dir, file_name)
logger.info("TXT File Path: {}".format(txt_file_path))


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        for h in logger.handlers:
            logger.removeHandler(h)

    # TODO: NBC-specific CMD Ideas
    # - A "list staff team" command or just a "members in @role"
    # - Make moderation commands more useful and optimized, if I ever make
    #   something as sophisticated as localbot then we would switch over.
    # - At some point move custom commands over to this bot
    # - Auto response? Like in PCMR

    # TODO: Where needed...
    #       Add a "Permissions" tag that mentions requirements
    #       Add "Cooldown" tag that describes ratelimits (1 per 30, etc.)

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                description=f"Run `{config.BOT_PREFIX}help "
                            "<commandname>` to view detailed help on a "
                            "specific command"
                            "\n`[] Required Args`"
                            "\n`<> Optional Args`"
                            "\n\nClick the header of any of my commands to "
                            "visit the server's website",
                colour=config.BOT_COLOUR
            )
            embed.set_author(
                name="NBC Boterator Command List",
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.add_field(
                name="Fun Commands [Disabled]",
                value="`choose`, `roll`",
                inline=False
            )
            embed.add_field(
                name="Utility Commands [8]",
                value="`about`, `avatar`, `changelog`, `joinpos`, `ping`, "
                      "`pinned`, `suggest`, `whois`",
                inline=False
            )
            embed.add_field(
                name="Moderation Commands [1]",
                value="`purge`",
                inline=False
            )
            embed.set_footer(text=config.BOT_FOOTER)
            await ctx.send(embed=embed)

    @help.command(enabled=False)
    async def choose(self, ctx):
        pass

    @help.command(enabled=False)
    async def roll(self, ctx):
        pass

    @help.command()
    async def about(self, ctx):
        cmd = self.bot.get_command("about")
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            title=f"{config.BOT_PREFIX}{cmd.name}",
            description="Retrieves relevant information about the bot "
                        "(uptime, library, etc.)"
                        "\n\n**Type:** Utility"
                        f"\n**Usage:** `{config.BOT_PREFIX}about`"
                        f"\n**Aliases:** {cmd_aliases}",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{config.BOT_HELP_ANAME}",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command()
    async def avatar(self, ctx):
        cmd = self.bot.get_command("avatar")
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            title=f"{config.BOT_PREFIX}{cmd.name}",
            description=f"Outputs an enlarged version of a specified user's "
                        "profile picture"
                        "\n\n**Type:** Utility"
                        f"\n**Usage:** `{config.BOT_PREFIX}avatar "
                        f"<user>`"
                        f"\n**Aliases:** {cmd_aliases}"
                        f"\n{config.BOT_HELP_USER_ARG}",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{config.BOT_HELP_ANAME}",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command()
    async def changelog(self, ctx):
        cmd = self.bot.get_command("changelog")
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            title=f"{config.BOT_PREFIX}{cmd.name}",
            description=f"Learn what's new with this version of the bot"
                        "\n\n**Type:** Utility"
                        f"\n**Usage:** `{config.BOT_PREFIX}"
                        f"{cmd.name}`"
                        f"\n**Aliases:** {cmd_aliases}",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{config.BOT_HELP_ANAME}",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command()
    async def joinpos(self, ctx):
        cmd = self.bot.get_command("joinpos")
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            title=f"{config.BOT_PREFIX}{cmd.name}",
            description=f"States the position that a specified user joined "
                        "the server. E.g. Joe is member #50 out of 550"
                        "\n\n**Type:** Utility"
                        f"\n**Usage:** `{config.BOT_PREFIX}"
                        f"{cmd.name} <user>`"
                        f"\n**Aliases:** {cmd_aliases}"
                        f"\n{config.BOT_HELP_USER_ARG}",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{config.BOT_HELP_ANAME}",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command()
    async def ping(self, ctx):
        cmd = self.bot.get_command("ping")

        embed = discord.Embed(
            title=f"{config.BOT_PREFIX}{cmd.name}",
            description=f"Tests my connection to Discord"
                        "\n\n**Type:** Utility"
                        f"\n**Usage:** `{config.BOT_PREFIX}"
                        f"{cmd.name}`",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{config.BOT_HELP_ANAME}",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command()
    async def pinned(self, ctx):
        cmd = self.bot.get_command("pinned")
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            title=f"{config.BOT_PREFIX}{cmd.name}",
            description=f"Retrieves information about a channel's pinned "
                        "messages"
                        "\n\n**Type:** Utility"
                        f"\n**Usage:** `{config.BOT_PREFIX}"
                        f"{cmd.name} <channel>`"
                        f"\n**Aliases:** {cmd_aliases}",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{config.BOT_HELP_ANAME}",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command(enabled=False)
    async def serverinfo(self, ctx):
        cmd = self.bot.get_command("serverinfo")
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            title=f"{config.BOT_PREFIX}{cmd.name}",
            description=f"Retrieves information about this server"
                        "\n\n**Type:** Utility"
                        f"\n**Usage:** `{config.BOT_PREFIX}"
                        f"{cmd.name}`"
                        f"\n**Aliases:** {cmd_aliases}",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{config.BOT_HELP_ANAME}",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command()
    async def suggest(self, ctx):
        cmd = self.bot.get_command("suggest")

        embed = discord.Embed(
            title=f"{config.BOT_PREFIX}{cmd.name}",
            description=f"Allows you to report a bug, suggest ideas for new "
                        "commands or suggest improvements for existing ones. "
                        "Your response will be sent in "
                        f"<#{config.SUGGEST_CHANNEL_ID}>."
                        "\n\n**Type:** Utility"
                        f"\n**Usage:** `{config.BOT_PREFIX}"
                        f"{cmd.name} <suggestion-text-here>`",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{config.BOT_HELP_ANAME}",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command()
    async def whois(self, ctx):
        cmd = self.bot.get_command("whois")
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            title=f"{config.BOT_PREFIX}{cmd.name}",
            description=f"Retrieves relevant information about a specified "
                        "user in the server"
                        "\n\n**Type:** Utility"
                        f"\n**Usage:** `{config.BOT_PREFIX}"
                        f"{cmd.name} <user>`"
                        f"\n**Aliases:** {cmd_aliases}"
                        f"\n{config.BOT_HELP_USER_ARG}",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{config.BOT_HELP_ANAME}",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command(enabled=False)
    async def ban(self, ctx):
        cmd = self.bot.get_command("ban")
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            title=f"{config.BOT_PREFIX}{cmd.name}",
            description=f"Bans a specified user from the server."
                        "\n\n**Type:** Moderation"
                        f"\n**Usage:** `{config.BOT_PREFIX}"
                        f"{cmd.name} [userID or @mention] <reason> <days>`"
                        f"\n**Aliases:** {cmd_aliases}"
                        f"\n{config.BOT_HELP_REASON_ARG}"
                        f"{config.BOT_HELP_BAN_ARG}",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{config.BOT_HELP_ANAME}",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command(enabled=False)
    async def kick(self, ctx):
        cmd = self.bot.get_command("kick")
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            title=f"{config.BOT_PREFIX}{cmd.name}",
            description=f"Kicks a specified user from the server."
                        "\n\n**Type:** Moderation"
                        f"\n**Usage:** `{config.BOT_PREFIX}"
                        f"{cmd.name} <userID or @mention> <reason>`"
                        f"\n**Aliases:** {cmd_aliases}"
                        f"\n{config.BOT_HELP_REASON_ARG}",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{config.BOT_HELP_ANAME}",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command()
    async def purge(self, ctx):
        cmd = self.bot.get_command("purge")
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            title=f"{config.BOT_PREFIX}{cmd.name}",
            description=f"Deletes a specified number of messages from the "
                        "current channel."
                        "\n\n**Type:** Moderation"
                        "\n**Permissions:** Manage Messages"
                        f"\n**Usage:** `{config.BOT_PREFIX}"
                        f"{cmd.name} <#-of-messages-to-delete>`"
                        f"\n**Aliases:** {cmd_aliases}",
            colour=config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{config.BOT_HELP_ANAME}",
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command()
    @commands.is_owner()
    async def owner(self, ctx):
        with open(txt_file_path, "r", encoding="utf-8") as f:
            msg = "".join(f.readlines())
            logger.debug("TXT File Data Loaded")

        await ctx.send(msg)

def setup(bot):
    bot.add_cog(HelpCog(bot))
