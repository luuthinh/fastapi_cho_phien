import os

from dotenv import load_dotenv
from databases import DatabaseURL

MONGODB_URL = os.getenv("MONGODB_URL", "")

if not MONGODB_URL:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER = os.getenv("MONGO_USER", "userdb")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "pass")
    MONGO_DB = os.getenv("MONGO_DB","fastapi")

    MONGODB_URL = DatabaseURL(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}")
else:
    MONGO_URL = DatabaseURL(MONGODB_URL)

print("ppp", MONGODB_URL)
database_name = MONGO_DB    