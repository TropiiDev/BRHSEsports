import discord, pymongo, os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

class setprefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Prefix Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"prefix"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"prefix"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="setprefix", description="Set the prefix for the server")
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self, ctx, prefix:str):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.prefixes

        await ctx.send(f"Prefix set to `{prefix}`")
        coll.update_one({"_id":ctx.guild.id}, {"$set":{"prefix":prefix}})

    @commands.hybrid_command(name="prefix", description="Get the prefix for the server")
    @commands.check(is_enabled)
    async def prefix(self, ctx):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.prefixes

        prefix = coll.find_one({"_id":ctx.guild.id})["prefix"]
        await ctx.send(f"The prefix for this server is `{prefix}`")

async def setup(bot):
    await bot.add_cog(setprefix(bot))