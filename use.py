import pickle
import tensorflow as tf
import tensorflow_hub as hub

import numpy as np
import pandas as pd
from heapq import nlargest
from sklearn.metrics.pairwise import cosine_similarity
import json
import nltk

from post import Post
from parse_file import parse_file
from thread_obj import Thread, all_posts


# load universal sentence encoder module
encoder  = None
post_text = lambda post: post.subject if len(post.subject.split(' ')) >= 10 else post.payload


def load_use_model(use_cpu=False):
    global encoder
    if use_cpu:
        tf.config.set_visible_devices([], 'GPU')
    encoder = hub.load('../pretrained_models/use/universal-sentence-encoder_4')


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
def use_similarity(input_post, encodings, all_posts, n):
    if input_post.payload not in encodings.keys():
        in_vec = encoder([post_text(input_post)])
    else:
        in_vec = [encodings[input_post.payload]]
        all_posts = [p for p in all_posts if p.payload != input_post.payload]
    encoding_vecs = [encodings[post.payload] for post in all_posts]
    scores = cosine_similarity(in_vec, encoding_vecs).flatten()
    post_score_map = {all_posts[i]:scores[i] for i in range(len(all_posts))}
    return tuple(nlargest(n, post_score_map, key=post_score_map.get))


def encode_posts(posts, save_name):
    encoded_posts = encoder([post_text(post) for post in posts])
    embeddings = {posts[i].payload:encoded_posts[i] for i in range(len(posts))}
    with open(f'../encodings/use/{save_name}.pickle', 'wb') as handle:
        pickle.dump(embeddings, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return embeddings


def encode_test_space(test_space_file):
    from testing.similaritytest import json_to_post1, json_to_post2

    if test_space_file == "test_space_2019_2":
        test_space_posts = json.load(open(f"testing/{test_space_file}.json"))["test_space"]
        posts = [json_to_post2(p) for p in test_space_posts]
    else:
        test_space_posts = json.load(open(f"testing/{test_space_file}.json"))["testcases"]
        posts = [json_to_post1(p) for p in test_space_posts]
    load_use_model()
    encode_posts(posts, f'{test_space_file}')


if __name__== '__main__':
    load_use_model()
    posts = all_posts(parse_file('help2002-2017.txt'))
    encode_posts(posts, '2017')
    posts = all_posts(parse_file('help2002-2018.txt'))
    encode_posts(posts, '2018')
    posts = all_posts(parse_file('help2002-2019.txt'))
    encode_posts(posts, '2019')

    
