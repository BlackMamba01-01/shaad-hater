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


async def start_game(ctx, active_players):
    """Handles the country guessing game logic."""
    country = random.choice(countries)
    search_term = country["search_term"]
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {"query": search_term, "per_page": 1}

    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.unsplash.com/search/photos", headers=headers, params=params) as response:
            data = await response.json()
            if not data["results"]:
                await ctx.send("⚠️ Couldn't retrieve an image. Try again.")
                active_players.discard(ctx.author.id)  # Allow user to use commands again
                return
            
            image_url = data["results"][0]["urls"]["regular"]
            embed = discord.Embed(title="Guess the Country! You have 3 attempts.")
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)

            attempts = 3
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author

            while attempts > 0:
                try:
                    guess = await ctx.bot.wait_for("message", check=check, timeout=60.0)
                    if guess.content.strip().lower() == country["name"].lower():
                        await ctx.send(f"✅ Correct! The country is {country['name']}.")
                        break
                    else:
                        attempts -= 1
                        if attempts > 0:
                            await ctx.send(f"❌ Incorrect! {attempts} attempts left.")
                        else:
                            await ctx.send(f"❌ Game over! The country was {country['name']}.")
                except asyncio.TimeoutError:
                    await ctx.send(f"⏳ Time's up! The country was {country['name']}.")
                    break

            active_players.discard(ctx.author.id)  # Remove user when game ends
