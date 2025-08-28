from pydantic import BaseModel
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import constants
from typing import Optional

model= SentenceTransformer(constants.MODEL_NAME)

class SearchParams(BaseModel):
    CollectionName : str 
    Query : str
    Limit : int
    ScoreThreshold : Optional[float] =None
    QueryFilter : Optional[models.Filter] = None

    def GetQueryVector(self):
        return model.encode(self.Query)
    
    
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

filter_title = models.Filter(
    must=[
        models.FieldCondition(
            key="title",
            match=models.MatchText(text="amazing")
        )
    ]
)

#STANFORD_IMDB_NLP

#This query is created by chatgpt considering semantic similarity with point with id 1667 as a consequence, provided closest pointis 1667 with score 0.65
param_imdb = SearchParams(CollectionName= constants.COLLECTION_NAME_IMDB,
                         Query= "Wow, this movie had such a promising start — a bunch of carefree college girls wandering" \
                         " around in barely-there outfits, check. Then we hit a lively 80's-style bar scene where the cheesiness" \
                         " hits full throttle, check. Next morning, off to a forested state park, check. A quirky mix of characters — " \
                         "the girls’ teacher, rowdy bikers, a clueless store clerk, and a local drunk straight out of a cult film — all contributing" \
                         " to a growing body count, check. There’s even a bizarre ritual performed by a wandering eccentric in the woods — I’ll let that slide" \
                         ", check. And then… everything just falls apart. Absolute chaos. That monster head in the lake though? Hilariously bad" \
                         ", had me laughing out loud.",
                         Limit = 4,
                         ScoreThreshold = None,
                         QueryFilter = None)

param_imdb2 = SearchParams(
    CollectionName=constants.COLLECTION_NAME_IMDB,
    Query=(
        "I went into this film with zero expectations, but it really surprised me. "
        "The pacing in the first half was slow, almost dragging at times, but once the mystery "
        "started unfolding, I was hooked. The cinematography is gorgeous — wide shots of the "
        "countryside really set the mood, and the soundtrack matched the tension perfectly. "
        "The lead actor gave a solid performance, though some of the side characters felt "
        "underdeveloped. The ending was bittersweet, leaving just enough ambiguity to keep "
        "me thinking about it afterwards. Not perfect, but definitely worth watching."
    ),
    Limit=6,
    ScoreThreshold= 0.65,
    QueryFilter=filter_negative)

#-------------------------------------------------------------------------------------------------------------------------------------------
#AMAZON_POLARITY

param_amazon_review = SearchParams(
    CollectionName=constants.COLLECTION_NAME_AMAZON,
    Query=(
        "I’ve been using this product for about two weeks and I’m really impressed. "
        "The build quality feels sturdy, and the packaging was neat and secure. "
        "Battery life easily lasts through the day, and the performance is smooth with no lag. "
        "Only downside is that it took a little longer to set up than expected, "
        "but once it was ready, it worked perfectly. Definitely worth the price."
    ),
    Limit=4,
    ScoreThreshold=None,
    QueryFilter=None
)


param_amazon_review2 = SearchParams(
    CollectionName=constants.COLLECTION_NAME_AMAZON,
    Query="The headphones sound great for the price. Clear audio, decent bass, and very comfortable. Only issue is the battery life could be better.",
    Limit=5,
    ScoreThreshold= 0.24,
    QueryFilter=None
)


param_amazon_review3 = SearchParams(
    CollectionName=constants.COLLECTION_NAME_AMAZON,
    Query="This coffee maker is super easy to use and brews quickly. The design is compact and fits nicely on my counter.",
    Limit=5,
    ScoreThreshold=None,
    QueryFilter=filter_positive
)

param_amazon_review4 = SearchParams(
    CollectionName=constants.COLLECTION_NAME_AMAZON,
    Query="Product is great.",
    Limit=5,
    ScoreThreshold=None,
    QueryFilter=filter_title
)
