# Description: Cog that houses server moderator-only commands for NBC Boterator

# Continue testing purge command

# Cooldown section in the docs is my friend
# - Adjust cooldown time and add error handling for CommandOnCooldown

# Temporary fix on new mod commands, try to find way to make error handler handle the missing member arg

import asyncio
import discord

from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

# Look into converters further, could be pretty useful for other things.
class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = f'{ctx.author} (ID: {ctx.author.id}): {argument}'  # Does this actually follow the format of the default reason? (with name of action + moderator uID + reason)

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(
                f'Reason is too long ({len(argument)}/{reason_max})'
            )
        return ret

class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["clear"])
    @commands.cooldown(2, 12, type=BucketType.user)  # Add a reset to cooldown if one of many error messages are shown
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, purge_amount: int):

        # reason = f'Purge issued by user {ctx.author} (ID: {ctx.author.id})'

        if purge_amount == 0:
            # Not sure why I made the error messages like this, ERROR should be in the title
            embed = discord.Embed(
                colour=self.bot.config.BOT_ERR_COLOUR
            )
            embed.set_author(
                name=self.bot.config.BOT_AUTHOR_NAME,
                url=self.bot.config.BOT_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.add_field(
                name='ERROR',
                value='You cannot delete 0 messages, nice try.',
                inline=False
            )
            embed.set_footer(
                text=self.bot.config.BOT_FOOTER
            )
            zeroerror = await ctx.channel.send(embed=embed)

            await ctx.message.delete()
            await asyncio.sleep(5)  # Intentional delay
            # Look into delete_after argument,
            # could replace asyncio.sleep statements in this cog
            await zeroerror.delete()

            # Error has been handled, do not continue with the rest of the command logic
            return

        elif purge_amount < 0:
            embed = discord.Embed(
                colour=self.bot.config.BOT_ERR_COLOUR
            )
            embed.set_author(
                name=self.bot.config.BOT_AUTHOR_NAME,
                url=self.bot.config.BOT_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.add_field(
                name='ERROR',
                value='You cannot delete a negative number of messages, nice try.',
                inline=False
            )
            embed.set_footer(
                text=self.bot.config.BOT_FOOTER
            )
            negativeerror = await ctx.channel.send(embed=embed)

            await ctx.message.delete()
            await asyncio.sleep(5)
            await negativeerror.delete()
            return

        elif purge_amount >= 100:
            embed = discord.Embed(
                colour=self.bot.config.BOT_ERR_COLOUR
            )
            embed.set_author(
                name=self.bot.config.BOT_AUTHOR_NAME,
                url=self.bot.config.BOT_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.add_field(
                name='ERROR',
                value='For security reasons you cannot delete more than 100'
                      'messages at a time, please try again.',
                inline=False
            )
            embed.set_footer(
                text=f'Actioned by {ctx.author.name}#{ctx.author.discriminator}',
                icon_url=(ctx.author.avatar_url)
            )
            limiterror = await ctx.channel.send(embed=embed)

            await ctx.message.delete()
            await asyncio.sleep(10)
            await limiterror.delete()
            return

        else:
            embed = discord.Embed(
                title='WARNING',
                colour=self.bot.config.BOT_ERR_COLOUR
            )
            embed.set_author(
                name=self.bot.config.BOT_AUTHOR_NAME,
                url=self.bot.config.BOT_URL,
                icon_url=self.bot.user.avatar_url
            )
            embed.add_field(
                name='Purge Confirmation',
                value='Please confirm (yes/no) that you want to clear '
                      f'``{purge_amount}`` message(s)',
                inline=False
            )
            embed.set_footer(
                text=f'Actioned by {ctx.author.name}#{ctx.author.discriminator}',
                icon_url=(ctx.author.avatar_url)
            )
            confirm = await ctx.channel.send(embed=embed)

        def check(m):
            return m.content == "yes" or "no" and m.author == ctx.author

        while True:
            try:
                msg = await self.bot.wait_for('message', timeout=20.0, check=check)

                if msg.content.lower() == "yes" and msg.author == ctx.author:
                    embed = discord.Embed(
                        title='WARNING',
                        colour=self.bot.config.BOT_ERR_COLOUR
                    )
                    embed.set_author(
                        name=self.bot.config.BOT_AUTHOR_NAME,
                        url=self.bot.config.BOT_URL,
                        icon_url=self.bot.user.avatar_url
                    )
                    embed.add_field(
                        name='Purge In Progress',
                        value=f'Clearing ``{purge_amount}`` message(s)...',
                        inline=False
                    )
                    embed.set_footer(
                        text=f'Actioned by {ctx.author.name}#{ctx.author.discriminator}',
                        icon_url=(ctx.author.avatar_url)
                    )
                    tmp = await ctx.channel.send(embed=embed)

                    await confirm.delete()
                    await msg.delete()
                    await ctx.message.delete()

                    # Delete the number of messages that the user inputted
                    # Making sure to delete messages prior to the invoked
                    # command

                    # TODO: Figure out a way to only delete messages from the last 14 days
                    # (because anything after that needs to be loaded into cache, which is a very resource intensive task)

                    # Experiment with bulk=True/False, maybe let the user input
                    # if they want bulk delete or not to preserve messages in
                    # logs (bulk delete is faster)
                    deleted = await ctx.channel.purge(limit=purge_amount, before=ctx.message)

                    complete = discord.Embed(title='SUCCESS', colour=self.bot.config.BOT_SUCCESS_COLOUR)
                    complete.set_author(name=self.bot.config.BOT_AUTHOR_NAME, url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
                    complete.add_field(name='Purge Complete', value=f'Successfully purged ``{len(deleted)}`` message(s)', inline=False)
                    complete.set_footer(text=f'Actioned by {ctx.author.name}#{ctx.author.discriminator}', icon_url=(ctx.author.avatar_url))
                    await tmp.edit(embed=complete)

                    await asyncio.sleep(5)
                    await tmp.delete()
                    break

                elif msg.content.lower() == "no" and msg.author == ctx.author:
                    embed = discord.Embed(title='WARNING', colour=self.bot.config.BOT_ERR_COLOUR)
                    embed.set_author(name=self.bot.config.BOT_AUTHOR_NAME, url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
                    embed.add_field(name='Purge Cancelled', value='This action has been cancelled', inline=False)
                    embed.set_footer(text=f'Actioned by {ctx.author.name}#{ctx.author.discriminator}', icon_url=(ctx.author.avatar_url))
                    await confirm.edit(embed=embed)

                    await ctx.message.delete()
                    await msg.delete()
                    await asyncio.sleep(5)
                    await confirm.delete()
                    break

            except asyncio.TimeoutError:
                embed = discord.Embed(title='WARNING', colour=self.bot.config.BOT_ERR_COLOUR)
                embed.set_author(name=self.bot.config.BOT_AUTHOR_NAME, url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
                embed.add_field(name='Purge Cancelled', value='This action timed-out', inline=False)
                embed.set_footer(text=f'Actioned by {ctx.author.name}#{ctx.author.discriminator}', icon_url=(ctx.author.avatar_url))
                await confirm.edit(embed=embed)

                await ctx.message.delete()
                await asyncio.sleep(10)
                await confirm.delete()
                break

        return

    # Add try catch blocks for each of the below commands, try to account for as many errors as possible with an embed response stating what the error is (404, bad)

    @commands.command(aliases=["boot"])
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason: ActionReason = None):
        if member is None:
            return
            # Add custom embed error here because default error handler is being goofy (do the same for ban, softban, and unban)

        if reason is None:
            reason = f'No reason provided - Kick issued by Moderator {ctx.author} (ID: {ctx.author.id})'

        embed = discord.Embed(title='SUCCESS', colour=self.bot.config.BOT_SUCCESS_COLOUR)
        embed.set_author(name=self.bot.config.BOT_AUTHOR_NAME, url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=f'{member.avatar_url}')
        embed.add_field(name='Moderation Action Complete', value=f'Sucessfully kicked `{member.name}#{member.discriminator}` | ID: `{member.id}`')
        embed.set_footer(text=f'Actioned by {ctx.author.name}#{ctx.author.discriminator}', icon_url=(ctx.author.avatar_url))

        await ctx.message.delete()
        await ctx.guild.kick(member, reason=reason)
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["bean"])
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: int, reason: ActionReason = None, delete_days: int = None): # Clear everything out and start from scratch, logically would want to be able to ping the person we want to ban but also be able to take ID as input
        if user is None:
            return
        else:
            user = await self.bot.fetch_user(user)  # Taking input as integer because global error handler wasn't handling it the way I wanted to

        if delete_days is None:
            delete_days = 7

        print(delete_days) # DEBUG

        # TODO: after figure out items below, add multiban logic here
        #           - So just take the IDs as string, verify that they are indeed users (or can let error handler just tell us that the ID is invalid) and put IDs in a list
        #           - Loop through list and attempt to ban each ID
        #           - Compile a list of successful and non-successful bans (which we will display at the end)

        # Need to add logic to check if user being banned/kicked/unbanned is already banned, etc.
        # For unbans a 404 Error popped up saying "Unknown Ban", figure out how this translates to an error and if this same error applies to banning when a member is already banned
        # Clean up the if statements if possible

        # except discord.Forbidden

        #if deletedays is None: # Figure out a way that I can still take reason input without having to put deletedays at the end, or just put deletedays at the end (found it, need to use Optional function from the typing package)
        #    deletedays = 7

        if reason is None:
            reason = f'No reason provided - Ban issued by Moderator {ctx.author} (ID: {ctx.author.id})'

        embed = discord.Embed(title='SUCCESS', colour=self.bot.config.BOT_SUCCESS_COLOUR)
        embed.set_author(name=self.bot.config.BOT_AUTHOR_NAME, url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=f'{user.avatar_url}')
        embed.add_field(name='Moderation Action Complete', value=f'Sucessfully banned `{user.name}#{user.discriminator}` | ID: `{user.id}`')
        embed.set_footer(text=f'Actioned by {ctx.author.name}#{ctx.author.discriminator}', icon_url=(ctx.author.avatar_url))

        await ctx.message.delete()
        await ctx.guild.ban(user, reason=reason, delete_message_days=delete_days) # Need to test days deleted (max is 7)
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: int, reason: ActionReason=None): # Scrap all of this and start from the beginning, only logically make sense to take userID as input because the member won't be in the server
        # Look at how other bots implemented their unban, do they also only take userID input?
        if user is None:
            return
        else:
            user = await self.bot.fetch_user(user) # Works now, stupidly tried to take discord.User input (which would be impossible as that user wouldn't be in the server)

        if reason is None:
            reason = f'No reason provided - Unban issued by Moderator {ctx.author} (ID: {ctx.author.id})'

        elif len(reason) > 512:
            # Create error embed here and then copy this over to other mod commands
            return

        try:
            await ctx.guild.unban(user, reason=reason)
        except:
            print("User already unbanned!")
            # Add proper embed error here
            return

        embed = discord.Embed(title='SUCCESS', colour=self.bot.config.BOT_SUCCESS_COLOUR)
        embed.set_author(name=self.bot.config.BOT_AUTHOR_NAME, url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=f'{user.avatar_url}')
        embed.add_field(name='Moderation Action Complete', value=f'Sucessfully removed the ban for `{user.name}#{user.discriminator}` | ID: `{user.id}`')
        embed.set_footer(text=f'Actioned by {ctx.author.name}#{ctx.author.discriminator}', icon_url=(ctx.author.avatar_url))

        await ctx.message.delete()
        await ctx.channel.send(embed=embed)

    # Test the above commands and then code a soft_ban command (bans, deletes all messages from past 7 days and then unbans; should only need to append the reason once to the first ban action but state that it was a softban)

    # For multiban/kick commands, will most likely need to take IDs as string (separated by spaces or commas?) and then attempt to convert them after the fact
    # There should be a built in converter, just split the string, store in a list, check that all IDs are valid (keep a counter of how many failed)

    # Thinking of handling invalid IDs during conversion (i.e. increasing fail counter + removing those IDs from the list)
    # Not sure exactly how the converter works (is an ID of someone who is not in the server still "valid"? Will need to explore possible errors that the converter can throw as well)
    # Failed kicks will also add to the same fail counter (only would occur if the ID of someone who is not in the server is still valid according to the converter
    # or because 404 error, ??)

    # Store in another list(?) then loop the kicking/banning action while keeping count of how many kicks were successful and how many failed
    # Will need a local error handler so that if ID is invalid the program doesn't exit the loop and instead handles it gracefully in the way I want it to

    # Output which ones went through in an elegant fashion (with name + discrim so that the mod knows which one might've not gone through)
    # Then tell them how many failed (due to either invalid ID, already banned/kicked or not in the server)

    # Don't take a reason argument for these ones, just assign a default one (with maybe the for loop "i" var to show that this was #1/7).

def setup(bot):
    bot.add_cog(ModCog(bot))
