"""
This script contains the functions to run jaccard and cosine similarity algorithm.
The main functions are the cosine_similarity function and the jaccard function.
"""
from collections import Counter
from math import sqrt
from typing import List, Set
from utils import merge
from project_types import Tokens, Vector

def dot_product(xs : Vector, ys : Vector) -> float:
    return sum([x*y for (x,y) in zip(xs,ys)])

def norm(xs : Vector) -> float:
    return sqrt(dot_product(xs,xs))

def word_vector(toks : Tokens, words : Set[str]) -> Vector:
    return list(merge({w : 0 for w in words}, Counter(toks)).values())

# uses the angle between the 2 posts to denote how similiar they are
# The smaller the angle between them are, the higher the score
def cosine_similarity(A : Tokens, B : Tokens) -> float:
    if(len(A) == 0 or len(B) == 0):
        return 0.0
    all_words = set(A) | set(B)
    A_vec = word_vector(A, all_words)
    B_vec = word_vector(B, all_words)
    return dot_product(A_vec, B_vec) / (norm(A_vec) * norm(B_vec))

# calculates (intersection / union) of two sets of tokens
def jaccard(A : Tokens, B : Tokens) -> float:
    if(len(A) == 0 or len(B) == 0):
        return 0.0
    return len(set(A) & set(B)) / len(set(A) | set(B))
