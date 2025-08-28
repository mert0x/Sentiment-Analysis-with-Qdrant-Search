from pydantic import BaseModel, StrictStr, Field
from typing import Optional,Union
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import VectorParams, Distance, ScalarQuantization, ScalarQuantizationConfig, VectorParams, BinaryQuantization, BinaryQuantizationConfig
import pandas as pd
from sentence_transformers import SentenceTransformer
from loguru import logger
from SearchParams import SearchParams
from RecommendParams import RecommendParams


class ClientOptions(BaseModel):
    url: Optional[StrictStr] = Field(default= "http://localhost:6333")
    model_name: Optional[StrictStr] = Field(default= "all-MiniLM-L6-v2")
    payload_indexing: Optional[StrictStr] = Field(default= "no_indexing")
    payload_schema: Optional[tuple[str,models.PayloadSchemaType]] = None
    quantization: Optional[StrictStr] = Field(default = None)  #Scalar and Binary quantization is implemented, 
                                                    #any other strings provided would trigger default behaviour.

    def get_model(self):
        return SentenceTransformer(self.model_name)
    
    def get_quantizationconfig(self):
        if(self.quantization == "ScalarQuantization"):
            return ScalarQuantization(
                    scalar= ScalarQuantizationConfig(
                        type="int8",
                        quantile= 0.99,
                        always_ram= True
                    )
                )
        
        elif(self.quantization == "BinaryQuantization"):
            return BinaryQuantization(
                    binary= BinaryQuantizationConfig(
                        always_ram= True
                    )
                )
        else:
            return None


    def get_vectorconfig(self) -> VectorParams:
        
            return models.VectorParams(
                size = 384,
                distance = Distance.COSINE,
                quantization_config= self.get_quantizationconfig())
    
    def get_payloadschema(self) -> tuple[str, models.PayloadSchemaType]:
            """
            Returns the payload indexing configuration based on the 'payload_indexing' field.
            """
            if self.payload_indexing == "default":
                return ["default", None]
            
            elif self.payload_indexing == "no_indexing":
                return ["no_indexing", None]
            
            elif self.payload_indexing == "custom":
                return self.payload_schema
        
class ClientService:
    
    def __init__(self, client_config: "ClientOptions" = ClientOptions()):
        self.api = QdrantClient(client_config.url)
        self.model_name = client_config.model_name
        self.model = client_config.get_model()
        self.payload_indexing = client_config.payload_indexing
        self.payloadschema = client_config.get_payloadschema()
        self.quantization = client_config.quantization
        self.quantization_config = client_config.get_quantizationconfig()
        self.vectors_config = client_config.get_vectorconfig()
        print("test")
    
    def DeleteCollection(self, CollectionName):
        self.api.delete_collection(CollectionName)
        logger.info("DeleteCollection is successfull.")
    
    def CreateCollection(self, CollectionName : str, ShardNumber : int):
        
        if(self.api.collection_exists(CollectionName)):
            self.DeleteCollection(CollectionName)
        
        self.api.create_collection(collection_name= CollectionName, vectors_config= self.vectors_config, shard_number= ShardNumber, quantization_config= self.quantization_config)
        
        if(self.quantization == None):
            logger.info(f"{CollectionName} collection  is created with {ShardNumber} shards with no quantization.")
        else:
            logger.info(f"{CollectionName} collection  is created with {ShardNumber} shards with {self.quantization}.")            
    
    def Upsert(self, CollectionName, DataPoints):
        self.api.upsert(collection_name= CollectionName, points= DataPoints)

    def CreatePayloadIndex(self, CollectionName,):
        if(self.payload_indexing == "custom"):
            self.api.create_payload_index(collection_name= CollectionName,field_name= self.payloadschema[0],field_schema= self.payloadschema[1])
            logger.info("CreatePayloadIndex is successfull.")

    def Search(self, Params : SearchParams):
        return self.api.search(collection_name = Params.CollectionName, query_vector = Params.GetQueryVector(), score_threshold= Params.ScoreThreshold, query_filter= Params.QueryFilter, limit= Params.Limit)
    
    def Recommend(self, Params : RecommendParams):
        return self.api.recommend(collection_name= Params.CollectionName, positive= Params.Positive, negative= Params.Negative,limit= Params.Limit, query_filter= Params.QueryFilter, score_threshold=Params.ScoreThreshold)