from parse_file import *
from post import Post
from thread import Thread
from typing import List

"""
This function takes a new post object and a list of thread objects
and returns a tuple of the n most similar existing posts to the new post.
"""
def find_similar_posts(post : Post, threads : List[Thread], n : int) -> List[Post]:
    return None