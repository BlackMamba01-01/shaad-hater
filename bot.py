import discord
from discord.ext import commands
import os
from assessment import message_analysis_and_response

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
    print(f"Logged in as {bot.user}")

@bot.command()
@commands.has_permissions(administrator=True)  # Only admins can use this
async def set_role(ctx, *, role_name: str):
    global cuck_role
    cuck_role = role_name
    await ctx.send(f"✅ Role set to: `{role_name}`")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore bot's own messages

    if message.content.startswith("!"):
        return

    if any(role.name == cuck_role for role in message.author.roles):
        response = message_analysis_and_response(message.content)  # No need for str(message.content)
        await message.channel.send(f"{message.author.mention}\n{response[:2000]}") 


@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.event
async def on_disconnect():
    print("Bot disconnected! Restarting...")
    await asyncio.sleep(5)  # Wait a bit before reconnecting
    os.execv(__file__, ["python"] + sys.argv)  # Restart the scrip

bot.run(TOKEN)

