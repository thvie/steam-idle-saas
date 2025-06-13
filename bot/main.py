import discord
from discord.ext import commands
from config.settings import settings
import asyncio
import logging
from bot.cogs.connect import ConnectCog
from bot.cogs.redeem import RedeemCog

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot giriş yaptı: {bot.user}")

async def setup():
    await bot.add_cog(ConnectCog(bot))
    await bot.add_cog(RedeemCog(bot))

async def main():
    await setup()
    await bot.start(settings.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
