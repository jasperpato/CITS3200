from sklearn.cluster import AffinityPropagation
from algorithms import cosine_similarity
from thread_obj import Thread, all_posts
from weights import verified_weight
from pipeline import process_post
from utils import cached
from typing import List
import numpy

process_cached = cached(process_post)

def simple_clustering(threads : List[Thread], cleaners, filters, n):
    closest_vector = {}
    all_posts_reduced = all_posts(threads)
    for post in all_posts(threads):
        for other_post in all_posts_reduced:
            if post == other_post:
                continue
            payload_toks = process_post(post, cleaners, filters, tuple([]), False)
            cosine_sim = cosine_similarity(payload_toks, process_cached(other_post, cleaners, filters, tuple([]), False))
            if post not in closest_vector:
                closest_vector[post] = (None, 0.003)
            if other_post not in closest_vector:
                closest_vector[other_post] = (None, 0.003)
            if cosine_sim < closest_vector[post][1]:
                if cosine_sim == 0.0: continue
                closest_vector[post] = (other_post, cosine_sim)
            if cosine_sim < closest_vector[other_post][1]:
                if cosine_sim == 0.0: continue
                closest_vector[other_post] = (post, cosine_sim)
        all_posts_reduced.remove(post)
    clusters = {}
    for post in all_posts(threads):
        clusters[post] = []
    for post in closest_vector:
        if closest_vector[post][0] == None: continue
        clusters[closest_vector[post][0]].append(post)
    faq = []
    for i in range(n):
        maxi = 0
        biggest_cluster = ""
        for post in clusters.keys():
            if post in faq: continue
            if len(clusters[post]) >= maxi:
                maxi = len(clusters[post])
                biggest_cluster = post
        faq.append(biggest_cluster)
    return faq


def simple_verified_clustering(threads : List[Thread], alg, cleaners, filters, n):
    closest_vector = {}
    verified_all_posts = []
    for post in all_posts(threads):
        if verified_weight(post) == 1.35:
            verified_all_posts.append(post)
    all_posts_reduced = all_posts(threads)
    for post in verified_all_posts:
        for other_post in all_posts_reduced:
            if post == other_post:
                continue
            payload_toks = process_post(post, cleaners, filters, tuple([]), False)
            cosine_sim = alg(payload_toks, process_cached(other_post, cleaners, filters, tuple([]), False))
            if post not in closest_vector:
                closest_vector[post] = (None, 0.003)
            if other_post not in closest_vector:
                closest_vector[other_post] = (None, 0.003)
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
    print(len(clusters))
    faq = []
    for i in range(n):
        maxi = 0
        biggest_cluster = ""
        for post in clusters.keys():
            if post in faq: continue
            if len(clusters[post]) >= maxi:
                maxi = len(clusters[post])
                print(maxi)
                biggest_cluster = post
        faq.append(biggest_cluster)
    return faq

#Constructs affinity matrix corresponding to the similarity between posts
def build_affinity(threads : List[Thread], cleaners, filters):
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

#not finished?????
#Extends the affinity matrix to include new posts
def add_to_affinity(threads : List[Thread], cleaners, filters):
    try:
        graph = numpy.load("graph.npy", allow_pickle=True)
    except:
        print("cannot add to non-existant graph")
        return
    posts = all_posts(threads)
    for i in range(len(graph), len(posts(threads))):
        graph.append([])
        for j in range(len(posts)):
            payload_toks = process_post(post, cleaners, filters, tuple([]), False)
            cosine_sim = cosine_similarity(payload_toks, process_cached(other_post, cleaners, filters, tuple([]), False))
            graph[j].append(cosine_sim)
            graph[i].append(cosine_sim)
    
#Returns list of n posts corresponding to the centers of the biggest clusters
def affinity_clustering(threads : List[Thread], cleaners, filters, n):
    try:
        affinity_graph = numpy.load("graph.npy", allow_pickle=True)
    except:
        print("graph not saved, building graph")
        affinity_graph = build_affinity(threads, cleaners, filters)
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
    for i in range(n):
        maxi = 0
        pos = 0
        for j in range(n_clusters):
            if j in biggest_clusters: continue
            if cluster_sizes[j] > maxi:
                maxi = cluster_sizes[i]
                pos = j
        biggest_clusters.append(pos)
    posts = all_posts(threads)
    faq = []
    for clus in biggest_clusters:
        faq.append(posts[cluster_centers[clus]])
    return faq

    

    
