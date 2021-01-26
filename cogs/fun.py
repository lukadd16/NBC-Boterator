# Description: Cog that houses fun-and-games related commands

# TODO: Most commands here are disabled until they meet my standards
#       Try to find cool, amusing commands from internet, come up with own
#       ideas or even combine own ideas with online code

import app_logger
import discord
import os
import pathlib
import random

from discord.ext import commands

logger = app_logger.get_logger(__name__)

abrams_folder_path = os.path.join(
    pathlib.Path().absolute(), "data\\images\\abrams"
)


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        for h in logger.handlers:
            logger.removeHandler(h)

    @commands.command()
    async def abrams(self, ctx):
        logger.info(
            "Easter Egg Discovered By %s#%s",
            ctx.author.name,
            ctx.author.discriminator
        )

        random_img_name = random.choice([
            x for x in os.listdir(abrams_folder_path)
            if os.path.isfile(os.path.join(abrams_folder_path, x))
        ])
        logger.debug(
            "Selected Image (%s)", random_img_name
        )

        await ctx.send(
            file=discord.File(
                os.path.join(
                    abrams_folder_path, random_img_name
                ), "EasterEgg.jpg"
            )
        )

    # Better dice roll example from online docs
    # TODO: Add proper local error handler for missing dice arg or
    #       incorrectly inputted dice arg
    @commands.command(enabled=False)
    async def roll(self, ctx, dice: str):
        try:
            rolls, limit = map(int, dice.split('d'))

        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        if rolls > 100 or limit > 100:
            await ctx.send(
                "What you are asking is beyond my current computational "
                "abilities (in other words, going any higher will likely "
                "cause me to crash)"
            )

        else:
            result = ', '.join(
                str(random.randint(1, limit)) for r in range(rolls)
            )
            await ctx.send(result)

    # Chooses randomly between multiple provided items
    @commands.command(enabled=False)
    async def choose(self, ctx, *choices: str):
        message = await ctx.send("I prefer...")

        botchoice = random.choice(choices)

        await message.edit(content=f"I prefer {botchoice}")

    # Repeats user message multiple times
    # TODO: Add escape mentions util for this command + add a long cooldown
    #       to prevent abuse (not sure where I want to go with this CMD tbh)
    @commands.command(enabled=False)
    async def repeater(self, ctx, times: int, *, content):
        if times > 50:
            await ctx.send(
                "What you are asking will disturb others, "
                "I cannot let you do that"
            )

        else:
            for i in range(times):
                await ctx.send(content)

    # TODO: Create a command that can search up info about any Iron Man Armour
    @commands.command(enabled=False)
    async def ironman(self, ctx):
        pass

    # TODO: Add proper 8ball responses
    @commands.command(enabled=False)
    async def ball(self, ctx):
        await ctx.send(
            random.choice(
                [
                    "You are doomed...",
                    "You will succeed",
                    "PLACEHOLDER"
                ]
            )
        )


def setup(bot):
    bot.add_cog(FunCog(bot))
