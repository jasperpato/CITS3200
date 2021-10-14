from typing import Dict
from project_types import Tokens
from algorithm import SimilarityAlgorithm

class Jaccard(SimilarityAlgorithm):

    def similarity(self, in_toks : Tokens, toks_dict : Dict[int, Tokens]) -> Dict[int, float]:
        scores = {}
        for id, toks in toks_dict.items():
            scores[id] = len(set(in_toks) & set(toks)) / len(set(in_toks) | set(toks))
        return scores
        #return {id: len(set(in_toks) & set(toks)) / len(set(in_toks) | set(toks)) for id, toks in toks_array.items()}