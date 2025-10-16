import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import logging

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='%', intents=intents)

@bot.event
async def on_ready():
    print(f'Ready to fight? {bot.user} 1v1 bot activated!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)

@bot.command()
async def skirmish(ctx, *, question):
    await ctx.send('1V1!')

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)