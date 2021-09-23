from collections import Counter
from math import sqrt
from typing import List, Set, Dict
from utils import merge
from project_types import Tokens, Vector
from post import Post

def dot_product(xs : Vector, ys : Vector) -> float:
    return sum([x*y for (x,y) in zip(xs,ys)])

def norm(xs : Vector) -> float:
    return sqrt(dot_product(xs,xs))

def word_vector(toks : Tokens, words : Set[str]) -> Vector:
    return list(merge({w : 0 for w in words}, Counter(toks)).values())


def bag_of_words(in_toks : Tokens, toks_array : List[Tokens], *kwargs) -> List[float]:
    scores = []
    for i in range(0, len(toks_array)):
        all_words = set(in_toks) | set(toks_array[i])
        A_vec = word_vector(in_toks, all_words)
        B_vec = word_vector(toks_array[i], all_words)
        scores[i] = dot_product(A_vec, B_vec) / (norm(A_vec) * norm(B_vec))
    return scores
    

# calculates (intersection / union) of two sets of tokens
def jaccard(in_toks : Tokens, toks_array : List[Tokens], *kwargs) -> float:
    scores = []
    for i in range(0, len(toks_array)):
        scores[i] = len(set(in_toks) & set(toks_array[i])) / len(set(in_toks) | set(toks_array[i]))
    return scores