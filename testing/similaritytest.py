from pipeline import process_post, pipeline
import json
from utils import reduce
import Thread
import Post

def test(self):
    space = open("test_space_2019.json")
    case = open("test_case_2019.json")
    threads = json.load(space)
    tests = json.load(case)
    for test_case in tests:
        top = pipeline(parse_thread(threads), parse_post(test_case), 3, False)
        for closest in top:
            tag_of_Post = next((t for t in threads if closest.payload==t.Body).split(" "), None)
            print(tag_of_Post)
            print(test_case.Category)
    pass

def parse_post(post):
    return Post(post.Date, post.Subject, post.body,True)

def parse_thread(thread):
    posts = [parse_post(this_post) for this_post in thread]
    return(Thread(this_post.Subject, posts) for this_post in thread)
   