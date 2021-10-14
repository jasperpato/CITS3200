"""
Class code to run TFIDF
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os, sys
from typing import Dict
from project_types import Tokens

from .algorithm import SimilarityAlgorithm

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

class Tfidf(SimilarityAlgorithm):
    vectorizer = None

    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def similarity(self, in_toks : Tokens, toks_dict : Dict[int, Tokens]) -> Dict[int, float]:
        in_text = ''.join(in_toks) 
        document_list = [''.join(toks) for key, toks in toks_dict.items()]
        document_list.insert(0, in_text)
        embeddings = self.vectorizer.fit_transform(document_list)
        # This is to transform the numpy to a dict, otherwise the data is useless
        # Might be a wrong implementation, since this is assuming the 1st entry corresponds to first post etc..
        scores = dict(enumerate(cosine_similarity(embeddings[0], embeddings[1:]).flatten(),0)) 
        return scores