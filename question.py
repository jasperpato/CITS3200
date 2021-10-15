from re import sub
from post import Post
from utils import to_lower, remove_stopwords, remove_non_alphabet
from pipeline import pipeline
from weights import verified_weight, date_weight
from spell_correction_pysc import spell_correction
from similarity_algorithms.tfidf import Tfidf
from similarity_algorithms.use import Use
from similarity_algorithms.jaccard import Jaccard
from similarity_algorithms.cosine import Cosine
from parse_file import parse_file
from datetime import datetime
from uuid import uuid4
import json
import os

currentdir = os.path.dirname(__file__)

tfidf = None
use = None


def encapsulate(test_cases):
    list_of_tup = [] 
    cleaners = [to_lower, lambda x: sub(r'\s+', ' ', x)]
    filters = [remove_non_alphabet, remove_stopwords]
    substitutes = []
    weight = [date_weight, verified_weight]
    files = ['help2002-2021.txt']
    all_threads = [parse_file(f) for f in files]
    threads = all_threads[0]
    for i, case in enumerate(test_cases):
        date = datetime.strptime("2019-07-28 16:54:49", "%Y-%m-%d %H:%M:%S")
        post = Post(uuid4(),  date, case['Subject'], case['Body'], False)
        pruned_threads = [t for t in threads if t.subject != post.subject]
        list_of_tup.append(tuple(generate_post(post, pruned_threads, cleaners, filters, substitutes, weight, 10, i % 4)))
    return list_of_tup, test_cases

def generate_post(post, threads, cleaners, filters, substitutes, weights, nposts, start_algo):
    jaccard_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [jaccard.similarity],0.2, nposts)
    bag_of_words_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [cosine.similarity],0.2, nposts)
    tfidf_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [tfidf.similarity],0.2, nposts)
    use_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [use.similarity],0.2, nposts)
    list_of_posts = [bag_of_words_posts, jaccard_posts, tfidf_posts, use_posts]
    diff_posts = return_best_posts(list_of_posts)
    return diff_posts

def find_diff_posts(algo_results, start_index):
    out_posts = []
    ind = (start_index + 1) % 4
    out_posts.append(algo_results[ind][0])
    while ind != start_index:
        ind = (ind + 1) % 4
        similar_posts = algo_results[ind]
        for post in similar_posts:
            if post in out_posts:
                continue
            else:
                out_posts.append(post)
                break
    return out_posts

def return_best_posts(algo_results):
    out_posts = []
    for posts in algo_results:
        out_posts.append(posts[0])
    return out_posts

out_file = open('google_docs_case_dump.txt', 'w')
tfidf = Tfidf()
use = Use(os.path.join(currentdir, "../pretrained_models/universal-sentence-encoder_4/"))
jaccard = Jaccard()
cosine = Cosine()
test = json.load(open("./testing/test_case_2021_google_docs.json"))["testcases"]
result, cases = encapsulate(test)

my_dict = {"COSINE":0, "JACCARD":1, "TFIDF":2, "USE":3}

key_list = list(my_dict.keys())
val_list = list(my_dict.values())
for i in range (len(result)):
    s = f"Original Post\nSubject:{cases[i]['Subject']}\nBody:{cases[i]['Body']}\n{'-'*100}\n"
    print(s)
    out_file.write(s)
    for j in range (len(result[i])):
        algo_name = key_list[val_list.index(j)]
        s = "<<<<----------------------------------->>>>\n"\
        +   "|                                         |\n"\
        +   "|                                         |\n"\
        +  f"Result {algo_name}                         \n"\
        +  f"Subject:{result[i][j].subject}           \n\n"\
        +  f"Body:{result[i][j].payload}                \n"\
        +   "|                                         |\n"\
        +   "|                                         |\n"\
        +   "<<<<----------------------------------->>>>\n"
        print(s)
        out_file.write(s)
    s = "-"*100 + "\n"
    print(s)
    out_file.write(s)
