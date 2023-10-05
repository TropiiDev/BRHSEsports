import discord, pymongo, os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

class rl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("rl Online")

    @commands.hybrid_command(name="rl", description="Check stats on Rocket League!")
    async def rl(self, ctx, player: str = None):
        await ctx.send("Getting stats...")
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.rlstats
        rl_wins = coll.find_one({"_id": {"game": "Rocket League"}})['wins']
        rl_losses = coll.find_one({"_id": {"game": "Rocket League"}})['losses']
        players = coll.find_one({"_id": {"player": player}})
        if player == None:
            em = discord.Embed(title="Stats", description="Stats of game won vs game loss and player points", color=0x00ff00)
            em.add_field(name="Wins", value=rl_wins, inline=True)
            em.add_field(name="Losses", value=rl_losses, inline=True)
            em.set_footer(text="Created by: @fstropii")
            await ctx.send(embed=em)
        elif players:
            player_score = coll.find_one({"_id": {"player": player}})["score"]
            player_assists = coll.find_one({"_id": {"player": player}})["assists"]
            em = discord.Embed(title=f"Stats for {player}", description="Player Score and Assists for every game played", color=0x00ff00)
            em.add_field(name="Player Score: ", value=player_score, inline=False)
            em.add_field(name="Player Assists: ", value=player_assists, inline=False)
            em.set_footer(text="Created by: @fstropii")
            await ctx.send(embed=em)
        else:
            await ctx.send("That player does not exist")

    @commands.hybrid_command(name="addrl", description="Add a game to the Rocket League stats!")
    @commands.has_permissions(administrator=True)
    async def addrl(self, ctx, wins: int, losses: int):
        await ctx.send("Adding stats...")
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.rlstats

        if coll.find_one({"_id": {"game": "Rocket League"}}):
            coll.update_one({"_id": {"game": "Rocket League"}}, {"$inc":{"wins":wins, "losses":losses}})
            await ctx.send("Updated")
        else:
            coll.insert_one({"_id": {"game": "Rocket League"}, "wins":wins, "losses":losses})
            await ctx.send("Added")

    @commands.hybrid_command(name="edituser", description="Add a game to the Rocket League stats!")
    @commands.has_permissions(administrator=True)
    async def edituser(self, ctx, player_name: str, score: int, assists: int):
        await ctx.send("Adding stats...")
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.rlstats

        if coll.find_one({"_id": {"player": player_name}}):
            coll.update_one({"_id": {"player": player_name}}, {"$inc":{"score":score, "assists":assists}})
            await ctx.send("Updated")
        else:
            coll.insert_one({"_id": {"player": player_name}, "score":score, "assists":assists})
            await ctx.send("Added")


async def setup(bot):
    await bot.add_cog(rl(bot))