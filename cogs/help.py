# Description: Cog that contains the re-designed help command for NBC Boterator

import discord
from discord.ext import commands

class NewHelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Change bullet points to code blocks with > arrows?

    # Add prefix+commandname as a title, change author to botname Help Menu (much easier, all sub commands will have this as author and can be changed easily via config.py)

    # NBC Specific Cmd Ideas:
    # - website (sends a link to our website + other socials?)
    # - (not specific to NBC but) a staff team command or just a "members in @role"
    # - Make moderation commands more useful and optimized, if I can ever make something as sophisticated as localbot then we would switch over.
    # - Add simple VC mute and deafen commands
    # - Add simple nickname change command
    # - At some point move custom commands over to this bot
    # - Auto response? Like in PCMR

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                description=f"Run `{self.bot.config.BOT_PREFIX}help "
                            "<commandname>` to view detailed help on a "
                            "specific command"
                            "\n`[] Required Args`"
                            "\n`<> Optional Args`"
                            "\n\nClick the header of any of my commands to "
                            "visit the server's website",
                colour=self.bot.config.BOT_COLOUR
            )
            embed.set_author(
                name="NBC Boterator Command List",
                url=self.bot.config.BOT_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.add_field(
                name="Fun Commands [Disabled]",
                value="`choose`, `roll`",
                inline=False
            )
            embed.add_field(
                name="Utility Commands [6]",
                value="`about`, `avatar`, `changelog`, `ping`, `suggest`, `whois`",
                inline=False
            )
            embed.add_field(
                name="Moderation Commands [5]",
                value="`ban`, `kick`, `purge`, `softban`, `unban`",
                inline=False
            )
            embed.set_footer(text=self.bot.config.BOT_FOOTER)
            await ctx.send(embed=embed)

    @help.command(enabled=False)
    async def choose(self, ctx):
        pass

    @help.command(enabled=False)
    async def roll(self, ctx):
        pass

    @help.command(aliases=["botinfo", "info"])
    async def about(self, ctx):
        cmd = self.bot.get_command('about')
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            title=f"{self.bot.config.BOT_PREFIX}{cmd.name}",
            description="Retrieves relevant information about me "
                        "(uptime, library, etc.)\n\n**Type:** Utility"
                        f"\n**Usage:** `{self.bot.config.BOT_PREFIX}about`"
                        f"\n**Aliases:** {cmd_aliases}",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{self.bot.config.BOT_HELP_ANAME}",
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command(aliases=["av"])
    async def avatar(self, ctx):
        cmd = self.bot.get_command('avatar')
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            title=f"{self.bot.config.BOT_PREFIX}{cmd.name}",
            description=f"Outputs an enlarged version of a specified user's "
                        "profile picture\n\n**Type:** Utility"
                        f"\n**Usage:** `{self.bot.config.BOT_PREFIX}avatar "
                        f"<user>`\n**Aliases:** {cmd_aliases}"
                        f"\n{self.bot.config.BOT_HELP_USER_ARG}",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{self.bot.config.BOT_HELP_ANAME}",
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command(aliases=["version", "whatsnew"])
    async def changelog(self, ctx):
        cmd = self.bot.get_command('changelog')
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            description=f"Learn what's new with this version of the bot\n\n"
                        "**Type:** Utility\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}{cmd.name}`"
                        f"\n**Aliases:** {cmd_aliases}",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{self.bot.config.BOT_HELP_ANAME}",
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command()
    async def ping(self, ctx):
        cmd = self.bot.get_command('ping')

        embed = discord.Embed(
            description=f"Tests my connection to Discord\n\n"
                        "**Type:** Utility\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}{cmd.name}`",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{self.bot.config.BOT_HELP_ANAME}",
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command(aliases=["sinfo"], enabled=False)
    async def serverinfo(self, ctx):
        cmd = self.bot.get_command('serverinfo')
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            description=f"Retrieves information about this server\n\n"
                        "**Type:** Utility\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}{cmd.name}`"
                        f"\n**Aliases:** {cmd_aliases}",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{self.bot.config.BOT_HELP_ANAME}",
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command()
    async def suggest(self, ctx):
        cmd = self.bot.get_command('suggest')

        embed = discord.Embed(
            description=f"Allows you to report a bug or suggest ideas for new commands/improvements to existing ones. Your response is sent directly to the developer.\n\n"
                        "**Type:** Utility\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}{cmd.name} <yoursuggestion>`",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{self.bot.config.BOT_HELP_ANAME}",
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command(aliases=["userinfo", "uinfo"])
    async def whois(self, ctx):
        cmd = self.bot.get_command('whois')
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            description=f"Retrieves relevant information about a specified user in this server\n\n"
                        "**Type:** Utility\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}{cmd.name} <user>`\n"
                        f"**Aliases:** {cmd_aliases}\n"
                        f"{self.bot.config.BOT_HELP_USER_ARG}",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{self.bot.config.BOT_HELP_ANAME}",
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command(enabled=False)
    async def ban(self, ctx):
        cmd = self.bot.get_command('ban')
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            description=f"Bans a specified user from your server.\n\n"
                        "**Type:** Moderation\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}{cmd.name} <userID or mention> <reason> <days>`\n"
                        f"**Aliases:** {cmd_aliases}\n"
                        f"{self.bot.config.BOT_HELP_REASON_ARG}"
                        f"{self.bot.config.BOT_HELP_BAN_ARG}",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{self.bot.config.BOT_HELP_ANAME}",
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @help.command()
    async def kick(self, ctx):
        cmd = self.bot.get_command('kick')
        cmd_aliases = f"`{'`, `'.join(cmd.aliases)}`"

        embed = discord.Embed(
            description=f"Kicks a specified user from your server.\n\n"
                        "**Type:** Moderation\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}{cmd.name} <userID or mention> <reason>`\n"
                        f"**Aliases:** {cmd_aliases}\n"
                        f"{self.bot.config.BOT_HELP_REASON_ARG}",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(
            name=f"{self.bot.config.BOT_HELP_ANAME}",
            url=self.bot.config.BOT_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    # Continue to add moderation help subcommands, include a "usage" thing for perm requirements

def setup(bot):
    bot.add_cog(NewHelpCog(bot))
