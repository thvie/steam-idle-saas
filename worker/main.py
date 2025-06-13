import asyncio
from config.settings import settings
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, create_async_engine
from db.models import SteamAccount
from bot.utils.encryption import decrypt
from worker.utils.game_detector import detect_real_game_running
from steamcom.async_steam import SteamClient

engine = create_async_engine(settings.DATABASE_URL)

async def idle_loop():
    async with AsyncSession(engine) as session:
        result = await session.exec(select(SteamAccount))
        accounts = result.all()

        tasks = []
        for account in accounts:
            tasks.append(asyncio.create_task(handle_account(account)))
        await asyncio.gather(*tasks)

async def handle_account(account: SteamAccount):
    username = decrypt(account.encrypted_username)
    shared_secret = decrypt(account.encrypted_shared_secret)

    client = SteamClient(username=username, shared_secret=shared_secret)
    try:
        await client.do_login()
        print(f"✅ Giriş başarılı: {username}")
    except Exception as e:
        print(f"❌ Giriş başarısız: {username} - {e}")
        return

    while True:
        game_detected = await detect_real_game_running(client)
        if game_detected:
            await client.stop_idle()
            print(f"⛔ Gerçek oyun algılandı: {username}")
        else:
            await client.start_idle(app_ids=[730])
            print(f"💤 Idling başladı: {username}")
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(idle_loop())
