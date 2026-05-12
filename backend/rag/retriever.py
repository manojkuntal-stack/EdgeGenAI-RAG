from .embedding import EmbeddingModel
from .vector_store import VectorStore


class Retriever:

    def __init__(self, docs):

        self.docs = docs

        self.embedder = EmbeddingModel()

        # Create embeddings
        embeddings = self.embedder.encode(docs)

        # Create vector store
        self.store = VectorStore(embeddings.shape[1])

        # Add documents
        self.store.add(embeddings, docs)

    def retrieve(self, query, k=5):

        # Encode query
        q_emb = self.embedder.encode(query)

        # Search top documents
        results = self.store.search(q_emb, k=k)

        return results

    def get_context(self, query, k=5):

        retrieved_docs = self.retrieve(query, k)

        # Combine retrieved chunks
        context = "\n\n".join(retrieved_docs)

        return context