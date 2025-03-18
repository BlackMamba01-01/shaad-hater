import discord
from discord.ext import commands
import os
import asyncio
import threading
from flask import Flask
from assessment import message_analysis_and_response  
from countryguessr import countryguessr

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Setup intents
intents = discord.Intents.default()
intents.message_content = True  # Required for reading messages
intents.guilds = True
intents.members = True  # Required for role-based logic

cuck_role = "Cuck"  # Default role

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- DISCORD BOT EVENTS ---------------- #
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.command()
async def geoguess(ctx):
    """Starts the Country Guessing game"""
    await countryguessr(ctx, bot)

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

@bot.command()
async def hello(ctx):
    """Simple hello command"""
    await ctx.send("Hello!")

@bot.command()
async def debug(ctx):
    """Command to check if bot is working"""
    await ctx.send("Debug: ✅ Bot is running!")

# ---------------- KEEP ALIVE (FLASK SERVER) ---------------- #
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
