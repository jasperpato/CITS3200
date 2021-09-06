import tensorflow.compat.v1 as tf_v1
tf_v1.disable_v2_behavior()
import tensorflow_hub as hub

import numpy as np
import pandas as pd
from heapq import nlargest
import json

from post import Post
from thread import Thread, all_posts


# load universal sentence encoder module
def load_USE_encoder(module):
    with tf_v1.Graph().as_default():
        sentences = tf_v1.placeholder(tf_v1.string)
        embed = hub.Module(module)
        embeddings = embed(sentences)
        session = tf_v1.train.MonitoredSession()
    return lambda x: session.run(embeddings, {sentences: x})


encoder = load_USE_encoder('../USE')


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    mag_1 = np.sqrt(np.dot(vec1, vec2))
    mag_2 = np.sqrt(np.dot(vec2, vec2))
    return dot_product / (mag_1 * mag_2)


# return a pandas dataframe that includes the similarity between every post. 
# can be used to generate clusters
def get_similarity_dataframe(posts, encoded_posts, encoder):
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
def similarity_function_USE(post, encoded_posts, posts, n, encoder):
    in_vec = encoder([post.payload])[0]
    scores = [cosine_similarity(in_vec, p) for p in encoded_posts]
    post_dict = {posts[i]:scores[i] for i in range(len(posts))}
    return tuple(nlargest(n, post_dict, key=post_dict.get))


def encode_posts(posts, save_name):
    k = lambda x: x.subject if x.subject else lambda x: x.payload
    encoded_posts = encoder([k(post) for post in posts])
    np.save(f'../encodings/{save_name}', encoded_posts)
    return encoded_posts


if __name__== '__main__':
    from testing.similaritytest2 import parse_post

    test_space_posts = json.load(open("testing/test_space_2019.json"))["testcases"]
    posts = [parse_post(p) for p in test_space_posts]
    encode_posts(posts, 'test_space.npy')


    
