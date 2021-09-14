import json
import datetime
import pickle
import numpy as np
import time
import nltk
import os
import sys
from re import sub
from os.path import dirname, join
from string import ascii_letters

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from post import Post
from thread_obj import all_posts
from weights import date_weight, verified_weight
from pipeline import process_post, pipeline
from parse_file import valid, group_into_threads
from algorithms import cosine_similarity, jaccard
from tfidf import tfidf_similarity
from use import use_similarity, load_use_model
#from bert import bert_similarity, load_bert_model


nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')

cleaner =  (lambda x: x.lower(),                # lowercase all text
                    lambda x: sub(r'\s+', ' ', x))      # remove extraneous spaces and punctuation

filters =  (lambda x: x not in ascii_letters,       # take non-alphabetical words out
            lambda x: x in stopwords)               # remove stopwords

weights = (verified_weight, date_weight)
#[lambda x: 1.5 if x.verified else 1.0]    # give a bit more priority to Chris's posts
substitutes = tuple([])


def pipeline_test(algo):
    test_space = json.load(open("testing/test_space_2019.json"))["testcases"]
    test_case_posts = json.load(open("testing/test_case_2019.json"))["testcases"]
    score_sum = 0
    time_sum = 0
    for i, test_case in enumerate(test_case_posts):
        print(f"{i + 1}'th Test Case")
        print(f"Subject: {test_case['Subject']}\n")
        print(f"body: {test_case['Body']}\n")
        print("________________________")
        ###
        algo_result = evaluate_algo(algo, test_case, test_space, test_case['target_count'])
        print(f"Time taken: {algo_result['time']}\n")
        print("________________________")
        ###
        target_categories = set(test_case['Category'].split(' '))
        sum = 0
        for j, post in enumerate(algo_result['top_posts']):
            post_json = [tp for tp in test_space if tp['Body'] == post.payload][0]
            post_categories = set(post_json['Category'].split(' '))
            sum = sum+1 if len(target_categories.intersection(post_categories)) > 0 else sum
            print(f"\t{j + 1}'th Post:") 
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


def tag_intersection_test(algo, n):
    overall_test_space = json.load(open("testing/test_space_2019.json"))["test_space"]
    score_sum = 0
    for case in overall_test_space:
        target_categories = set(case['Tags'].split(' '))
        space = overall_test_space[:]
        space.remove(case)
        algo_result = evaluate_algo(algo, case, space, n)
        sum = 0
        for post in algo_result['top_posts']:
            post_json = [tp for tp in space if tp['Body'] == post.payload][0]
            post_categories = set(post_json['Tags'].split(' '))
            sum += post_categories.intersection(target_categories) / len(target_categories)
        score_sum += sum / n 
    print("<<=====================================>>")
    print(print('FINAL SCORE:', score_sum / len(overall_test_space)))
    print("<<=====================================>>")
            


def evaluate_algo(algo, test_case, test_space, n):
    if algo == 'use':
        load_use_model(use_cpu=True)

    start_time = time.process_time()
    posts = [parse_post(p) for p in test_space]
    post = parse_test_case(test_case)

    if algo == 'basic':
        algs = (cosine_similarity, jaccard)
        top_posts = pipeline(post, parse_test_space(posts), cleaner, filters, substitutes, weights, algs, n)

    elif algo == 'tfidf':
        top_posts = tfidf_similarity(post, posts, n)

    elif algo == 'use':
        f_path = join(dirname(__file__), '../../encodings/use/test_space.pickle')
        with open(f_path, 'rb') as handle:
            encodings = pickle.load(handle)
        top_posts = use_similarity(post, encodings, n)
    return {'top_posts': top_posts, 'time': time.process_time() - start_time}


def parse_test_case(post):
    return Post(None, post['Subject'], post['Body'], False)


def parse_post(post):
    date = datetime.datetime.strptime(post["Date"], "%a %b %d %H:%M:%S %Y")
    verified = post['From'] in valid
    return Post(date, post['Subject'], post['Body'], verified)


def parse_test_space(test_space):
    posts = [parse_post(post) for post in test_space]
    return group_into_threads(posts)


if __name__ == '__main__':   
    pipeline_test('use')
