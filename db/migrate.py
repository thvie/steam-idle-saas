import asyncio
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import create_async_engine
from config.settings import settings
from db.models import User, SteamAccount, RedeemKey, UserAccess

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✅ Veritabanı tabloları başarıyla oluşturuldu.")

if __name__ == "__main__":
    asyncio.run(init_db())
