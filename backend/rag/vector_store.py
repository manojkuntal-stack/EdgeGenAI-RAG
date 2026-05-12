import faiss
import numpy as np


class VectorStore:

    def __init__(self, dim):

        self.dim = dim

        # Cosine similarity style search
        self.index = faiss.IndexFlatIP(dim)

        self.documents = []

    def add(self, embeddings, docs):

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        # Normalize embeddings
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)

        self.documents.extend(docs)

    def search(self, query_embedding, k=5):

        query_embedding = np.array(
            query_embedding,
            dtype=np.float32
        )

        # Normalize query
        faiss.normalize_L2(query_embedding)

        distances, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.documents):

                results.append(
                    self.documents[idx]
                )

        return results