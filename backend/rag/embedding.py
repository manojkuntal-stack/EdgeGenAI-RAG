from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingModel:
    def __init__(self):
        # Better lightweight embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def encode(self, texts):
        """
        Convert text or list of texts into embeddings
        """

        # If single string → convert to list
        if isinstance(texts, str):
            texts = [texts]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings


def cosine_similarity(a, b):
    """
    Compute cosine similarity between two vectors
    """

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))