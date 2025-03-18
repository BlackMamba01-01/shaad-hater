import discord
from discord.ext import commands
import random
import aiohttp
import asyncio
import os

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

countries = [
    {"name": "France", "search_term": "random village France"},
    {"name": "Japan", "search_term": "small town Japan"},
    {"name": "Brazil", "search_term": "hidden beach Brazil"},
    {"name": "Canada", "search_term": "remote cabin Canada"},
    {"name": "Norway", "search_term": "fjord Norway"},
    {"name": "Russia", "search_term": "Siberian town"},
    {"name": "South Africa", "search_term": "random street South Africa"},
    {"name": "Mongolia", "search_term": "yurt village"},
    {"name": "Chile", "search_term": "Patagonia landscape"},
    {"name": "Iceland", "search_term": "volcanic landscape Iceland"},
]

active_games = {}  # Tracks users currently playing


async def get_country_image():
    """Fetches a random country image from Unsplash API."""
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
    """Starts the country guessing game."""
    if ctx.author.id in active_games:
        await ctx.send("❌ You're already in a game! Use `!guessend` to quit.")
        return

    country, image_url = await get_country_image()
    if not country:
        await ctx.send("❌ Couldn't retrieve an image. Try again.")
        return

    active_games[ctx.author.id] = {"country": country, "attempts": 3}

    embed = discord.Embed(title="🌍 Guess the Country! (You have 3 tries)")
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for attempt in range(3):
        try:
            guess = await bot.wait_for("message", check=check, timeout=60.0)
            if guess.content.strip().lower() == country.lower():
                await ctx.send(f"✅ Correct! The country is **{country}**.")
                del active_games[ctx.author.id]
                return
            else:
                remaining = 2 - attempt
                await ctx.send(f"❌ Incorrect! {remaining} guesses left." if remaining > 0 else "❌ Game over!")
        except asyncio.TimeoutError:
            await ctx.send(f"⏳ Time's up! The country was **{country}**.")
            break

    del active_games[ctx.author.id]  # Remove user from active games


async def guessend(ctx):
    """Ends the guessing game for a user."""
    if ctx.author.id in active_games:
        del active_games[ctx.author.id]
        await ctx.send("❌ You have quit the game.")
    else:
        await ctx.send("❌ You are not in a game.")
