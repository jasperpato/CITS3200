import json
import datetime
from os.path import dirname, join
import numpy as np

from post import Post
from string import ascii_letters
from weights import date_weight, verified_weight
import nltk
from re import sub
from pipeline import pipeline
from parse_file import valid, group_into_threads
from algorithms import cosine_similarity, jaccard
from USE import encoder, similarity_function_USE
stopwords = nltk.corpus.stopwords.words('english')


def pipeline_test():
    test_space_posts = json.load(open("testing/test_space_2019.json"))["testcases"]
    test_case_posts = json.load(open("testing/test_case_2019.json"))["testcases"]
    cleaner =  (lambda x: x.lower(),                # lowercase all text
                    lambda x: sub(r'\s+', ' ', x))      # remove extraneous spaces and punctuation

    filters =  (lambda x: x not in ascii_letters,       # take non-alphabetical words out
                lambda x: x in stopwords)               # remove stopwords

    weights = (verified_weight,date_weight)
    #[lambda x: 1.5 if x.verified else 1.0]    # give a bit more priority to Chris's posts
    substitutes = tuple([])
    alg = (cosine_similarity, jaccard)
    total_sum = 0
    for i, test_case in enumerate(test_case_posts):
        print(f"{i + 1}'th Test Case")
        print(f"Subject: {test_case['Subject']}\n")
        print(f"body: {test_case['Body']}\n")
        print("________________________")
        ###
        top_posts = pipeline(parse_test_case(test_case), parse_test_space(test_space_posts), cleaner, filters, substitutes, weights, alg, test_case["target_count"])
        ###
        target_categories = set(test_case['Category'].split(' '))
        sum = 0
        for j, post in enumerate(top_posts):
            test_space_post = [tp for tp in test_space_posts if tp['Body'] == post.payload][0]
            post_categories = set(test_space_post['Category'].split(' '))
            sum = sum+1 if len(target_categories.intersection(post_categories)) > 0 else sum
            #score = len(target_categories.intersection(post_categories)) / len(target_categories)
            print(f"\t{j + 1}'th Post:") 
            #print(f"Evaluation score: {score}")
            print(f"post category: {post_categories}\n")
            print(f"target category: {target_categories}\n")
            print(f"{post}")
            print("________________________")
        total_sum += sum / test_case["target_count"]
        print(f'Total case identified:{sum}\n')
        print(f'Target existing:{test_case["target_count"]}\n')
        print(f'Recall: {sum / test_case["target_count"]}\n')
        print("<<=====================================>>")
    print('FINAL SCORE:', total_sum / len(test_case_posts))
    print("<<=====================================>>\n")


def encoder_test():
    print('\n\n')
    test_space_posts = json.load(open("testing/test_space_2019.json"))["testcases"]
    test_case_posts = json.load(open("testing/test_case_2019.json"))["testcases"]  
    encoded_posts = np.load(join(dirname(__file__), '../../encodings/test_space.npy'))
    total_sum = 0
    for i, test_case in enumerate(test_case_posts):
        print(f"{i + 1}'th Test Case")
        print(f"Subject: {test_case['Subject']}\n")
        print(f"body: {test_case['Body']}\n")
        print("________________________")
        ###
        top_posts = similarity_function_USE(parse_test_case(test_case), encoded_posts, [parse_post(post) for post in test_space_posts], 4, encoder)
        ###
        target_categories = set(test_case['Category'].split(' '))
        sum = 0
        for j, post in enumerate(top_posts):
            test_space_post = [tp for tp in test_space_posts if tp['Body'] == post.payload][0]
            post_categories = set(test_space_post['Category'].split(' '))
            sum = sum+1 if len(target_categories.intersection(post_categories)) > 0 else sum
            #score = len(target_categories.intersection(post_categories)) / len(target_categories)
            print(f"\t{j + 1}'th Post:") 
            #print(f"Evaluation score: {score}")
            print(f"post category: {post_categories}\n")
            print(f"target category: {target_categories}\n")
            print(f"{post}")
            print("________________________")
        total_sum += sum / test_case["target_count"]
        print(f'Total case identified:{sum}\n')
        print(f'Target existing:{test_case["target_count"]}\n')
        print(f'Recall: {sum / test_case["target_count"]}\n')
        print("<<=====================================>>")
    print('FINAL SCORE:', total_sum / len(test_case_posts))
    print("<<=====================================>>\n")


def parse_test_case(post):
    return Post(None, post['Subject'], post['Body'], False)


def parse_post(post):
    date = datetime.datetime.strptime(post["Date"], "%a %b %d %H:%M:%S %Y")
    verified = post['From'] in valid
    return Post(date, post['Subject'], post['Body'], verified)


def parse_test_space(test_space_posts):
    posts = [parse_post(post) for post in test_space_posts]
    return group_into_threads(posts)


if __name__ == '__main__':   
    #pipeline_test()
    encoder_test()