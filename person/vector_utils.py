import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def create_person_vectors(persons):
    texts = [f"{p.first_name} {p.last_name} {p.email}" for p in persons]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts).toarray()
    return vectors, vectorizer


def index_person_vectors(vectors):
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)  # Use L2 distance for similarity
    index.add(vectors)
    return index
