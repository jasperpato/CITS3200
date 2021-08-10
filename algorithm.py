from parse_file import *
from post import Post
from thread import Thread
from typing import List
from summarise import cosine_similarity
import heapq
from itertools import chain
from tokeniser import preprocess

"""
This function takes a new post object and a list of thread objects
and returns a tuple of the n most similar existing posts to the new post.
"""

def find_similar_posts(post : Post, threads : List[Thread], n : int, subject : bool) -> List[Post]:
    all_posts = chain(*[t.posts for t in threads])
    k = (lambda x: x.subject) if subject else (lambda x: x.payload)
    post_scores = {p:cosine_similarity(preprocess(k(post)), preprocess(k(p))) for p in all_posts}
    return tuple(heapq.nlargest(n, post_scores, key=post_scores.get))