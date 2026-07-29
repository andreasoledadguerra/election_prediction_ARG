import os
from motor.motor_asyncio import AsyncIOMotorClient


class MongoRepository:

    DB_NAME = os.getenv("MONGO_DB", "election_prediction")
    COLLECTION_NAME = "resultados_electorales"

    def __init__(self):
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[self.DB_NAME]
        self.collection = self.db[self.COLLECTION_NAME]

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