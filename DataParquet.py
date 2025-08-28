from datasets import load_dataset
import pandas as pd
import string
import numpy as np
from pydantic import BaseModel
from ClientClass import ClientService
from loguru import logger
import pyarrow.parquet as pq
from qdrant_client.http import models


class DataParquet(BaseModel):
    path : str
    batch_size : int
    main_column : str


    def preprocess(self) -> pd.DataFrame:

        df = pd.read_parquet(self.path) 
        
        for col in df.select_dtypes(include=['object', 'string']).columns:
            df[col] = df[col].str.lower()

        numeric_cols = df.select_dtypes(include=["number"]).columns

        #Droppping outliers does not make sense for textual data, however it is tested via a financial data.
        for col in numeric_cols:
            # Identify the quartiles
            q1, q3 = np.percentile(df[col], [25, 75])
            # Calculate the interquartile range
            iqr = q3 - q1
            # Calculate the lower and upper bounds
            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)
            # Drop the outliers
            df = df[(df[col] >= lower_bound) 
                    & (df[col] <= upper_bound)]    

        return df

    #This is a generator function which makes task easier, it returns a batch when needed, does not deallocate the AR,
    #it can move on from where it left off.
    def read_parquet_in_batches(self):
        batch_count= 0
        file = pq.ParquetFile(self.path) #Loads metadata, schema, column definitions.
        for batch in file.iter_batches(batch_size = self.batch_size, columns = file.schema.names):
            yield batch.to_pandas() 
            batch_count +=1
            if(batch_count > 10):
                break 

    #Processing and upserting each batch.
    def process_batch(self, client : ClientService, df : pd.DataFrame, CollectionName : str, counter : int):
        
        text = df[self.main_column].tolist()
        #label = df["label"].tolist()
        #lang = df["lang"].tolist()
        
        cols = list(df.columns)
        '''
        payloads = []
        for col in df.columns:
            payloads.append(df[col].tolist())
            '''            
        payloads = [df[col].tolist() for col in cols]

        vectors = {
            #Creating a dictionary in order to be aware of the model used.
            client.model_name: [
            arr.tolist()
            for arr in client.model.encode(
            sentences=text, # piece of data on each iteration
            batch_size=self.batch_size,
            normalize_embeddings=True,
    )
    ]
    }
        data_points = []
        for j in range (len(text)):
            i = 0
            my_dict = {}
            for meta_data in payloads:
                my_dict[cols[i]] = meta_data[j]
                i += 1
            new_point = models.PointStruct(
                id = self.batch_size * counter + j,
                vector = vectors[client.model_name][j],
                payload= my_dict
                )
            
            data_points.append(new_point)
        
        client.Upsert(CollectionName= CollectionName, DataPoints= data_points)
        logger.info(f"Upserted batch {counter}")

    def process_df(self, client : ClientService, CollectionName : str):
        counter = 0 #For batch idx.
        for df in self.read_parquet_in_batches():
            self.process_batch(client, df, CollectionName, counter)
            counter += 1
        logger.info("File is upserted.")

    def print_data(self):
        print(pd.read_parquet(path = self.path))


    
