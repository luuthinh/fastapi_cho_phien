import logging
_logger = logging.getLogger(__name__)

from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from .mongodb import db


async def connect_to_mongo():
    _logger.info("Connect to mongo server....")
    # db.client = AsyncIOMotorClient(str(MONGODB_URL), 
    #                                maxPoolSize=MAX_CONNECTIONS_COUNT,
    #                                minPoolSize=MIN_CONNECTIONS_COUNT)
    db.client = AsyncIOMotorClient('localhost',27017)
    _logger.info("Connect success.")


async def close_mongo_connection():
    _logger.info("Disconnect mongo server....")
    db.client.close()
    _logger.info("Disconnect success")