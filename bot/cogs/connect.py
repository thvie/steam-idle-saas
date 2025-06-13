import discord
from discord.ext import commands
from discord import app_commands
from bot.utils.encryption import encrypt
from db.crud import get_or_create_user, save_steam_account
from config.settings import settings
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import create_async_engine

engine = create_async_engine(settings.DATABASE_URL)

class ConnectModal(discord.ui.Modal, title="Steam Hesabını Bağla"):
    username = discord.ui.TextInput(label="Steam kullanıcı adı")
    shared_secret = discord.ui.TextInput(label="Shared Secret", style=discord.TextStyle.short)
    revocation_code = discord.ui.TextInput(label="Revocation Code", required=False)

    def __init__(self, bot, interaction):
        super().__init__()
        self.bot = bot
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        async with AsyncSession(engine) as session:
            user = await get_or_create_user(session, interaction.user.id)
            await save_steam_account(
                session, user,
                encrypt(self.username.value),
                encrypt(self.shared_secret.value),
                encrypt(self.revocation_code.value or "")
            )
        await interaction.response.send_message("✅ Steam hesabın başarıyla bağlandı!", ephemeral=True)

class ConnectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="connect", description="Steam hesabını bağla")
    async def connect(self, interaction: discord.Interaction):
        modal = ConnectModal(self.bot, interaction)
        await interaction.response.send_modal(modal)
