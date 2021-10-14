from collections import Counter
from math import sqrt
from typing import Set, Dict
from utils import merge
from project_types import Tokens, Vector
from .algorithm import SimilarityAlgorithm

class Cosine(SimilarityAlgorithm):

    def dot_product(self, xs : Vector, ys : Vector) -> float:
        return sum([x*y for (x,y) in zip(xs,ys)])

    def norm(self, xs : Vector) -> float:
        return sqrt(self.dot_product(xs,xs))

    def word_vector(self, toks : Tokens, words : Set[str]) -> Vector:
        return list(merge({w : 0 for w in words}, Counter(toks)).values())

    def similarity(self, in_toks : Tokens, toks_dict : Dict[int, Tokens]) -> Dict[int, float]:
        scores = {}
        for id, toks in toks_dict.items():
            all_words = set(in_toks) | set(toks)
            A_vec = self.word_vector(in_toks, all_words)
            B_vec = self.word_vector(toks, all_words)
            scores[id] = self.dot_product(A_vec, B_vec) / (self.norm(A_vec) * self.norm(B_vec))
        return scores
