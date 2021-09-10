import json
import datetime
import numpy as np
import time
import nltk
import os
from re import sub
from os.path import dirname, join

from post import Post
from thread_obj import all_posts
from string import ascii_letters
from weights import date_weight, verified_weight
from pipeline import process_post, pipeline
from parse_file import valid, group_into_threads
from algorithms import cosine_similarity, jaccard
from tfidf import tfidf_similarity
from use import use_similarity, load_use_model
from bert import bert_similarity, load_bert_model

stopwords = nltk.corpus.stopwords.words('english')

cleaner =  (lambda x: x.lower(),                # lowercase all text
                    lambda x: sub(r'\s+', ' ', x))      # remove extraneous spaces and punctuation

filters =  (lambda x: x not in ascii_letters,       # take non-alphabetical words out
            lambda x: x in stopwords)               # remove stopwords

weights = (verified_weight, date_weight)
#[lambda x: 1.5 if x.verified else 1.0]    # give a bit more priority to Chris's posts
substitutes = tuple([])


def pipeline_test(algo):
    test_space_posts = json.load(open("testing/test_space_2019.json"))["testcases"]
    test_case_posts = json.load(open("testing/test_case_2019.json"))["testcases"]
    score_sum = 0
    time_sum = 0
    for i, test_case in enumerate(test_case_posts):
        print(f"{i + 1}'th Test Case")
        print(f"Subject: {test_case['Subject']}\n")
        print(f"body: {test_case['Body']}\n")
        print("________________________")
        ###
        algo_result = evaluate_algo(algo, test_case, test_space_posts, test_case['target_count'])
        print(f"Time taken: {algo_result['time']}\n")
        print("________________________")
        ###
        target_categories = set(test_case['Category'].split(' '))
        sum = 0
        for j, post in enumerate(algo_result['top_posts']):
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
        score_sum += sum / test_case["target_count"]
        time_sum += algo_result['time']
        print(f'Total matches identified:{sum}\n')
        print(f'Number of targets existing:{test_case["target_count"]}\n')
        print(f'Recall: {sum / test_case["target_count"]}\n')
        print("<<=====================================>>")
    print('FINAL SCORE:', score_sum / len(test_case_posts))
    print('AVERAGE_ALGO_TIME:', time_sum / len(test_case_posts))
    print("<<=====================================>>\n")


def evaluate_algo(algo, test_case, test_space_posts, n):
    if algo == 'use':
        load_use_model(use_cpu=True)
    elif algo == 'bert':
        load_bert_model(use_cpu=True)

    start_time = time.process_time()
    posts = [parse_post(p) for p in test_space_posts]
    post = parse_test_case(test_case)
    if algo == 'basic':
        algs = (cosine_similarity, jaccard)
        top_posts = pipeline(post, parse_test_space(posts), cleaner, filters, substitutes, weights, algs, n)
    elif algo == 'tfidf':
        top_posts = tfidf_similarity(post, posts, n)
    elif algo == 'use':
        encoded_posts = np.load(join(dirname(__file__), '../../encodings/use/test_space.npy'))
        top_posts = use_similarity(post, encoded_posts, posts, n)
    elif algo == 'bert':
        encoded_posts = np.load(join(dirname(__file__), '../../encodings/bert/test_space.npy'))
        top_posts = bert_similarity(post, encoded_posts, posts, n)
    return {'top_posts': top_posts, 'time': time.process_time() - start_time}


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
    pipeline_test('use')
