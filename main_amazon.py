from ClientClass import ClientService, ClientOptions
from DataParquet import DataParquet
import constants
from qdrant_client.http.models import PayloadSchemaType
import SearchParams
import RecommendParams


#Initiating a client class object
client = ClientService(client_config= ClientOptions(quantization= "BinaryQuantization",payload_indexing= "custom", payload_schema=["label", PayloadSchemaType.INTEGER]))
client.CreateCollection(constants.COLLECTION_NAME_AMAZON, ShardNumber= 1)
client.CreatePayloadIndex(constants.COLLECTION_NAME_AMAZON)


#Initiating a data class object
data_obj_amazon = DataParquet(path = constants.AMAZON_PARQUET_FILE_PATH, batch_size= constants.BATCH_SIZE, main_column="content")
data_obj_amazon.process_df(client , CollectionName= constants.COLLECTION_NAME_AMAZON)


#-----------------------------------------------------------------------------------------------------------------------------------------
#SEARCH FOR AMAZON

result = client.Search(SearchParams.param_amazon_review)
#print(result)

result = client.Search(SearchParams.param_amazon_review2)
#print(result)

result = client.Search(SearchParams.param_amazon_review3)
#print(result)

result = client.Search(SearchParams.param_amazon_review4) #Reviews has the word amazing in its title
print(result)

#--------------------------------------------------------------------------------------------------------------------------------------------
#RECOMMEND FOR AMAZON

result = client.Recommend(RecommendParams.params_amazon)
#print(result)

result = client.Recommend(RecommendParams.params_amazon2)
#print(result)

result = client.Recommend(RecommendParams.params_amazon3)
print(result)
#--------------------------------------------------------------------------------------------------------------------------------------------------
