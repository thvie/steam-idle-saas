import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

class Settings:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    FERNET_KEY = os.getenv("FERNET_KEY")

    @staticmethod
    def get_fernet():
        return Fernet(Settings.FERNET_KEY.encode())

settings = Settings()
