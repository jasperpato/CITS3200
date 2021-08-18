"""
This is the 'heart' of the program.
Developers need to understand how the pipe_line function works, as this is the main interface that they must use.
"""
from post import Post
from thread import Thread, all_posts
from typing import List, Callable, Tuple
from heapq import nlargest
from nltk import word_tokenize
from utils import pipe, cached
from summarise import cosine_similarity
from itertools import product
from project_types import Tokens

def process_post(       p : Post,
                        cleaners : Tuple[Callable[[str], str]],
                        filters : Tuple[Callable[[str], bool]],
                        substitutes : Tuple[Callable[[str], str]]) -> List[Tokens]:
        """
        Returns a list of tokens.

        This is where the processing of a post's text occurs. The function caller provides, alongside the post in question,
        a tuple of cleaner functions (s.t. forall f in cleaners. f : str -> str), a tuple of filters (s.t. forall f in filters. f : str -> bool),
        and a tuple of substitute functions (s.t. forall f in substitutes. f : str -> str).

        Processing occurs in 4 phases:
                - Cleaner functions are first applied to the post's text (currently just the payload of the post) in a left-to-right fashion.
                - Tokenisation
                - tokens are then filtered out as specified by functions in the filters tuple
                - token for token substitution, in a left-to-right fashion, is then applied to the resulting tokens

        Please ensure the the passed functions are indeed tuples of functions - this is because immutability is required for cacheing.
        """
        return [pipe(*substitutes)(tok) for tok in word_tokenize(pipe(*cleaners)(p.payload)) if any(product(filters,tok))]

#process_cached is simply the process_post function, but with memoisation
process_cached = cached(process_post)

def pipe_line(  post : Post,
                threads : List[Thread],
                cleaners : Tuple[Callable[[str], str]],
                filters : Tuple[Callable[[str], bool]],      # functions that check if a string should be filtered out
                substitutes : Tuple[Callable[[str], str]],   # functions that apply textual substitution
                weights : List[Callable[[Post], float]],    # functions that return a scalar value that scales a post up/down
                n : int) -> List[Post]:
        """
        Returns a list of posts (of length n) that are similar, in descending order of similarity, to the given post.

        This is basically the plumbing of our program. The caller provides a post, all of the threads to be checked against,
        a tuple of cleaner functions (s.t. forall f in cleaners. f : str -> str), a tuple of filters (s.t. forall f in filters. f : str -> bool),
        a tuple of substitute functions (s.t. forall f in substitutes. f : str -> str), a tuple of weight functions (s.t. forall f in weights. f : Post -> float),
        and an integer n that represents how many posts should be returned (needs to be a natural number, specifically).

        Each post in the given threads are checked for similarity with the given post's tokens. Similarity is computed by:
                - processing the threads' posts with the cleaners, filters, and substitutes (applied in that order)
                - cosine similarity takes the post's tokens and the threads' posts' tokens and computes similarity
                - weight functions are then applied
        """
    post_toks = process_post(post,cleaners,filters,substitutes)

    # check similarity between given post and all other posts, and then scale with weights
    post_scores = {p:(pipe(*weights)(p))*(cosine_similarity(post_toks, process_cached(p,cleaners,filters,substitutes))) for p in all_posts(threads)}
    return nlargest(n, post_scores, key=post_scores.get)