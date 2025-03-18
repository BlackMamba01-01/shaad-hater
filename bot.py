import discord
from discord.ext import commands
import os
import asyncio
import sys
from assessment import message_analysis_and_response
import threading
from flask import Flask

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Required to read user messages
intents.members = True  # Required to check roles

cuck_role = "Cuck"

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

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
    """Admin command to set the target role"""
    global cuck_role
    await ctx.send(f" Role is: `{cuck_role}`")

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

@bot.event
async def on_disconnect():
    print("⚠️ Bot disconnected! Restarting...")
    await asyncio.sleep(5)
    os.execv(sys.executable, [sys.executable] + sys.argv)  # Restart the bot

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running on Render!"

def run_flask():
    app.run(host="0.0.0.0", port=7865)  # Render requires a web service

# Run Flask in a separate thread
threading.Thread(target=run_flask).start()

bot.run(TOKEN)
