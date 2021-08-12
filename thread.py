from typing import List
from post import Post
from itertools import chain

class Thread:
    def __init__(self, subject : str, posts : List[Post]):
        self.subject = subject
        self.posts = posts
        
    def __str__(self):
        thread_str = ""
        for p in self.posts:
            thread_str += str(p)
            if p is not self.posts[-1]:
                thread_str += '\n'
        return thread_str

def all_posts(threads : List[Thread]) -> List[Post]:
    return list(chain(*[t.posts for t in threads]))