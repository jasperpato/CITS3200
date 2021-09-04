from summarise import cosine_similarity

#takes in threads in whatever form they're in (need to find out what that is exactly)
#creates a dictionary containing a list of each thread closest to the key thread
def clustering(threads):

    closest_vector = {}
    
    for thread in threads:

        for other_thread in threads:

            #doesn't find how close the thread is to itself
            if thread == other_thread:
                continue

            #finds the cosine similarity for each pair of threads
            cosine_sim = cosine_similarity(thread, other_thread)

            #sets current closest thread dependending on the cosine similarity
            if thread in closest_vector:

                if cosine_sim < closest_vector[thread][1]:

                    closest_vector[thread] = (other_thread, cosine_sim)

            else:
                
                closest_vector[thread] = (other_thread, cosine_sim)

    clusters = {}
    
    for thread in threads:

        clusters[thread] = []

    #structures the results into a dictionary with the thread as the key and a list of closest threads as the value
    for thread in closest_vector:

        clusters[closest_vector[thread][0]].append(thread)

    return clusters
