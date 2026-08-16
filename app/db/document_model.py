from models.enums.DataBaseEnum import DataBaseEnums
from models.db_schemes.document import Document
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger(__name__)



class DocumentModel:
    def __init__(self, db_client: AsyncIOMotorClient) -> None:
        self.db_client = db_client
        self.collection = self.db_client[DataBaseEnums.DOCUMENTS_COLLECTION.value]
    
    
    @classmethod
    async def get_instance(cls,db_client:AsyncIOMotorClient):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections =  self.db_client.list_collection_names()
        if all_collections and DataBaseEnums.DOCUMENTS_COLLECTION.value not in all_collections:
            self.db_client.create_collection(DataBaseEnums.DOCUMENTS_COLLECTION.value)

    async def upload_document(self, doc: Document):
        result = await self.collection.insert_one(doc.model_dump())
        doc.id = result.inserted_id
        return result

    async def delete_document(self, doc_name: str):
         return await self.collection.find_one_and_delete({"doc_name": doc_name})

    async def get_document(self, doc_name: str):
        record = await self.collection.find_one({"doc_name": doc_name})
        if record:
            return Document(**record)




