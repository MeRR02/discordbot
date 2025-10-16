import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import logging
import asyncio

load_dotenv()
TOKEN: str | None = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set!")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Ready to fight? {bot.user} 1v1 bot activated!')

@bot.command()
async def destroy(ctx, opponent: discord.Member):
    
    challenger = ctx.author

    #if opponent == challenger:
    #    await ctx.send("You can’t challenge yourself!")
    #    return
    #
    #if opponent == bot.user:
    #    await ctx.send("I appreciate the challenge, but I’m just a bot!")
    #    return

    # Ask the opponent for confirmation
    msg = await ctx.send(f"💥 {opponent.mention}, {challenger.mention} has challenged you to a 1v1!")

    # Add reaction options
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

    def check(reaction, user):
        return (user == opponent and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id)

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send(f"⌛ {opponent.mention} didn’t respond in time. Challenge canceled.")
        return

    if str(reaction.emoji) == "✅":
        await ctx.send(f"🔥 {opponent.mention} accepted the challenge!")
        # Send DMs
        try:
            await challenger.send(f"You have challenged {opponent.name} to a 1v1! Here is your party code: `ABC123`")
        except discord.Forbidden:
            await ctx.send(f"{challenger.mention}, I can't DM you!")
            await ctx.send("Party code will be shared here: `ABC123`")

        try:
            await opponent.send(f"You have been challenged by {challenger.name} to a 1v1! Here is your party code: `XYZ789`")
        except discord.Forbidden:
            await ctx.send(f"{opponent.mention}, I can't DM you!")
            await ctx.send("Party code will be shared here: `XYZ789`")

    else:
        await ctx.send(f"🐔 {opponent.mention} chickened out!")

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)