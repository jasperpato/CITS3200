from re import sub
from post import Post
from algorithms2 import jaccard, bag_of_words
from utils import space, to_lower, remove_none_alphabet, remove_stopwords, stemmer
from pipeline import pipeline
from weights import verified_weight, date_weight
from spell_correction_pysc import spell_correction
from similarity_algorithms.tfidf import Tfidf
#from similarity_algorithms.use import Use
from parse_file import parse_file
import json


def encapsulate(test_cases):
    list_of_tup = [] 
    cleaners = [to_lower,space]
    filters = [remove_none_alphabet, remove_stopwords]
    substitutes = []
    weight = [date_weight,verified_weight]
    files = ['help2002-2017.txt', 'help2002-2018.txt', 'help2002-2019.txt']
    all_threads = [parse_file(f) for f in files]
    threads = all_threads[2]
    for case in test_cases:
        post = Post(case['Date'], case['Subject'], case['Body'], False)
        list_of_tup.append(tuple(generate_post(post, threads, cleaners, filters, substitutes, weight, 5)))
    return list_of_tup, test_cases

def generate_post(post, threads, cleaners, filters, substitutes, weights, nposts):
    diff_posts = []
    tf = Tfidf()
    #Us = Use()
    Jaccard_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [jaccard],0.2, nposts)
    Bag_of_words_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [bag_of_words],0.2, nposts)
    Tfidf_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [tf.similarity],0.2, nposts)
    #Use_posts = pipeline(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, [Us.similarity],0.2, nposts)
    list_of_posts = [Bag_of_words_posts, Jaccard_posts, Tfidf_posts]
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

test = json.load(open("./testing/test_case_2019.json"))["testcases"]
result, cases = encapsulate(test)

my_dict ={"cosine":0, "jacard":1, "tfidf":2}

key_list = list(my_dict.keys())
val_list = list(my_dict.values())
for i in range (len(result)):
    print("Orig post:", cases[i])
    for j in range (len(result[i])):
        print("<<<<---------------------------------->>>>")
        print("|                                         |")
        print("|                                         |")
        print("result {use}: {res}".format(use = key_list[val_list.index(j)],res = result[i][j].payload))
        print("|                                         |")
        print("|                                         |")
        print("<<<<---------------------------------->>>>")
    print("------------------------------------------------------------------------------------\n")
