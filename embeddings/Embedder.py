import json

import openai
import numpy as np
from time import sleep

import pandas as pd


class Embedder:
    def __init__(self, api_key: str, model: str = 'curie'):
        openai.api_key = api_key
        self.EMBEDDING_MODEL = model
        self.DOC_EMBEDDING_MODEL = f'text-search-{model}-doc-001'
        self.QUERY_EMBEDDING_MODEL = f'text-search-{model}-query-001'
        self.doc_cache = open('doc_cache.json', 'a+')
        self.query_cache = open('query_cache.json', 'a+')
        self.doc_dict = json.loads(self.doc_cache.read()) if self.doc_cache.read() != '' else dict()
        self.query_dict = json.loads(self.query_cache.read()) if self.query_cache.read() != '' else dict()
        self.context_embeddings: dict[tuple[str, str], list[float]] = {}

    def get_doc_embedding(self, text: str):
        if self.doc_cache.read() != '':
            self.doc_dict = json.loads(self.doc_cache.read())
        sleep(0.2)
        if self.doc_dict.get(text) is None:
            result = openai.Embedding.create(
                model=self.DOC_EMBEDDING_MODEL,
                input=text)["data"][0]["embedding"]
            self.doc_dict[text] = result
        json.dump(self.doc_dict, self.doc_cache)
        return self.doc_dict[text]

    def get_query_embedding(self, text: str):
        if self.query_cache.read() != '':
            self.query_dict = json.loads(self.query_cache.read())
        sleep(0.2)
        if self.query_dict.get(text) is None:
            result = openai.Embedding.create(
                model=self.QUERY_EMBEDDING_MODEL,
                input=text)["data"][0]["embedding"]
            self.query_dict[text] = result
        json.dump(self.query_dict, self.query_cache)
        return self.query_dict[text]

    def compute_doc_embeddings(self, df: pd.DataFrame) -> dict[tuple[str, str], list[float]]:
        """
        Create an embedding for each row in the dataframe using the OpenAI Embeddings API.

        Return a dictionary that maps between each embedding vector and the index of the row that it corresponds to.
        """
        result = {
            idx: self.get_doc_embedding(r.content.replace("\n", " ")) for idx, r in df.iterrows()
        }
        df = pd.DataFrame().from_dict(result, orient='index')
        df.to_csv('embeddings.csv', header=True, index=False)
        self.context_embeddings = result
        return result

    def load_embeddings(self, fname: str) -> dict[tuple[str, str], list[float]]:
        """
        Read the document embeddings and their keys from a CSV.

        fname is the path to a CSV with exactly these named columns:
            "title", "heading", "0", "1", ... up to the length of the embedding vectors.
        """
        df = pd.read_csv(fname, header=0, index_col='Unnamed: 0')
        max_dim = max([int(c) for c in df.columns if c != "title" and c != "heading"])
        result = {
            eval(_): [r[str(i)] for i in range(max_dim + 1)] for _, r in df.iterrows()
        }
        self.context_embeddings = result
        return result

    def __del__(self):
        self.doc_cache.close()
        self.query_cache.close()