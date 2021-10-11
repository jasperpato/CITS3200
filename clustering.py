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

def clustering(threads : List[Thread]):

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

def verified_clustering(threads : List[Thread]):
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

def build_affinity(threads : List[Thread]):
    all_posts_reduced = all_posts(threads)
    graph = []
    cutoff = 0.002
    for post in all_posts(threads):
        graph.append([])
        for other_post in all_posts_reduced:
            payload_toks = process_post(post, cleaners, filters, tuple([]), False)
            cosine_sim = cosine_similarity(payload_toks, process_cached(other_post, cleaners, filters, tuple([]), False))
            graph[len(graph)-1].append(cosine_sim)
    return graph

from sklearn.cluster import AffinityPropagation
import numpy

def affinity_clustering(threads : List[Thread]):
    try:
        affinity_graph = numpy.load("graph.npy", allow_pickle=True)
    except:
        affinity_graph = build_affinity(threads)
        print("graph built")
        numpy.save("graph", numpy.array(affinity_graph))
    aff_prop = AffinityPropagation(affinity = "precomputed")
    aff_prop.fit(affinity_graph)
    labels = aff_prop.fit_predict(affinity_graph)
    cluster_centers = aff_prop.cluster_centers_indices_
    n_clusters = len(cluster_centers)
    cluster_sizes = [0]*n_clusters
    for label in labels:
        cluster_sizes[label] = cluster_sizes[label] + 1
    biggest_clusters = []
    for i in range(0, 5):
        maxi = 0
        pos = 0
        for i in range(n_clusters):
            if i in biggest_clusters: continue
            if cluster_sizes[i] > maxi:
                maxi = cluster_sizes[i]
                pos = i
        biggest_clusters.append(pos)
    posts = all_posts(threads)
    for clus in biggest_clusters:
        print(posts[cluster_centers[clus]])

    
def main():

    threads = parse_file("help2002-2019.txt")
    start = time.time()
    affinity_clustering(threads)
    end = time.time()
    print("time taken: ", end-start)
    
