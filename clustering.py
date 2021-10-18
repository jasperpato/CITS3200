from sklearn.cluster import AffinityPropagation
from thread_obj import Thread, all_posts
from weights import verified_weight
from pipeline import process_post
from utils import cached
from typing import List
import numpy

process_cached = cached(process_post)

def simple_clustering(threads : List[Thread], alg, cleaners, filters, n):
    closest_vector = {}
    all_posts_reduced = all_posts(threads)
    for post in all_posts(threads):
        payload_toks = process_post(post, cleaners, filters, tuple([]), False)
        payload_toks_dict = {p.id: process_cached(p, cleaners, filters, tuple([]), False) for p in all_posts_reduced}
        similarities = alg().similarity(payload_toks, payload_toks_dict)
        for other_post in all_posts_reduced:
            if post == other_post:
                continue
            if post not in closest_vector:
                closest_vector[post] = (None, 0.003)
            if other_post not in closest_vector:
                closest_vector[other_post] = (None, 0.003)
            if similarities[other_post.id] < closest_vector[post][1]:
                if similarities[other_post.id] == 0.0: continue
                closest_vector[post] = (other_post, similarities[other_post.id])
            if similarities[other_post.id] < closest_vector[other_post][1]:
                if similarities[other_post.id] == 0.0: continue
                closest_vector[other_post] = (post, similarities[other_post.id])
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
        payload_toks = process_post(post, cleaners, filters, tuple([]), False)
        payload_toks_dict = {p.id: process_cached(p, cleaners, filters, tuple([]), False) for p in all_posts_reduced}
        similarities = alg().similarity(payload_toks, payload_toks_dict)
        for other_post in all_posts_reduced:
            if post == other_post:
                continue
            if post not in closest_vector:
                closest_vector[post] = (None, 0.003)
            if other_post not in closest_vector:
                closest_vector[other_post] = (None, 0.003)
            if similarities[other_post.id] < closest_vector[post][1]:
                if similarities[other_post.id] == 0.0: continue
                closest_vector[post] = (other_post, similarities[other_post.id])
            if similarities[other_post.id] < closest_vector[other_post][1]:
                if similarities[other_post.id] == 0.0: continue
                closest_vector[other_post] = (post, similarities[other_post.id])
        all_posts_reduced.remove(post)
    clusters = {}
    for post in closest_vector:
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

#Constructs affinity matrix corresponding to the similarity between posts
def build_affinity(threads : List[Thread], alg, cleaners, filters):
    all_posts_reduced = all_posts(threads)
    graph = []
    cutoff = 0.002
    for post in all_posts(threads):
        graph.append([])
        payload_toks = process_post(post, cleaners, filters, tuple([]), False)
        payload_toks_dict = {p.id: process_cached(p, cleaners, filters, tuple([]), False) for p in all_posts_reduced}
        similarities = alg().similarity(payload_toks, payload_toks_dict)
        for other_post in all_posts_reduced:
            graph[len(graph)-1].append(similarities[other_post.id])
    return graph
    
#Returns list of n posts corresponding to the centers of the biggest clusters
def affinity_clustering(threads : List[Thread], alg, cleaners, filters, n):
    try:
        affinity_graph = numpy.load("graph.npy", allow_pickle=True)
    except:
        print("graph not saved, building graph")
        affinity_graph = build_affinity(threads, alg, cleaners, filters)
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

    

    
