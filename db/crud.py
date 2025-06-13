from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import User, SteamAccount, RedeemKey, UserAccess
from datetime import datetime, timedelta

async def get_or_create_user(session: AsyncSession, discord_id: int) -> User:
    result = await session.exec(select(User).where(User.discord_id == discord_id))
    user = result.first()
    if not user:
        user = User(discord_id=discord_id)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user

async def save_steam_account(session: AsyncSession, user: User, username: str, shared_secret: str, revocation_code: str):
    acc = SteamAccount(
        user_id=user.id,
        encrypted_username=username,
        encrypted_shared_secret=shared_secret,
        encrypted_revocation_code=revocation_code,
    )
    session.add(acc)
    await session.commit()

async def redeem_key(session: AsyncSession, key: str, user: User) -> bool:
    result = await session.exec(select(RedeemKey).where(RedeemKey.key == key))
    k = result.first()
    if not k or k.is_used:
        return False
    k.is_used = True
    k.used_by = user.id
    k.used_at = datetime.utcnow()
    access = UserAccess(user_id=user.id, valid_until=datetime.utcnow() + timedelta(days=k.duration_days))
    session.add(k)
    session.merge(access)
    await session.commit()
    return True

async def has_valid_access(session: AsyncSession, user: User) -> bool:
    result = await session.exec(select(UserAccess).where(UserAccess.user_id == user.id))
    access = result.first()
    return access and access.valid_until > datetime.utcnow()
