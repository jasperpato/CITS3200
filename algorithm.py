from post import Post
from thread import Thread, all_posts
from typing import List, Callable, Tuple
from heapq import nlargest
from nltk import word_tokenize
from utils import pipe, cached
from summarise import cosine_similarity
from itertools import product

# clean and tokenize the text, filter out specified tokens, and then apply substitutions to the tokens
def process_post(p : Post, cleaners : Tuple[Callable[[str], str]], filters : Tuple[Callable[[str], bool]], substitutes : Tuple[Callable[[str], str]]):
        return [pipe(*substitutes)(tok) for tok in word_tokenize(pipe(*cleaners)(p.payload)) if any(product(filters,tok))]

# process_post, except memoised so as to avoid recomputation.
#   Reduces query speed by an order of magnitude in some circumstances.
process_cached = cached(process_post)

def pipe_line(  post : Post,
                threads : List[Thread],
                cleaners : Tuple[Callable[[str], str]],
                filters : Tuple[Callable[[str], bool]],      # functions that check if a string should be filtered out
                substitutes : Tuple[Callable[[str], str]],   # functions that apply textual substitution
                weights : List[Callable[[Post], float]],    # functions that return a scalar value that scales a post up/down
                n : int) -> List[Post]:

    post_toks = process_post(post,cleaners,filters,substitutes)

    # check similarity between given post and all other posts, and then scale with weights
    post_scores = {p:(pipe(*weights)(p))*(cosine_similarity(post_toks, process_cached(p,cleaners,filters,substitutes))) for p in all_posts(threads)}
    return nlargest(n, post_scores, key=post_scores.get)