import importlib
import discord
from discord.ext import commands

sqzlib = importlib.import_module('commands.sqz')
sqzdxlib = importlib.import_module('commands.stonks')

TOKEN = 'INSERT_TOKEN_HERE'

client = discord.Client()
bot = commands.Bot(command_prefix="!", case_insensitive=True)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# @bot.event
# async def on_message(message):
#     if message.content == '!chibi help':
#         await message.channel.send('I am here to help!')
@bot.command(name='dix', description='Get daily dix (deprecated)')
async def dix(ctx):
    await ctx.send(f'This command is deprecated. Please use the command `!sqz` instead') 

@bot.command(name='sqz', description='Get daily squeeze metrics')
async def sqz(ctx):
    report = sqzlib.get_sqz_metrics_report()
    await ctx.send(f'Here is your sqz report:\n{report}') 
    
@bot.command(name='sqzdx', description='Get daily squeeze metrics analysis')
async def sqzdx(ctx):
    chart_images = sqzdxlib.get_sqz_analysis()
    for chart_image in chart_images:
        await ctx.send(file=discord.File(fp=chart_image, filename='sqzdx.png'))

bot.run(TOKEN)