import discord, pymongo, os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

class code(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("code Online")

    @commands.hybrid_command(name="code", description="Send the game code to the server owner!")
    async def code(self, ctx, game: str, code: str):
        if game == "Rocket League":
            # get the server owner
            owner = ctx.guild.owner
            await owner.send(f"Hey! {ctx.author} is looking for a game of Rocket League! Their code is `{code}`")
            await ctx.send("Message sent to server owner")
        elif game == "Smash Bros":
            # get the server owner
            owner = ctx.guild.owner
            await owner.send(f"Hey! {ctx.author} is looking for a game of Smash Bros! Their code is `{code}`")
            await ctx.send("Message sent to server owner")
        else:
            await ctx.send("That game either isn't supported or you misspelled\nSupported games: Rocket League, Smash Bros")


async def setup(bot):
    await bot.add_cog(code(bot))