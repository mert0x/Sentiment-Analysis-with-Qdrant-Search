from pydantic import BaseModel
from qdrant_client.http import models
import constants
from typing import Optional


class RecommendParams(BaseModel):
        CollectionName : str
        Positive : list 
        Negative : list 
        QueryFilter : Optional[models.Filter] = None  
        Limit : Optional[int] = 5 
        ScoreThreshold : Optional[float] = None


filter_negative = models.Filter(
        must= [models.FieldCondition(
                key= "label",
                match=models.MatchValue(value=0)
        )],
)

filter_positive = models.Filter(
        must= [models.FieldCondition(
                key= "label",
                match=models.MatchValue(value=1)
        )],
)

#STANFORD_IMDB_NLP

params_imdb = RecommendParams(CollectionName= constants.COLLECTION_NAME_IMDB,Positive = [15,459], Negative= [2,24,1804], Limit= 3)

#With filter
params_imdb2 = RecommendParams(CollectionName= constants.COLLECTION_NAME_IMDB,Positive = [5,980], Negative= [1002,159], Limit= 3, QueryFilter= filter_negative)

#With Score Threshold
params_imdb3 = RecommendParams(CollectionName= constants.COLLECTION_NAME_IMDB,Positive = [987], Negative= [1900,47,80], Limit= 3, ScoreThreshold=0.50)


#-------------------------------------------------------------------------------------------------------------------------------------------
#AMAZON POLARITY

params_amazon = RecommendParams(CollectionName= constants.COLLECTION_NAME_AMAZON,Positive = [1444,1300], Negative= [6,804], Limit= 3)

params_amazon2 = RecommendParams(CollectionName= constants.COLLECTION_NAME_AMAZON,Positive = [13,1000], Negative= [88], Limit= 3, QueryFilter = filter_positive)

params_amazon3 = RecommendParams(CollectionName= constants.COLLECTION_NAME_AMAZON,Positive = [424,136], Negative= [968], Limit= 3, ScoreThreshold= 0.2)
