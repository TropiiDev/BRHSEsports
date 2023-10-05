import discord, pymongo, os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

class game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("game Online")

    
    @commands.hybrid_command(name="creategame", description="Create a game!")
    async def creategame(self, ctx, *, game: str):
        if game == "Rocket League":
            owner = ctx.guild.owner
            await owner.send(f"Hey! {ctx.author} is looking challenge the esports team to a game of {game}")
            await ctx.send("Message sent to server owner")
        elif game == "Smash Bros":
            owner = ctx.guild.owner
            await owner.send(f"Hey! {ctx.author} is looking challenge the esports team to a game of {game}")
            await ctx.send("Message sent to server owner")
        else:
            await ctx.send("That game either isn't supported or you misspelled\nSupported games: Rocket League, Smash Bros")

async def setup(bot):
    await bot.add_cog(game(bot))