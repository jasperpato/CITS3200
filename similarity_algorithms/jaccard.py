from typing import List
from project_types import Tokens

# calculates (intersection / union) of two sets of tokens
def jaccard_similarity(in_toks : Tokens, toks_array : List[Tokens], **kwargs) -> List[float]:
    scores = []
    for i in range(0, len(toks_array)):
        scores.append(len(set(in_toks) & set(toks_array[i])) / len(set(in_toks) | set(toks_array[i])))
    return scores