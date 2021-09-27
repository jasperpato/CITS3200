from re import sub
from post import Post
from algorithms import jaccard, cosine_similarity
from utils import space, to_lower, remove_none_alphabet, remove_stopwords, stemmer
from pipeline import pipeline
from weights import verified_weight, date_weight
from spell_correction_pysc import spell_correction
#from similarity_algorithms import tfidf
from parse_file import parse_file
import json


def encapsulate(test_cases):
    list_of_tup = []
    cleaners = [to_lower,space]
    filters = [remove_none_alphabet, remove_stopwords]
    substitutes = [stemmer]
    weight = [date_weight,verified_weight]
    files = ['help2002-2017.txt', 'help2002-2018.txt', 'help2002-2019.txt']
    all_threads = [parse_file(f) for f in files]
    threads = all_threads[2]
    for case in test_cases:
        post = Post(None, case['Subject'], case['Body'], None)
        print(post.payload)
        list_of_tup.append(tuple(generate_post(post, threads, cleaners, filters, substitutes, weight, 5)))
    return list_of_tup

def generate_post(post, threads, cleaners, filters, substitutes, weights, nposts):
    diff_posts = []
    Jaccard_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [cosine_similarity],0.2, nposts)
    Cosine_Posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [jaccard],0.2, nposts)
    Tfidf_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, (jaccard, cosine_similarity),0.2, nposts)
    print(Jaccard_posts[0].payload)
    # Mod_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, cosine_similarity, nposts)
    list_of_posts = [Cosine_Posts, Tfidf_posts]
    diff_posts.append(Jaccard_posts[0])
    diff_posts = find_diff_posts(list_of_posts, diff_posts)
    return diff_posts

def find_diff_posts(list, diff: list):
    for item in list:
        for cos in item:
                if cos in diff or cos == item[-1]:
                    diff.append(cos)
                    break
                else:
                    continue
    return diff

test = json.load(open("./testing/test_case_2019.json"))["testcases"]
result = encapsulate(test)
