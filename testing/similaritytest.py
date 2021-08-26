from pipeline import process_post, pipeline
import json
from utils import reduce
from thread import Thread
from post import Post
from string import ascii_letters
import nltk
from re import sub
stopwords = nltk.corpus.stopwords.words('english')

def test():
    space = open("test_space_2019.json")
    case = open("test_case_2019.json")
    threads = json.load(space)
    tests = json.load(case)
    substitutes = ( lambda x: x.lower(),                # lowercase all text
                    lambda x: sub(r'\s+', ' ', x))      # remove extraneous spaces

    filters = (  lambda x: x not in ascii_letters,       # take non-alphabetical words out
                lambda x: x in stopwords)               # remove stopwords

    weights = [ lambda x: 1.5 if x.verified else 1.0]   # give a bit more priority to Chris' posts
    cleaner = [lambda x:x]

    for test_case in tests["testcases"]:
        print(test_case['Subject'])
        print('\n')
        top = pipeline(parse_post(dict(test_case)),parse_thread(threads),cleaner, substitutes, filters, weights, 3)
        for closest in top:
            tag_of_Post = next((t for t in threads if closest.payload==t.Body).split(" "), None)
            print(tag_of_Post)
            print(test_case.Category)
    pass

def parse_post(post):
    return Post("Wed Oct  9 17:02:25 2019", post['Subject'], post['Body'],True)

def parse_thread(thread):
    posts = [parse_post(this_post) for this_post in thread['testcases']]
    return(Thread(this_post['Subject'], posts) for this_post in thread['testcases'])
   
test()