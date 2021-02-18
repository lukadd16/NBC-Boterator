# Description: Cog that houses server moderator-only commands

import app_logger
import asyncio
import config
import discord

from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

logger = app_logger.get_logger(__name__)


# Look into converters further, could be pretty useful for other things.
# TODO: Test to see if this ever actually gets called
class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = f"Actioned by {ctx.author} (ID: {ctx.author.id}): {argument}"

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(
                f"Reason is too long ({len(argument)}/{reason_max})"
            )
        return ret


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        for h in logger.handlers:
            logger.removeHandler(h)

    # TODO: Add a cooldown reset if one of many error messages are shown
    # TODO: Remove "Purge Confirm" & "Purge Complete" messages;
    #       move that field's value to description
    @commands.command(aliases=["clear"])
    @commands.cooldown(2, 12, type=BucketType.user)
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, purge_amount: int):
        # reason = f'Purge issued by user {ctx.author} (ID: {ctx.author.id})'

        if purge_amount == 0:
            logger.debug(
                "Zero Message Deletion Attempted"
            )

            embed = discord.Embed(
                title='ERROR',
                description='You cannot delete 0 messages, nice try.',
                colour=config.BOT_ERR_COLOUR
            )
            embed.set_author(
                name=config.BOT_AUTHOR_NAME,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.set_footer(
                text=config.BOT_FOOTER
            )
            zeroerror = await ctx.channel.send(embed=embed)  # TODO: Convert to delete_after

            await ctx.message.delete()
            await asyncio.sleep(5)  # Intentional delay
            await zeroerror.delete()

            # Error has been handled, exit command execution
            return

        elif purge_amount < 0:
            logger.debug(
                "Negative Message Deletion Attempted"
            )

            embed = discord.Embed(
                title='ERROR',
                description='You cannot delete a negative number of messages, '
                            'nice try.',
                colour=config.BOT_ERR_COLOUR
            )
            embed.set_author(
                name=config.BOT_AUTHOR_NAME,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.set_footer(
                text=config.BOT_FOOTER
            )
            negative_error = await ctx.channel.send(embed=embed)

            await ctx.message.delete()
            await asyncio.sleep(5)
            await negative_error.delete()
            return

        elif purge_amount >= 100:
            logger.info(
                "High Message Purge Attempted By %s#%s (%s)",
                ctx.author.name,
                ctx.author.discriminator,
                ctx.author.id
            )

            embed = discord.Embed(
                title='ERROR',
                description='For security reasons you cannot delete more than '
                            '100 messages at a time, please try again.',
                colour=config.BOT_ERR_COLOUR
            )
            embed.set_author(
                name=config.BOT_AUTHOR_NAME,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.set_footer(
                text=f'Actioned by {ctx.author.name}#'
                     f'{ctx.author.discriminator}',
                icon_url=(ctx.author.avatar_url)
            )
            limit_error = await ctx.channel.send(embed=embed)

            await ctx.message.delete()
            await asyncio.sleep(10)
            await limit_error.delete()
            return

        else:
            embed = discord.Embed(
                title='WARNING',
                colour=config.BOT_ERR_COLOUR
            )
            embed.set_author(
                name=config.BOT_AUTHOR_NAME,
                url=config.WEBSITE_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.add_field(
                name='Purge Confirmation',
                value='Please confirm (yes/no) that you want to clear '
                      f'``{purge_amount}`` message(s)',
                inline=False
            )
            embed.set_footer(
                text=f'Actioned by {ctx.author.name}#'
                     f'{ctx.author.discriminator}',
                icon_url=(ctx.author.avatar_url)
            )
            confirm = await ctx.channel.send(embed=embed)

        def check(m):
            return m.content == "yes" or "no" and m.author == ctx.author

        while True:
            try:
                user_response = await self.bot.wait_for(
                    'message',
                    timeout=20.0,
                    check=check
                )

                if user_response.content.lower() == "yes" and \
                        user_response.author == ctx.author:

                    logger.debug(
                        "Author Confirmation Received"
                    )

                    embed = discord.Embed(
                        title='WARNING',
                        colour=config.BOT_ERR_COLOUR
                    )
                    embed.set_author(
                        name=config.BOT_AUTHOR_NAME,
                        url=config.WEBSITE_URL,
                        icon_url=self.bot.user.avatar_url
                    )
                    embed.add_field(
                        name='Purge In Progress',
                        value=f'Clearing ``{purge_amount}`` message(s)...',
                        inline=False
                    )
                    embed.set_footer(
                        text=f'Actioned by {ctx.author.name}#'
                             f'{ctx.author.discriminator}',
                        icon_url=(ctx.author.avatar_url)
                    )
                    in_progress = await ctx.channel.send(embed=embed)

                    await confirm.delete()
                    await user_response.delete()
                    await ctx.message.delete()

                    # Delete number of messages that user inputted;
                    # Ensuring that only messages prior to the invoked command
                    # are deleted

                    # TODO: Figure out way to only delete messages from last
                    #       14 days, since anything after 14 needs to be loaded
                    #       into cache - a very resource intensive task)

                    logger.debug("Commencing Purge")

                    # Is bulk=True the default?
                    deleted = await ctx.channel.purge(
                        limit=purge_amount,
                        before=ctx.message
                    )

                    logger.info("Purge Complete")

                    complete = discord.Embed(
                        title='SUCCESS',
                        colour=config.BOT_SUCCESS_COLOUR
                    )
                    complete.set_author(
                        name=config.BOT_AUTHOR_NAME,
                        url=config.WEBSITE_URL,
                        icon_url=self.bot.user.avatar_url
                    )
                    complete.add_field(
                        name='Purge Complete',
                        value=f'Successfully purged ``{len(deleted)}`` '
                              'message(s)',
                        inline=False
                    )
                    complete.set_footer(
                        text=f'Actioned by {ctx.author.name}#'
                             f'{ctx.author.discriminator}',
                        icon_url=(ctx.author.avatar_url)
                    )
                    await in_progress.edit(embed=complete)

                    await asyncio.sleep(5)
                    await in_progress.delete()
                    break

                elif user_response.content.lower() == "no" and \
                        user_response.author == ctx.author:

                    logger.debug("Author cancelled action")

                    embed = discord.Embed(
                        title='WARNING',
                        colour=config.BOT_ERR_COLOUR
                    )
                    embed.set_author(
                        name=config.BOT_AUTHOR_NAME,
                        url=config.WEBSITE_URL,
                        icon_url=self.bot.user.avatar_url
                    )
                    embed.add_field(
                        name='Purge Cancelled',
                        value='This action has been cancelled',
                        inline=False
                    )
                    embed.set_footer(
                        text=f'Actioned by {ctx.author.name}#'
                             f'{ctx.author.discriminator}',
                        icon_url=(ctx.author.avatar_url)
                    )
                    await confirm.edit(embed=embed)

                    await ctx.message.delete()
                    await user_response.delete()
                    await asyncio.sleep(5)
                    await confirm.delete()
                    break

            except asyncio.TimeoutError:
                logger.info("Command Timed Out")

                embed = discord.Embed(
                    title='WARNING',
                    colour=config.BOT_ERR_COLOUR
                )
                embed.set_author(
                    name=config.BOT_AUTHOR_NAME,
                    url=config.WEBSITE_URL,
                    icon_url=self.bot.user.avatar_url
                )
                embed.add_field(
                    name='Purge Cancelled',
                    value='This action timed-out',
                    inline=False
                )
                embed.set_footer(
                    text=f'Actioned by {ctx.author.name}#'
                         f'{ctx.author.discriminator}',
                    icon_url=(ctx.author.avatar_url)
                )
                await confirm.edit(embed=embed)

                await ctx.message.delete()
                await asyncio.sleep(10)
                await confirm.delete()
                break

        return

    # TODO: Add try catch blocks for each of the below commands, try to
    #       account for as many errors as possible, either within the function
    #       itself or a local error handler, with an embed response stating
    #       what the error is (404, bad arg, etc.)
    @commands.command(aliases=["boot"], enabled=False)
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, members: str = None, *,
                   reason: ActionReason = None):
        if members is None:
            raise commands.MissingRequiredArgument(members)  # TODO: Test this

        if reason is None:
            reason = 'No reason provided - Kick issued by Moderator '
            f'{ctx.author} (ID: {ctx.author.id})'

        for member in members:
            member_obj = await self.bot.fetch_user(member)

        embed = discord.Embed(
            title='SUCCESS',
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_thumbnail(
            url=f'{member.avatar_url}'
        )
        embed.add_field(
            name='Moderation Action Complete',
            value=f'Sucessfully kicked `{member.name}#{member.discriminator}` '
                  f'| ID: `{member.id}`'
        )
        embed.set_footer(
            text=f'Actioned by {ctx.author.name}#{ctx.author.discriminator}',
            icon_url=(ctx.author.avatar_url)
        )

        await ctx.message.delete()
        await ctx.guild.kick(member, reason=reason)
        await ctx.channel.send(embed=embed)

    @kick.error
    async def kick_handler(self, ctx, error, members):
        embed = discord.Embed(
            title='ERROR',
            colour=config.BOT_ERR_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name='Moderation Action Failed',
            value='The following users could not be kicked:'
            #       f'{for member in members}'
            #       f'`{member.name}#{member.discriminator}` '
            #       f'| ID: `{member.id}`'
        )
        embed.set_footer(
            text=f'Actioned by {ctx.author.name}#{ctx.author.discriminator}',
            icon_url=(ctx.author.avatar_url)
        )

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == "member":
                await ctx.send("You forgot to give me input to repeat!")

    # TODO: Clear everything out and start from scratch, logically would want
    #       be able to ping user we want to ban but also able to take ID as arg

    # Create base kick and ban cmds that take a single proper discord.Member (or discord.User?) object
    # Unban will always need to take an ID so multi logic would still apply to a single object
    # Then create subcmds for kick and ban called "multi" that ONLY take IDs as string, no discord.Member/User objects.
    @commands.command(aliases=["bean"], enabled=False)
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: int, reason: ActionReason = None,
                  delete_days: int = None):
        if user is None:
            return
        else:
            # Taking input as integer because global error handler wasn't
            # handling it the way I wanted to
            user = await self.bot.fetch_user(user)

        if delete_days is None:
            delete_days = 7

        print(delete_days)  # DEBUG

        # TODO: after figure out items below, add multiban logic here
        # - So just take the IDs as string, verify that they are indeed users
        #   (or can let error handler just tell us that the ID is invalid)
        #   and put IDs in a list
        # - Loop through list and attempt to ban each ID
        # - While looping append successful and failed bans to a list
        #   (which we will display at the end)

        # Doing the above might be difficult if letting error handler take over
        # If anything is wrong with a given ID then could just report back "Failed to ban user.mention"

        # Either append fails to same list, or have two lists for success and fails, then if failslist.length > 0
        # Respond with generic error message saying "Please make sure you entered a valid 18-digit ID and that the user you are trying to ban exists"

        # Use same looping logic for both kick multi and unban multi sub-commands
        # (only difference should be the response text + actual action taken on user(s))

        # TODO: ~~Need to add logic to check if user being moderated is already~~
        # banned, etc.; For unbans a 404 Error popped up saying "Unknown Ban",
        # figure out how this translates to an error and if this same error
        # applies to banning when a member is already banned;
        # Clean up the if statements if possible

        # TODO: Use Optional function from typing package to make delete_days
        #       an optional arg, rather than putting it at end of arg list
        # if deletedays is None:
        #     deletedays = 0

        if reason is None:
            reason = 'No reason provided - Ban issued by Moderator '
            f'{ctx.author} (ID: {ctx.author.id})'

        embed = discord.Embed(
            title='SUCCESS',
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_thumbnail(
            url=f'{user.avatar_url}'
        )
        embed.add_field(
            name='Moderation Action Complete',
            value=f'Sucessfully banned `{user.name}#{user.discriminator}` '
                  f'| ID: `{user.id}`'
        )
        embed.set_footer(
            text=f'Actioned by {ctx.author.name}#{ctx.author.discriminator}',
            icon_url=(ctx.author.avatar_url)
        )

        await ctx.message.delete()
        await ctx.guild.ban(
            user,
            reason=reason,
            delete_message_days=delete_days  # Need to test days deleted;
                                             # Maximum allowed is 7
        )
        await ctx.channel.send(embed=embed)

    # TODO: Scrap all of this and start from the beginning,
    #       only logically makes sense to take userID as input because the
    #       user is no longer in the server
    @commands.command(enabled=False)
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user: str,
                    reason: ActionReason = None):
        if user is None:
            return
        else:
            user = await self.bot.fetch_user(user)

        if reason is None:
            reason = 'No reason provided - Unban issued by Moderator '
            f'{ctx.author} (ID: {ctx.author.id})'

        elif len(reason) > 512:
            # TODO: Create error embed here and then copy this over to other
            #       mod commands (??)
            return

        try:
            await ctx.guild.unban(user, reason=reason)
        # TODO: Figure out exact exception(s)
        except:
            print("User already unbanned!")
            # TODO: Add proper embed error here
            return

        embed = discord.Embed(
            title='SUCCESS',
            colour=config.BOT_SUCCESS_COLOUR
        )
        embed.set_author(
            name=config.BOT_AUTHOR_NAME,
            url=config.WEBSITE_URL,
            icon_url=self.bot.user.avatar_url
        )
        embed.set_thumbnail(
            url=f'{user.avatar_url}'
        )
        embed.add_field(
            name='Moderation Action Complete',
            value=f'Sucessfully removed the ban for `{user.name}#'
                  f'{user.discriminator}` | ID: `{user.id}`'
        )
        embed.set_footer(
            text=f'Actioned by {ctx.author.name}#{ctx.author.discriminator}',
            icon_url=(ctx.author.avatar_url)
        )

        await ctx.message.delete()
        await ctx.channel.send(embed=embed)

    # TODO: Test the above commands and then code a soft_ban command
    #       (bans, deletes all messages from past 7 days and then unbans;
    #       should only need to append the reason once to the first ban action
    #       but state that it was a softban)

    # For multiban/kick commands, will most likely need to take IDs as string
    # (separated by spaces or commas?) and then attempt to convert them after
    # the fact; There should be a built in converter, just split the string,
    # store in a list, check that all IDs are valid (keep a counter of how
    # many failed)

    # Thinking of handling invalid IDs during conversion
    # (i.e. increasing fail counter + removing those IDs from the list); Not
    # sure exactly how the converter works (is an ID of someone who is not in
    # the server still "valid"? Will need to explore possible errors that the
    # converter can throw as well); Failed kicks will also add to the same fail
    # counter (only would occur if the ID of someone who is not in the server
    # is still valid according to the converter or because 404 error, ??)

    # Store in another list(?) then loop the kicking/banning action while
    # keeping count of how many kicks were successful and how many failed;
    # Will need a local error handler so that if ID is invalid the program
    # doesn't exit the loop and instead handles it gracefully in the way
    # I want it to

    # Output which ones went through in an elegant fashion (with name +
    # discrim + ID so that the mod knows which one might've not gone through)
    # Then tell them how many failed (due to either invalid ID,
    # already banned/kicked or not in the server)

    # Don't take a reason argument for these ones, just assign a default one
    # (with maybe the for loop "i" var to show that this was #1/7).


def setup(bot):
    bot.add_cog(ModCog(bot))
