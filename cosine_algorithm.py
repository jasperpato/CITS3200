from post import Post
from thread import Thread, all_posts
from typing import List
from summarise import cosine_similarity
from heapq import nlargest
from itertools import chain
from tokeniser import preprocess
 
def cosine_algorithm(post : Post, threads : List[Thread], n : int, subject : bool) -> List[Post]:  
    k = (lambda x: x.subject) if subject else (lambda x: x.payload)
    post_scores = {p:cosine_similarity(preprocess(k(post)), preprocess(k(p))) for p in all_posts(threads)}
    return tuple(nlargest(n, post_scores, key=post_scores.get))