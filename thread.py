from typing import List
from post import Post
from itertools import chain
from collections import Counter

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
    """
    Returns all of the posts in a list of threads
    """
    return list(chain(*[t.posts for t in threads]))

# debug
def print_threads(threads : List[Thread]) -> None:
    for num, t in enumerate(threads):
        title = " Thread " + str(num) + ' '
        spaces = '-' * ((60 - len(title)) // 2)
        print("\n\n" + spaces + title + spaces + '\n')
        print(str(t))
        print('-' * 60 + '\n')