import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!hi', intents=discord.Intents.default())

# Load the botcommands extension
bot.load_extension('botcommands')
bot.load_extension('levellingsystem')

#botrpc
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name = "commands."))
    print("Bot RPC OK")
    print("Bot Ready.")

#run bot
bot.run('MTI4MTE0MzY1MTQyNjEwNzQxMw.Gury7V.uFwXPDfunF0ybi9eEWjq3r1WPTkhhZGK1dbgWM')