from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    discord_id: int = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SteamAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    encrypted_username: str
    encrypted_shared_secret: str
    encrypted_revocation_code: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RedeemKey(SQLModel, table=True):
    key: str = Field(primary_key=True)
    is_used: bool = Field(default=False)
    used_by: Optional[int] = Field(default=None, foreign_key="user.id")
    used_at: Optional[datetime] = None
    duration_days: int = 30

class UserAccess(SQLModel, table=True):
    user_id: int = Field(primary_key=True, foreign_key="user.id")
    valid_until: datetime
