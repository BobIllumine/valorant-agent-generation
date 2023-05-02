import os

import numpy as np
import openai
import pandas as pd

import embeddings


class CharacterGenerator:
    MAX_SECTION_LEN = 2500
    SEPARATOR = "\n* "
    SEPARATOR_LEN = 3

    def __init__(self, api_key: str, embedder: embeddings.Embedder,
                 model: str = 'text-davinci-003'):
        openai.api_key = api_key
        self.embedder = embedder
        self.model = model
        self.history = pd.read_csv('history.csv') if os.path.exists('history.csv') else pd.DataFrame([], columns=['prompt', 'response'])

    @staticmethod
    def _vector_similarity(x: list[float], y: list[float]) -> float:
        """
        We use dot product to calculate the similarity between vectors.
        """
        return np.dot(np.array(x), np.array(y))

    def _order_docs(self, query: str) -> list[tuple[float, tuple[str, str]]]:
        query_embedding = self.embedder.get_query_embedding(query)

        document_similarities = sorted([
            (CharacterGenerator._vector_similarity(query_embedding, doc_embedding), doc_index)
            for doc_index, doc_embedding in
            self.embedder.context_embeddings.items()
        ], reverse=True)

        return document_similarities

    def __call__(self, query: str, context: pd.DataFrame, **prompt_kwargs) -> str:
        top_rel = self._order_docs(query)
        sections, sec_len, = [], 0
        for _, section_index in top_rel:
            # Add contexts until we run out of space.
            doc_section = context.loc[section_index]
            if sec_len + doc_section.tokens.sum() + CharacterGenerator.SEPARATOR_LEN > CharacterGenerator.MAX_SECTION_LEN:
                continue
            sec_len += doc_section.tokens.sum() + CharacterGenerator.SEPARATOR_LEN

            sections.append(CharacterGenerator.SEPARATOR + doc_section.content.replace("\n", " "))

        header = 'Generate a new Valorant with the given traits. ' \
                 'Give name, role, lore (how they ended up in Valorant), ' \
                 'abilities (C, Q, E, X. be creative, but make them fit into Valorant\'s meta), ' \
                 'appearance (make it more interesting) and ' \
                 'relationships with other agents (maximum three, be creative)'\
                 'Use the given context as a reference but do not copy it. \n\nContext:\n'

        fmt = """\n\n Use the following format for your answer. 
                Name: 
                Codename: 
                Role: 
                Appearance:
                Biography:
                Personality: 
                Abilities:
                C - 
                Q - 
                E - 
                X - 
                Relationships:"""
        prompt = header + "".join(sections) + fmt + "\n\n Traits: " + query + "\n A:"
        response = openai.Completion.create(
            model=self.model,
            prompt=prompt,
            **prompt_kwargs
        )
        self.history = self.history.append({'prompt': query, 'response': response.choices[0].text}, ignore_index=True)
        self.history.to_csv('history.csv', index=False)
        return response.choices[0].text
