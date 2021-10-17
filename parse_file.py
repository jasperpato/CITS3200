"""
This script goes through a text file containing the posts of a given year, converts 
all the posts in Post class object, groups the ones with the same subject into threads
and returns the final list of posts and threads.
"""

import email
import datetime
from itertools import groupby
from post import Post
from thread_obj import Thread
from typing import List

# expand this with other demonstrators emails or those who you want
# their post to appear more frequently
valid = set(["chris.mcdonald@uwa.edu.au"])

def parse_post(id : int, post_str : str) -> Post:
    """
    Returns a Post object given a string representation of a post.

    Post follows rfc2822 spec - see http://www.faqs.org/rfcs/rfc2822.html
    """ 
    message = email.message_from_string(post_str)
    header = dict(message)

    date = datetime.datetime.strptime(header["Date"], "%a %b %d %H:%M:%S %Y")
    subject = header["Subject"]
    payload = message.get_payload().strip()
    verified = header["From"] in valid

    return Post(id,date,subject,payload,verified)

def group_into_threads(posts : List[Post]) -> List[Thread]:
    """
    Returns a list of threads given a list of posts.

    Posts are in ascending order by date, so we sort them by subject
    and then group all of the Post objects with the same subject into
    threads.
    """
    sub = lambda x: x.subject
    return [Thread(subject, list(posts)) for subject, posts in
                    groupby(sorted(posts, key = sub), key = sub)]

def parse_file(filename : str) -> List[Thread]:
    """
    Returns a list of Thread objects.

    Each file is a dump of posts, which is parsed into a list of Thread
    objects.
    """
    with open(filename, 'r') as file:
        s = file.read()
        post_strings = ["Date: " + x for x in s.split("Date: ")][1:]
        posts = [parse_post(id, s) for id, s in enumerate(post_strings)]
        
    return posts