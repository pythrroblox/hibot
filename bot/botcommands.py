#importing
import discord
from discord.ext import commands
import random

#greetings array
greetings = ["hi bạn nha,", "hi nha,", "con", "chào nha"]

#timeout options (value in seconds)
timeouttimeoptions = [
    discord.OptionChoice(name="1 minute", value=60),
    discord.OptionChoice(name="5 minutes", value=300),
    discord.OptionChoice(name="10 minutes", value=600),
    discord.OptionChoice(name="1 hour", value=3600),
    discord.OptionChoice(name="1 day", value=86400),
    discord.OptionChoice(name="1 week", value=604800)
]

#make bot instance
bot = commands.Bot(command_prefix='!hi', intents=discord.Intents.default())

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #slash commands
    @commands.slash_command(name="ping", description="Check the bot's latency.")
    async def ping(self, ctx):
        latency = self.bot.latency * 1000 
        await ctx.respond(f'Pong! Latency is {latency:.2f}ms') #converted to ms

    @commands.slash_command(name="greet", description="Greet with a random greeting!")
    async def greet(self, ctx, user: discord.User):
        greetingsrandom = random.choice(greetings)
        await ctx.respond(f'{greetingsrandom} {user.display_name}!')

    @commands.slash_command(name="moderatingusers", description="Kick, ban, or timeout a user.")
    async def moderate(self, ctx, user: discord.Member, actions: discord.Option(str, "Choose an action", choices=["kick", "ban", "timeout"]), duration: discord.Option(int, "Choose a duration", choices=timeouttimeoptions) = None, reason: str = "Add a reason here."):
        try:
            if actions == "kick":
                await user.kick(reason=reason)
                await ctx.respond(f'{user.display_name} has been kicked for {reason}', ephemeral=True)
            elif actions == "ban":
                await user.ban(reason=reason)
                await ctx.respond(f'{user.display_name} has been banned for {reason}', ephemeral=True)
            elif actions == "timeout":
                if duration is None:
                    await ctx.respond("Choose a duration to timeout.")
                else:
                    await user.timeout_for(duration, reason=reason)
                    await ctx.respond(f'{user.display_name} has been timed out for {reason}', ephemeral=True)
        except Exception as e:
            await ctx.respond(f'Failed to {actions} {user.display_name}.', ephemeral=True)

def setup(bot):
    bot.add_cog(BotCommands(bot))
