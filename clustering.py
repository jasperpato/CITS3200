from algorithms import cosine_similarity
from thread_obj import Thread, all_posts
from weights import verified_weight
from utils import cached, remove_none_alphabet, remove_stopwords, to_lower
from typing import List
from pipeline import process_post
from re import sub
import time

from parse_file import parse_post, group_into_threads

#takes in threads in whatever form they're in (need to find out what that is exactly)
#creates a dictionary containing a list of each thread closest to the key thread
process_cached = cached(process_post)

cleaners =    ( to_lower,              # lowercase all text
                    lambda x: sub(r'\s+', ' ', x))

filters = (  remove_none_alphabet, # take non-alphabetical words out
                remove_stopwords)          # remove stopwords

def clustering(threads : List[Thread], subject : bool):

    closest_vector = {}

    i = 0

    all_posts_reduced = all_posts(threads)
    
    for post in all_posts(threads):

        print("post: ", i)
        i = i + 1

        #if i == 10: break

        for other_post in all_posts_reduced:

            #doesn't find how close the thread is to itself
            if post == other_post:
                continue

            #finds the cosine similarity for each pair of threads
            payload_toks = process_post(post, cleaners, filters, tuple([]), False)
            cosine_sim = cosine_similarity(payload_toks, process_cached(other_post, cleaners, filters, tuple([]), False))

            #sets current closest thread dependending on the cosine similarity
            if post not in closest_vector:

                #previous 0.003
                closest_vector[post] = (None, 0.002)

            if other_post not in closest_vector:

                closest_vector[other_post] = (None, 0.002)

            if cosine_sim < closest_vector[post][1]:

                if cosine_sim == 0.0: continue

                closest_vector[post] = (other_post, cosine_sim)
                #print(cosine_sim)

            if cosine_sim < closest_vector[other_post][1]:

                if cosine_sim == 0.0: continue

                closest_vector[other_post] = (post, cosine_sim)

        all_posts_reduced.remove(post)
        
    clusters = {}
    
    for post in all_posts(threads):

        clusters[post] = []

    #structures the results into a dictionary with the thread as the key and a list of closest threads as the value
    for post in closest_vector:

        if closest_vector[post][0] == None: continue
        
        clusters[closest_vector[post][0]].append(post)

    return clusters

from weights import verified_weight

def verified_clustering(threads : List[Thread], subject : bool):
    closest_vector = {}
    verified_all_posts = []
    for post in all_posts(threads):
        if verified_weight(post) == 1.35:
            verified_all_posts.append(post)
    i = 0
    all_posts_reduced = all_posts(threads)
    print(len(verified_all_posts))
    for post in verified_all_posts:
        #print("post: ", i)
        i = i + 1
        for other_post in all_posts_reduced:
            if post == other_post:
                continue
            payload_toks = process_post(post, cleaners, filters, tuple([]), False)
            cosine_sim = cosine_similarity(payload_toks, process_cached(other_post, cleaners, filters, tuple([]), False))
            if post not in closest_vector:
                closest_vector[post] = (None, 0.002)
            if other_post not in closest_vector:
                closest_vector[other_post] = (None, 0.002)
            if cosine_sim < closest_vector[post][1]:
                if cosine_sim == 0.0: continue
                closest_vector[post] = (other_post, cosine_sim)
            if cosine_sim < closest_vector[other_post][1]:
                if cosine_sim == 0.0: continue
                closest_vector[other_post] = (post, cosine_sim)
        all_posts_reduced.remove(post)
    clusters = {}
    for post in closest_vector:
        clusters[post] = []
    for post in closest_vector:
        if closest_vector[post][0] == None: continue
        clusters[closest_vector[post][0]].append(post)
    return clusters


#needed to 'borrow' because importing gave encoding issue
def parse_file(filename):
    with open(filename, 'r', encoding="utf8") as file:
        s = file.read()
        post_strings = ["Date: " + x for x in s.split("Date: ")][1:]
        posts = [parse_post(s) for s in post_strings]
        
    return group_into_threads(posts)

def main():

    threads = parse_file("help2002-2019.txt")

    start = time.time()
    clusters = verified_clustering(threads, False)
    end = time.time()

    print(end - start)

    frequent = 0
    frequent_key = ""

    for key in clusters:

        if len(clusters[key]) > frequent:
            frequent = len(clusters[key])
            frequent_key = key

    print(frequent_key.payload)

    print()
    print("-----------------------------------------------------------")
    print()

    print(frequent)

    for post in clusters[frequent_key]:

        print(post.payload)
        print("----------------")

    keys = list(clusters.keys())
