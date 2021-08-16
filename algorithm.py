from post import Post
from thread import Thread, all_posts
from typing import List, Callable, Tuple
from heapq import nlargest
from nltk import word_tokenize
from utils import pipe, cached
from summarise import cosine_similarity
from itertools import product

# payload is piped through substitution functions, then result is tokenised,
# and resulting tokens are filtered out if they hit any of the given filters
def process_post(p : Post, substitutes : Tuple[Callable[[str], str]], filters : Tuple[Callable[[str], bool]]):
        return list(filter(lambda x: any(product(filters,x)), word_tokenize(pipe(*substitutes)(p.payload))))

# process_post, except memoised so as to avoid recomputation.
#   Reduces query speed by an order of magnitude in some circumstances.
process_cached = cached(process_post)

def pipe_line(  post : Post,
                threads : List[Thread],
                substitutes : Tuple[Callable[[str], str]],   # functions that apply textual substitution
                filters : Tuple[Callable[[str], bool]],      # functions that check if a string should be filtered out
                weights : List[Callable[[Post], float]],    # functions that return a scalar value that scales a post up/down
                n : int) -> List[Post]:

    post_toks = process_post(post, substitutes, filters)

    # check similarity between given post and all other posts, and then scale with weights
    post_scores = {p:(pipe(*weights)(p))*(cosine_similarity(post_toks, process_cached(p,substitutes,filters))) for p in all_posts(threads)}
    return nlargest(n, post_scores, key=post_scores.get)