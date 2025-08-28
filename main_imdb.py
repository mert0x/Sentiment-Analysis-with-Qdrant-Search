from ClientClass import ClientService, ClientOptions
from DataParquet import DataParquet
import constants
from qdrant_client.http.models import PayloadSchemaType
import SearchParams
import RecommendParams


#Initiating a client class object
client = ClientService(client_config= ClientOptions(quantization= "BinaryQuantization",payload_indexing= "custom", payload_schema=["label", PayloadSchemaType.INTEGER]))
client.CreateCollection(constants.COLLECTION_NAME_IMDB, ShardNumber= 1)
client.CreatePayloadIndex(constants.COLLECTION_NAME_IMDB)


#Initiating a data class object
data_obj_movies = DataParquet(path = constants.IMDB_PARQUET_FILE_PATH, batch_size= constants.BATCH_SIZE, main_column="text")
data_obj_movies.process_df(client , CollectionName= constants.COLLECTION_NAME_IMDB)
print(data_obj_movies)

#SEARCH FOR IMDB DATASET
result = client.Search(SearchParams.param_imdb)
#print(result)

result = client.Search(SearchParams.param_imdb2)
#print(result)
#-----------------------------------------------------------------------------------------------------------------------------------------

#RECOMMEND FOR IMDB DATASET
result = client.Recommend(RecommendParams.params_imdb)
#print(result)
#id 1667    

result = client.Recommend(RecommendParams.params_imdb2)
#print(result)

result = client.Recommend(RecommendParams.params_imdb3)
print(result)
#-----------------------------------------------------------------------------------------------------------------------------------------