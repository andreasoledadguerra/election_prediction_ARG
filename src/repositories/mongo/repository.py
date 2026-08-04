import os
from motor.motor_asyncio import AsyncIOMotorClient


class MongoRepository:

    def __init__(self, mongo_url: str, db_name: str, collection_name:str):
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    async def insert_if_not_exists(self, params: dict, response_json: dict) -> bool:
        """
        Inserta un documento con la estructura {params, response_json}.
        Si ya existe un documento con los mismos params, no lo inserta.

        Returns:
            True si se insertó, False si ya existía.
        """
        existing = await self.collection.find_one({"params": params})
        if existing:
            return False

        await self.collection.insert_one({
            "params": params,
            "response_json": response_json,
        })
        return True