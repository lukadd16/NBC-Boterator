# Description: Cog that houses fun & games commands for NBC Boterator

# Commands in this cog are disabled until they are up to my standards
# Try to find cool, fun commands from internet, come up with own ideas or even combine own ideas with online code

import asyncio
import discord
import random

from discord.ext import commands

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leavemarket(self, ctx):
        to_leave = self.bot.get_guild(602672463733850122)
        await to_leave.leave()

        # Confirmation that we have left the toxic server
        await ctx.send(f"Succesfully left {to_leave.name}")

        await ctx.send("\n[BT] I have access to the following guilds (as of bootup):")
        for guild in self.bot.guilds:
            await ctx.send(guild.name)

    # Better dice roll example from online docs
    @commands.command(enabled=False)
    async def roll(self, ctx, dice: str): # Add proper local error handler for missing dice arg or incorrectly inputted dice arg
        try:
            rolls, limit = map(int, dice.split('d'))

        except Exception:
            await ctx.send('Format has to be in NdN!')
            return
        
        if rolls > 100 or limit > 100:
            await ctx.send("What you are asking is beyond my current computational abilities (i.e. going any higher will most likely cause me to crash)")

        else:
            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await ctx.send(result)

    # Chooses randomly between multiple things
    @commands.command(enabled=False)
    async def choose(self, ctx, *choices: str):
        message = await ctx.send("I prefer...")

        botchoice = random.choice(choices)

        await message.edit(content=f"I prefer {botchoice}")

    # Repeats user message multiple times
    # DISABLED COMMAND, BUT WILL KEEP IN FILE FOR FUTURE REFERENCE

    @commands.command(enabled=False) # Use escape mentions util for this command and add a long cooldown to prevent abuse (not sure where I want to go with this CMD)
    async def repeater(self, ctx, times: int, *, content):
        if times > 50:
            await ctx.send("What you are asking will disturb others, I cannot let you do that")

        else:
            for i in range(times):
                await ctx.send(content)

    @commands.command(enabled=False) # Create a command that can search up info about any Iron Man Armour (from MCU)
    async def ironman(self, ctx):
        pass

    @commands.command(enabled=False)
    async def ball(self, ctx):
     await ctx.send(random.choice(["You are doomed...", "You will succeed", "test", "XD", "why"]))

def setup(bot):
    bot.add_cog(FunCog(bot))