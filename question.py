from re import sub
from post import Post
from similarity_algorithms.basic_algos import jaccard, bag_of_words
from utils import space, to_lower, remove_none_alphabet, remove_stopwords, stemmer
from pipeline import pipeline
from weights import verified_weight, date_weight
from spell_correction_pysc import spell_correction
from similarity_algorithms.tfidf import Tfidf
from similarity_algorithms.use import Use
from parse_file import parse_file
from datetime import datetime
import json
import os

currentdir = os.path.dirname(__file__)

tfidf = None
use = None


def encapsulate(test_cases):
    list_of_tup = [] 
    cleaners = [to_lower, space]
    filters = [remove_none_alphabet, remove_stopwords]
    substitutes = []
    weight = [date_weight, verified_weight]
    files = ['testing/test_space_2021_google_docs.txt']
    all_threads = [parse_file(f) for f in files]
    threads = all_threads[0]
    for case in test_cases:
        date = datetime.strptime("2019-07-28 16:54:49", "%Y-%m-%d %H:%M:%S")
        post = Post(date, case['Subject'], case['Body'], False)
        list_of_tup.append(tuple(generate_post(post, threads, cleaners, filters, substitutes, weight, 5)))
    return list_of_tup, test_cases

def generate_post(post, threads, cleaners, filters, substitutes, weights, nposts):
    diff_posts = []
    jaccard_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [jaccard],0.2, nposts)
    bag_of_words_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [bag_of_words],0.2, nposts)
    tfidf_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [tfidf.similarity],0.2, nposts)
    use_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [use.similarity],0.2, nposts)
    list_of_posts = [bag_of_words_posts, jaccard_posts, tfidf_posts, use_posts]
    diff_posts = find_diff_posts(list_of_posts, diff_posts)
    return diff_posts

def find_diff_posts(list, diff: list):
    for item in list:
        for cos in item:
            select = 0
            for it in list:
                if it is not item and cos not in it:
                    select += 1
            if select == 2 or cos == item[-1]:
                diff.append(cos)
                break

    return diff

out_file = open('google_docs_case_dump.txt', 'w')
tfidf = Tfidf()
use = Use(os.path.join(currentdir, "../pretrained_models/universal-sentence-encoder_4/"))
test = json.load(open("./testing/test_case_2019.json"))["testcases"]
result, cases = encapsulate(test)

my_dict = {"COSINE":0, "JACCARD":1, "TFIDF":2, "USE":3}

key_list = list(my_dict.keys())
val_list = list(my_dict.values())
for i in range (len(result)):
    s = f"Original Post\nSubject:{cases[i]['Subject']}\nBody:{cases[i]['Body']}\n{'-'*100}\n"
    print(s)
    out_file.write(s)
    for j in range (len(result[i])):
        use = key_list[val_list.index(j)]
        res = result[i][j].payload
        s = "<<<<----------------------------------->>>>\n"\
        +   "|                                         |\n"\
        +   "|                                         |\n"\
        +               f"result {use}: {res}\n"           \
        +   "|                                         |\n"\
        +   "|                                         |\n"\
        +   "<<<<----------------------------------->>>>\n"
        print(s)
        out_file.write(s)
    s = "-"*100 + "\n"
    print(s)
    out_file.write(s)
