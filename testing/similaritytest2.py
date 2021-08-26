import json
import datetime
from utils import reduce
from thread import Thread
from post import Post
from string import ascii_letters
import nltk
from re import sub
from pipeline import process_post, pipeline
from parse_file import valid, group
stopwords = nltk.corpus.stopwords.words('english')

def pipeline_test():
    test_space_posts = json.load(open("test_space_2019.json"))["testcases"]
    test_case_posts = json.load(open("test_case_2019.json"))["testcases"]
    substitutes =  (lambda x: x.lower(),                # lowercase all text
                    lambda x: sub(r'\s+', ' ', x))      # remove extraneous spaces and punctuation

    filters =  (lambda x: x not in ascii_letters,       # take non-alphabetical words out
                lambda x: x in stopwords)               # remove stopwords

    weights = [lambda x: 1.5 if x.verified else 1.0]    # give a bit more priority to Chris's posts
    cleaner = [lambda x: x]

    for test_case, i in enumerate(test_case_posts):
        print(f"{i + 1}'th Test Case")
        print(f"Subject: {test_case['Subject']}\n")
        top_posts = pipeline(parse_test_case(test_case), parse_test_space(test_space_posts), cleaner, substitutes, filters, weights, 3)
        target_categories = set(test_case['Category'].split(' '))
        sum = 0
        for post, j in enumerate(top_posts):
            test_space_post = [tp for tp in test_space_posts if tp['Body'] == post.payload][0]
            post_categories = set(test_space_post['Category'].split(' '))
            score = len(target_categories.intersection(post_categories)) / len(target_categories)
            sum += score
            print(f"\t{j + 1}'th Post:") 
            print("Evaluation score: {score}")
            print(f"{post}")
        print(f'Average Score: {sum / len(top_posts)}\n')

def parse_test_case(post):
    return Post(None, post['Subject'], post['Body'], False)

def parse_post(post):
    date = datetime.datetime.strptime(post["Date"], "%a %b %d %H:%M:%S %Y")
    verified = post['From'] in valid
    return Post(date, post['Subject'], post['Body'], verified)

def parse_test_space(test_space_posts):
    posts = [parse_post(post) for post in test_space_posts]
    return group(posts)
   
pipeline_test()