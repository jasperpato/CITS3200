from clustering import simple_clustering, simple_verified_clustering, affinity_clustering
from utils import remove_non_alphabet, remove_stopwords, to_lower
from parse_file import parse_post, group_into_threads
from re import sub
import importlib
import time


#needed to 'borrow' because importing gave encoding issue
def parse_file(filename):
    with open(filename, 'r', encoding="utf8") as file:
        s = file.read()
        post_strings = ["Date: " + x for x in s.split("Date: ")][1:]
        posts = [parse_post(id, s) for id, s in enumerate(post_strings)]
        
    return group_into_threads(posts)


def main():
    module = importlib.import_module(f"similarity_algorithms.tfidf")
    alg = getattr(module, "Tfidf")

    threads = parse_file("help2002-2019.txt")
    cleaners =    ( to_lower,              # lowercase all text
                    lambda x: sub(r'\s+', ' ', x))
    filters = (remove_non_alphabet, remove_stopwords)
    start = time.time()
    faq = affinity_clustering(threads, alg, cleaners, filters, 5)
    end = time.time()
    for i in faq:
        print(i)
        print("--------------------------------")
    print("time taken: ", end-start)
