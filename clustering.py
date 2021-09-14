from summarise import cosine_similarity
from thread import Thread, all_posts
from tokeniser import preprocess
from typing import List

from parse_file import parse_post, group

#takes in threads in whatever form they're in (need to find out what that is exactly)
#creates a dictionary containing a list of each thread closest to the key thread
def clustering(threads : List[Thread], subject : bool):

    k = (lambda x: x.subject) if subject else (lambda x: x.payload)

    closest_vector = {}

    i = 0
    
    for post in all_posts(threads):

        print("post: ", i)
        i = i + 1

        #if i == 10: break

        for other_post in all_posts(threads):

            #doesn't find how close the thread is to itself
            if post == other_post:
                continue

            #finds the cosine similarity for each pair of threads
            cosine_sim = cosine_similarity(preprocess(k(post)), preprocess(k(other_post)))

            #sets current closest thread dependending on the cosine similarity
            if post not in closest_vector:

                #previous 0.003
                closest_vector[post] = (None, 0.002)

            if cosine_sim < closest_vector[post][1]:

                if cosine_sim == 0.0: continue

                closest_vector[post] = (other_post, cosine_sim)
                #print(cosine_sim)

    clusters = {}
    
    for post in all_posts(threads):

        clusters[post] = []

    #structures the results into a dictionary with the thread as the key and a list of closest threads as the value
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
        
    return group(posts)

def main():

    threads = parse_file("help2002-2019.txt")

    clusters = clustering(threads, False)

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
