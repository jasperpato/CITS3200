import pickle
import sys 
import tensorflow as tf
import tensorflow_hub as hub
import json

from heapq import nlargest
from sklearn.metrics.pairwise import cosine_similarity
from os.path import dirname, join

from .algorithm import Algorithm
from parse_file import parse_file
from thread_obj import all_posts


post_text = lambda post: post.subject if len(post.subject.split(' ')) >= 10 else post.payload

filedir = dirname(__file__)
pretrained_model_path = join(filedir, '../../pretrained_models/use/universal-sentence-encoder_4')
sys.path.append(dirname(filedir))


class Use(Algorithm):
    model = None
    encodings = None

    def __init__(self, model_path, use_cpu=False):
        if use_cpu:
            tf.config.set_visible_devices([], 'GPU')
        self.model = hub.load(model_path)

    def load_encodings(self, encodings_path):
        with open(encodings_path, 'rb') as handle:
            self.encodings = pickle.load(handle)

    def encode_posts(self, posts, save_path=None):
        encoded_posts = self.model([post_text(post) for post in posts])
        encodings = {posts[i].payload:encoded_posts[i] for i in range(len(posts))}
        if save_path != None:
            with open(save_path, 'wb') as handle:
                pickle.dump(encodings, handle, protocol=pickle.HIGHEST_PROTOCOL)
        self.encodings = encodings

    def similarity(self, post, posts, n):
        if self.encodings == None:
            raise RuntimeError("Encodings must be loaded from save file (using load_encodings)" +
            " or computed (using encode_posts)")

        if post.payload not in self.encodings.keys():
            in_vec = self.model([post_text(post)])
        else:
            in_vec = [self.encodings[post.payload]]
            posts = [p for p in posts if p.payload != post.payload]

        encoding_vecs = [self.encodings[post.payload] for post in posts]
        scores = cosine_similarity(in_vec, encoding_vecs).flatten()
        post_score_map = {posts[i]:scores[i] for i in range(len(posts))}
        return tuple(nlargest(n, post_score_map, key=post_score_map.get))

    
def encode_test_spaces():
    from testing.similaritytest import json_to_post_1, json_to_post_2
    algo = Use(pretrained_model_path)
    
    
    test_f = open(join(filedir, "../testing/test_space_2019_2.json"))
    test_space_posts = json.load(test_f)['test_space']
    posts = [json_to_post_2(p) for p in test_space_posts]
    algo.encode_posts(posts, join(filedir, '../../encodings/use/test_space_2019_2.pickle'))

    test_f = open(join(filedir, "../testing/test_space_2019.json"))
    test_space_posts = json.load(test_f)['testcases']
    posts = [json_to_post_1(p) for p in test_space_posts]
    algo.encode_posts(posts, join(filedir, '../../encodings/use/test_space_2019_1.pickle'))


def encode_dataset():
    algo = Use(pretrained_model_path)

    posts = all_posts(parse_file(join(filedir, '../help2002-2017.txt')))
    algo.encode_posts(posts, join(filedir, '../../encodings/use/2017.pickle'))

    posts = all_posts(parse_file(join(filedir, '../help2002-2018.txt')))
    algo.encode_posts(posts, join(filedir, '../../encodings/use/2018.pickle'))

    posts = all_posts(parse_file(join(filedir, '../help2002-2019.txt')))
    algo.encode_posts(posts, join(filedir, '../../encodings/use/2019.pickle'))


if __name__== '__main__':
    encode_dataset()