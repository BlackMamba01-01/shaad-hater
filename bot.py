import discord
from discord.ext import commands
import os
import asyncio
import threading
from flask import Flask
from assessment import message_analysis_and_response  
import countryguessr as geo

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Setup intents
intents = discord.Intents.default()
intents.message_content = True  # Required for reading messages
intents.guilds = True
intents.members = True  # Required for role-based logic

cuck_role = "Cuck"  # Default role

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=intents)

active_players = set()

# ---------------- DISCORD BOT EVENTS ---------------- #
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

# ------------------- GEO GUESSR COMMANDS ------------------- #

@bot.before_invoke
async def check_if_playing(ctx):
    """Prevents users from using other commands while they are in a game."""
    if ctx.author.id in active_players and ctx.command.name != "guessend":
        await ctx.send("⚠️ You're already in a game! Finish it or use `!guessend` to stop.")
        raise commands.CheckFailure("User is already in a game")

@bot.command()
async def guessend(ctx):
    """Ends the guessing game and removes the user from active players."""
    if ctx.author.id in active_players:
        active_players.remove(ctx.author.id)
        await ctx.send("✅ Your game has been ended. You can now use other commands.")
    else:
        await ctx.send("⚠️ You're not currently playing a game.")

# Hook the game command into bot.py
@bot.command()
async def countryguessr(ctx):
    """Starts the country guessing game."""
    if ctx.author.id in active_players:
        await ctx.send("⚠️ You're already playing! Use `!guessend` to stop.")
        return

    active_players.add(ctx.author.id)  # Add user to active players
    await geo.start_game(ctx, active_players)  # Call function from countryguessr.py


# ------------------- ADMIN ONLY COMMANDS ------------------- #

@bot.command()
@commands.has_permissions(administrator=True)
async def set_role(ctx, *, role_name: str):
    """Admin command to set the target role"""
    global cuck_role
    cuck_role = role_name
    await ctx.send(f"✅ Role set to: `{role_name}`")

@bot.command()
@commands.has_permissions(administrator=True)
async def check_set_role(ctx):
    """Admin command to check the target role"""
    await ctx.send(f"🔍 Current Role: `{cuck_role}`")

# ------------------- ALL MESSAGE (NO COMMAND) ------------------- #

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore bot messages

    ctx = await bot.get_context(message)

    if ctx.valid:
        await bot.process_commands(message)  # ✅ Run command and stop further processing
        return  

    # ✅ Only process normal messages (not commands)
    if any(role.name == cuck_role for role in message.author.roles):
        response = message_analysis_and_response(message.content)
        await message.channel.send(f"{message.author.mention}\n{response[:2000]}") 

# ------------------- DEBUG COMMANDS ------------------- #

@bot.command()
async def hello(ctx):
    """Simple hello command"""
    await ctx.send("Hello!")

@bot.command()
async def debug(ctx):
    """Command to check if bot is working"""
    await ctx.send("Debug: ✅ Bot is running!")

# ---------------- KEEP ALIVE (FLASK SERVER) ---------------- #
# ------------------- IGNORE CODE BELOW  ------------------- #
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running on Render!"

def run_flask():
    app.run(host="0.0.0.0", port=7865)  # Render requires a web service

# Start Flask in a separate thread (Daemon Mode to prevent blocking)
threading.Thread(target=run_flask, daemon=True).start()

# Run the bot
bot.run(TOKEN)
