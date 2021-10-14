"""
This is the 'heart' of the program. Developers need to understand how the
pipeline function works, as this is the main interface that they must use.
"""
import numpy as np

from post import Post
from thread_obj import Thread, all_posts
from typing import List, Callable, Tuple
from heapq import nlargest
from nltk import word_tokenize
from utils import pipe, cached, pipe_weight
from itertools import product
from project_types import Tokens
from spell_correction_pysc import spell_correction
from spellchecker import SpellChecker

def process_post(p : Post,
                 cleaners : Tuple[Callable[[str], str]],
                 filters : Tuple[Callable[[str], bool]],
                 substitutes : Tuple[Callable[[str], str]],
                 subject : bool) -> List[Tokens]:
        """
        Returns a list of tokens.

        This is where the processing of a post's text occurs. The function
        caller provides, alongside the post in question, a tuple of cleaner
        functions (s.t. forall f in cleaners. f : str -> str), a tuple of
        filters (s.t. forall f in filters. f : str -> bool), and a tuple of
        substitute functions (s.t. forall f in substitutes. f : str -> str).

        Processing occurs in 4 phases:
        - Cleaner functions are first applied to the post's text (currently just
          the payload of the post) in a left-to-right fashion.
        - Tokenisation
        - tokens are then filtered out as specified by functions in the filters
          tuple
        - token for token substitution, in a left-to-right fashion, is then
          applied to the resulting tokens

        Please ensure the the passed functions are indeed tuples of functions -
        this is because immutability is required for cacheing.
        """
        text = p.subject if subject else p.payload
        return [pipe(*substitutes)(tok) for tok in word_tokenize(pipe(*cleaners)(text)) if any(product(filters,tok))]

#process_cached is simply the process_post function, but with memoisation
process_cached = cached(process_post)

def pipeline(post : Post,
             threads : List[Thread],
             cleaners : Tuple[Callable[[str], str]],
             filters : Tuple[Callable[[str], bool]], # check if string should be filtered out
             substitutes : Tuple[Callable[[str], str]], # apply textual substitution
             weights : List[Callable[[Post], float]], # return a value that scales a post's similarity
             algorithms : Tuple[Callable[[Tokens, Tokens], float]], # determines similarity between two posts
             w : float, # weight of subject to subject similarity, between 0.0 and 1.0
             n : int) -> List[Post]:
        """
        Returns a list of posts (of length n) that are similar, in descending
        order of similarity, to the given post.

        This is basically the plumbing of our program. The caller provides a
        post, all of the threads to be checked against, a tuple of cleaner
        functions (s.t. forall f in cleaners. f : str -> str), a tuple of
        filters (s.t. forall f in filters. f : str -> bool), a tuple of
        substitute functions (s.t. forall f in substitutes. f : str -> str), a
        tuple of weight functions (s.t. forall f in weights. f : Post -> float),
        and an integer n that represents how many posts should be returned
        (needs to be a natural number, specifically).

        Each post in the given threads are checked for similarity with the given
        post's tokens. Similarity is computed by:
        - processing the threads' posts with the cleaners, filters, and
          substitutes (applied in that order)
        - cosine similarity takes the post's tokens and the threads' posts'
          tokens and computes similarity
        - weight functions are then applied
        """
        spell = SpellChecker() #This part will take a while each time it is being run
        post.subject = spell_correction(post.subject,spell)
        post.payload = spell_correction(post.payload,spell)
        in_subject_toks = process_post(post, cleaners, filters, substitutes, True)
        in_payload_toks = process_post(post, cleaners, filters, substitutes, False)
        posts = all_posts(threads)
        similarities = {}

        all_subject_toks = [process_cached(p, cleaners, filters, substitutes, True) for p in posts]
        subject_similarities = np.mean([list(alg(in_subject_toks, all_subject_toks).values()) for alg in algorithms], axis=0)
        all_payload_toks =  [process_cached(p, cleaners, filters, substitutes, False) for p in posts]
        payload_similarities = np.mean([alg(in_payload_toks, all_payload_toks) for alg in algorithms], axis=0)

        for i, p in enumerate(posts):
          similarities[p] = pipe_weight(p,*weights) * (w * subject_similarities[i] + (1.0-w) * payload_similarities[i])
        
        return nlargest(n, similarities, key=similarities.get)
