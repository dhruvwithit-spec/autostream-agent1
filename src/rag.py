from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.knowledge_base import KnowledgeBase


class LocalRAG:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.documents = [f"{chunk.title}\n{chunk.content}" for chunk in kb.chunks]
        self.matrix = self.vectorizer.fit_transform(self.documents)

    def retrieve(self, query: str, top_k: int = 2) -> str:
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.matrix).flatten()
        top_indices = sims.argsort()[::-1][:top_k]
        selected = [self.documents[i] for i in top_indices if sims[i] > 0]
        return "\n\n".join(selected) if selected else self.documents[0]
