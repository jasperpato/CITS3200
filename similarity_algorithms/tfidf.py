from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from heapq import nlargest
import os, sys
from typing import Dict
from project_types import Tokens

from algorithm import SimilarityAlgorithm

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

class Tfidf(SimilarityAlgorithm):
    vectorizer = None

    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def similarity(self, in_toks : Tokens, toks_dict : Dict[int, Tokens]) -> Dict[int, float]:
        in_text = ''.join(in_toks) 
        document_list = [''.join(toks) for toks in toks_dict]
        document_list.insert(0, in_text)
        embeddings = self.vectorizer.fit_transform(document_list)
        scores = cosine_similarity(embeddings[0], embeddings[1:]).flatten()
        return scores