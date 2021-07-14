import os
from discord.ext import commands
from dotenv import load_dotenv
import requests
import textwrap
import yfinance as yf


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GoldAPI_KEY = os.getenv("GoldAPI_KEY")

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
    response = "\n".join([f"{LABELS[category]}: {ticker.info[category]}" for category in CATEGORIES])
    await ctx.send(f"```{response}```")

@bot.command(name="dd", help="Fetches information on provided ticker")
async def dd(ctx, symbol):
    print("received")
    ticker = yf.Ticker(symbol)
    response = "\n".join([f"{key}: {ticker.info[key]}" for key in ticker.info.keys()])
    for line in textwrap.wrap(response, 1996):
        await ctx.send(f"```{line}```")

@bot.command(name="spot", help="Returns spot price of provided precious metal")
async def spot(ctx, symbol):
    print("recieved")
    METALS = {
        "gold": "XAU",
        "au": "XAU",
        "silver": "XAG",
        "ag": "XAG",
        "platinum": "XPT",
        "pt": "XPT",
        "palladium": "XPD",
        "pd": "XPD"
    }
    if symbol.lower() not in METALS:
        await ctx.send("`Invalid selection`")
        return
    url = f"https://www.goldapi.io/api/{METALS[symbol.lower()]}/USD/"
    headers = {
        "x-access-token": GoldAPI_KEY,
        "Content-Type": "application/json"
    }
    payload = requests.get(url, headers=headers).json()
    CATEGORIES = ("symbol", "prev_close_price", "open_price", "price")
    LABELS = {
        "symbol": "Symbol",
        "prev_close_price": "Previous Close",
        "open_price": "Open",
        "price": "Price"
    }
    response = "\n".join([f"{LABELS[category]}: {payload[category]}" for category in CATEGORIES])
    await ctx.send(f"```{response}```")



bot.run(TOKEN)