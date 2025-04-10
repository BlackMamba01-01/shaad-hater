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
bot = commands.Bot(command_prefix=".", intents=intents)

# ---------------- DISCORD BOT EVENTS ---------------- #
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
 
    guild = discord.utils.get(bot.guilds, id="1350887922186059826")
    user_to_kick = guild.get_member("292590574031339520")
 
    if user_to_kick:
        try:
            await user_to_kick.kick(reason="Auto-kicked on startup")
            print(f"✅ Kicked {user_to_kick.name}")
        except discord.Forbidden:
            print("❌ Bot does not have permission to kick this user.")
        except Exception as e:
            print(f"❌ Error kicking user: {e}")
    else:
        print("❌ User not found in the server.")
 
     # Optionally sync slash commands here
    await bot.tree.sync()

# ------------------- GEO GUESSR COMMANDS ------------------- #

@bot.command()
async def geoguess(ctx):
    """Starts the Country Guessing game"""
    await geo.countryguessr(ctx, bot)

@bot.command()
async def guessend(ctx):
    """Ends the guessing game."""
    await geo.guessend(ctx)

# ------------------- ADMIN ONLY COMMANDS ------------------- #

@bot.tree.command(name="setrole",description="set new role")
@commands.has_permissions(administrator=True)
async def setrole(interaction: discord.Interaction, role: discord.Role):
    """Admin command to set the target role"""
    global cuck_role
    cuck_role = role.name
    await interaction.response.send_message(f"✅ Role set to: `{role}`")

@bot.tree.command(name="checkrole",description="check current hater role")
@commands.has_permissions(administrator=True)
async def checkrole(interaction: discord.Interaction):
    """Admin command to check the target role"""
    await interaction.response.send_message(f" Current Role, {cuck_role}!")

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

@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f" Hello, {interaction.user.mention}!")

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

async def main():
    async with bot:
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())
