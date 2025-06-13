import discord
from discord.ext import commands
from discord import app_commands
from db.crud import get_or_create_user, redeem_key
from config.settings import settings
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import create_async_engine

engine = create_async_engine(settings.DATABASE_URL)

class RedeemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="redeem", description="Lisans anahtarını kullan")
    async def redeem(self, interaction: discord.Interaction, key: str):
        async with AsyncSession(engine) as session:
            user = await get_or_create_user(session, interaction.user.id)
            success = await redeem_key(session, key, user)

            if success:
                await interaction.response.send_message(
                    f"✅ Anahtar başarıyla kullanıldı. {key.duration_days} gün boyunca erişimin açıldı.",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "❌ Bu anahtar geçersiz veya daha önce kullanılmış.",
                    ephemeral=True
                )
