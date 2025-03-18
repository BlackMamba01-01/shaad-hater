import discord
from discord.ext import commands
import random
import aiohttp
import os

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

countries = [
    {"name": "France", "search_term": "Eiffel Tower"},
    {"name": "Japan", "search_term": "Mount Fuji"},
    {"name": "Brazil", "search_term": "Christ the Redeemer"},
    # Add more countries and search terms as needed
]

async def get_country_image():
    """Fetches a random country image from Unsplash"""
    country = random.choice(countries)
    search_term = country["search_term"]
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {"query": search_term, "per_page": 1}

    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.unsplash.com/search/photos", headers=headers, params=params) as response:
            data = await response.json()
            if data["results"]:
                return country["name"], data["results"][0]["urls"]["regular"]
    return None, None

async def countryguessr(ctx, bot):
    """Handles the Country Guessing game logic"""
    country_name, image_url = await get_country_image()
    if not image_url:
        await ctx.send("Couldn't retrieve an image. Try again.")
        return

    embed = discord.Embed(title="Guess the Country!")
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

    def check(m):
        return m.channel == ctx.channel

    try:
        guess = await bot.wait_for("message", check=check, timeout=30.0)
        if guess.content.strip().lower() == country_name.lower():
            await ctx.send(f"✅ Correct! The country is **{country_name}**.")
        else:
            await ctx.send(f"❌ Incorrect! The country was **{country_name}**.")
    except asyncio.TimeoutError:
        await ctx.send(f"⏳ Time's up! The country was **{country_name}**.")
