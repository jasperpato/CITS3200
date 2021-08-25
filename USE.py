import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import tensorflow_hub as hub

'''
Versions of packages 
tensorflow==2.0.0
tensorflow-estimator==2.0.1
tensorflow-hub==0.7.0
'''

import numpy as np
import pandas as pd
from typing import List, Tuple
from heapq import nlargest

'''
Versions of packages
numpy==1.17.2
pandas==0.25.1
'''

from post import Post
from thread import Thread, all_posts


# load universal sentence encoder module
def load_USE_encoder(module):
    with tf.Graph().as_default():
        sentences = tf.placeholder(tf.string)
        embed = hub.Module(module)
        embeddings = embed(sentences)
        session = tf.train.MonitoredSession()
    return lambda x: session.run(embeddings, {sentences: x})


encoder = load_USE_encoder('../USE_model')


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    mag_1 = np.sqrt(np.dot(vec1, vec2))
    mag_2 = np.sqrt(np.dot(vec2, vec2))
    return dot_product / (mag_1 * mag_2)


# return a pandas dataframe that includes the similarity between every post. 
# can be used to generate clusters
def get_similarity_dataframe(threads):
    posts = all_posts(threads)
    k = lambda x: x.subject if x.subject else lambda x: x.payload
    encoded_posts = encoder([k(post) for post in posts])
    num_posts = len(posts)
    similarities_df = pd.DataFrame()
    for i in range(num_posts):
        for j in range(num_posts): 
            # cos(theta) = x . y / (mag_x * mag_y)
            cos_theta = cosine_similarity(encoded_posts[i], encoded_posts[j])
            similarities_df = similarities_df.append(
                {
                    'similarity': cos_theta, 
                    'post1': posts[i], 
                    'post2': posts[j]
                },
                ignore_index=True
            )


# Identical in use-case to the function defined in algorithm.py
def find_similar_posts(post, threads, n, subject):
    posts = all_posts(threads)
    k = lambda x: x.subject if x.subject else lambda x: x.payload
    encoded_posts = encoder([k(post) for post in posts])
    in_vec = encoder([k(post)])[0]
    post_scores = {p: cosine_similarity(in_vec, p) for p in encoded_posts}
    return tuple(nlargest(n, post_scores, key=post_scores.get))
