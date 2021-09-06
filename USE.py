import tensorflow_hub as hub

import numpy as np
import pandas as pd
from heapq import nlargest
import json
import nltk

from post import Post
from thread import Thread, all_posts


# load universal sentence encoder module

encoder = hub.load('../pretrained_models/universal-sentence-encoder_4')


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
    k = lambda post: post.subject if len(post.subject.split(' ')) >= 10 else post.payload
    encoded_posts = encoder([k(post) for post in posts])
    np.save(f'../encodings/use/{save_name}', encoded_posts)
    return encoded_posts


if __name__== '__main__':
    from testing.similaritytest import parse_post

    test_space_posts = json.load(open("testing/test_space_2019.json"))["testcases"]
    posts = [parse_post(p) for p in test_space_posts]
    encode_posts(posts, 'test_space.npy')


    
