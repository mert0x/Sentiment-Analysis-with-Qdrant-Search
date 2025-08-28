## Semantic Search & Recommendation Engine with Qdrant
This project is a comprehensive implementation of a semantic search and recommendation system using the Qdrant vector database. It is designed to process large datasets, generate vector embeddings, and perform fast, accurate similarity searches and recommendations. The application is built with a modular, configurable, and scalable architecture, demonstrating best practices in modern data science and software engineering.

# Project Overview
The core of this project is to transform raw text data into meaningful numerical representations (vector embeddings) and index them in a high-performance vector database. This allows for querying the database not just based on keywords, but on the semantic meaning of the text. The system is capable of handling multiple datasets (IMDB reviews, Amazon reviews) and provides a flexible framework for searching and recommending similar items.

# Key Technologies
Qdrant: An open-source vector database and similarity search engine used for storing, indexing, and searching vector embeddings.

SentenceTransformers: A Python framework for state-of-the-art sentence, text, and image embeddings. The all-MiniLM-L6-v2 model is used to generate 384-dimensional vectors.

Pydantic: A data validation library used to create robust and type-safe configuration models for the Qdrant client and search/recommendation parameters.

PyArrow & Pandas: Used for efficient reading and processing of data from Parquet files in memory-friendly batches.

Loguru: For simple and effective logging throughout the application.

Poetry: For managing project dependencies and packaging.

Features
Modular Architecture: The code is organized into distinct classes and modules for clarity and maintainability (e.g., ClientClass.py, DataParquet.py).

Configurable Qdrant Client: The ClientClass allows for easy configuration of Qdrant settings, including advanced features like vector quantization (Scalar & Binary) and payload indexing.

Efficient Data Pipeline: The DataParquet class reads large Parquet files in batches using a generator, preventing memory overload and ensuring scalability.

Semantic Search: Implements similarity search to find data points that are semantically closest to a given text query.

Recommendation Engine: Provides content-based recommendations using positive and negative examples to refine results.

Support for Multiple Datasets: The project includes separate entry points (main_imdb.py, main_amazon.py) to process and query different datasets independently.

Advanced Filtering: Allows for filtering search and recommendation results based on metadata (payloads), such as sentiment labels or keywords in titles.

# Setup and Installation
Follow these steps to set up and run the project locally.

1. Prerequisites
Docker: Qdrant runs in a Docker container. Make sure you have Docker installed and running.

Python 3.9+: The project is configured to use Python 3.9 or higher.

Poetry: For managing dependencies. If you don't have it, install it with pip install poetry.

2. Run Qdrant
Start the Qdrant vector database using Docker with the following command in your terminal:

```docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant```

3. Clone & Install Dependencies

Clone this repository and install the required Python packages using Poetry.

```git clone https://github.com/mert0x/Sentiment-Analysis-with-Qdrant-Search```

```cd Sentiment-Analysis-with-Qdrant-Search```

Install dependencies from pyproject.toml

``` poetry install ```

# Usage
The project's architecture is designed to be generic and adaptable to various datasets. The core logic for connecting to Qdrant, processing data, and performing queries is encapsulated in reusable classes (ClientClass.py, DataParquet.py).

The main_imdb.py and main_amazon.py scripts serve as concrete examples of how to use this generic workflow. They handle the end-to-end process for their respective datasets: initializing the client with specific configurations, processing the data, and running a series of pre-defined example queries.

Running the Example Pipelines
To run the end-to-end pipeline for a specific dataset, execute its main script:

For the IMDB dataset:

```poetry run python main_imdb.py```

For the Amazon dataset:

```poetry run python main_amazon.py```

The scripts will print the results of the search and recommendation queries to the console. To experiment with your own queries, you can modify the pre-defined objects in SearchParams.py and RecommendParams.py or create new ones.

# Project Structure Explained
Here is a breakdown of the key files and their roles:

pyproject.toml: Defines all project dependencies and metadata, managed by Poetry.

constants.py: Centralizes constant values like collection names, file paths, and model names for easy configuration.

ClientClass.py: A powerful, Pydantic-based class that encapsulates all interactions with the Qdrant client. It handles collection creation, vector upserting, searching, and recommending, with support for advanced configurations like quantization.

DataParquet.py: Manages the data ingestion pipeline. Its primary role is to read Parquet files efficiently in batches, process the text, generate embeddings, and upsert the data points (vectors + payloads) into Qdrant.

SearchParams.py / RecommendParams.py: Pydantic models that define the structure for search and recommendation queries. This makes the code clean and type-safe, and allows for pre-defining complex queries for different datasets.

main_imdb.py / main_amazon.py: These are the main entry points for running the end-to-end process for the IMDB and Amazon datasets, respectively. They initialize the client, process the data, and execute a series of search and recommendation examples.

main.py: A general-purpose file, likely used for initial development and testing of various functionalities.

This modular structure makes the project easy to understand, maintain, and extend with new datasets or features.
