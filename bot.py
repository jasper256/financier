import os
from discord.ext import commands
from dotenv import load_dotenv
import textwrap
import yfinance as yf


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="$")

@bot.command(name="quote", help="Fetches stock quote for provided ticker")
async def quote(ctx, symbol):
    print("received")
    CATEGORIES = ("shortName", "currentPrice", "open", "previousClose", "volume24Hr")
    LABELS = {"shortName": "Name", 
        "currentPrice": "Current Price", 
        "open": "Market Open", 
        "previousClose": "Previous Close", 
        "volume24Hr": "24 Hour Volume"
    }
    ticker = yf.Ticker(symbol)
    response = "```" + "\n".join([f"{LABELS[category]}: {ticker.info[category]}" for category in CATEGORIES]) + "```"
    await ctx.send(response)

@bot.command(name="dd", help="Fetches information on provided ticker")
async def dd(ctx, symbol):
    print("received")
    ticker = yf.Ticker(symbol)
    response = "\n".join([f"{key}: {ticker.info[key]}" for key in ticker.info.keys()])
    for line in textwrap.wrap(response, 1996):
        await ctx.send(f"```{line}```")

bot.run(TOKEN)