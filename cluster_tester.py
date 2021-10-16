from clustering import simple_clustering, simple_verified_clustering, affinity_clustering
from utils import remove_none_alphabet, remove_stopwords, to_lower
from parse_file import parse_post, group_into_threads
from re import sub
import time

#needed to 'borrow' because importing gave encoding issue
def parse_file(filename):
    with open(filename, 'r', encoding="utf8") as file:
        s = file.read()
        post_strings = ["Date: " + x for x in s.split("Date: ")][1:]
        posts = [parse_post(s) for s in post_strings]
        
    return group_into_threads(posts)


def main():

    threads = parse_file("help2002-2019.txt")
    cleaners =    ( to_lower,              # lowercase all text
                    lambda x: sub(r'\s+', ' ', x))
    filters = (  remove_none_alphabet, # take non-alphabetical words out
                remove_stopwords)          # remove stopwords
    start = time.time()
    faq = simple_verified_clustering(threads, cleaners, filters, 5)
    end = time.time()
    for i in faq:
        print(i)
        print("--------------------------------")
    print("time taken: ", end-start)
