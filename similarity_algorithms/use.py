import pickle
import sys 
import tensorflow as tf
import tensorflow_hub as hub
import json

from sklearn.metrics.pairwise import cosine_similarity
from os.path import dirname, join

from .algorithm import SimilarityAlgorithm
from parse_file import parse_file
from thread_obj import all_posts


post_text = lambda post: post.subject if len(post.subject.split(' ')) >= 10 else post.payload

filedir = dirname(__file__)
pretrained_model_path = join(filedir, '../../pretrained_models/use/universal-sentence-encoder_4')
sys.path.append(dirname(filedir))


class Use(SimilarityAlgorithm):
    model = None
    encodings = None

    def __init__(self, model_path, use_cpu=True):
        if use_cpu:
            tf.config.set_visible_devices([], 'GPU')
        self.model = hub.load(model_path)


    def load_encodings(self, encodings_path):
        with open(encodings_path, 'rb') as handle:
            self.encodings = pickle.load(handle)


    def encode_posts(self, toks_dict, save_path=None):
        sorted_keys = sorted(toks_dict.keys())
        toks_arr = [toks_dict[k] for k in sorted_keys]
        encoded_posts = self.model([''.join(toks) for toks in toks_arr])
        encodings = dict(zip(sorted_keys, encoded_posts))
        if save_path:
            with open(save_path, 'wb') as handle:
                pickle.dump(encodings, handle, protocol=pickle.HIGHEST_PROTOCOL)
        self.encodings = encodings


    def similarity(self, in_toks, toks_dict):
        if self.encodings == None:
            self.encode_posts(toks_dict)
           
        in_text = ''.join(in_toks)
        in_vec = self.model([in_text])

        sorted_keys = sorted(toks_dict.keys())
        encoding_vecs = [self.encodings[post_id] for post_id in sorted_keys]
        scores = cosine_similarity(in_vec, encoding_vecs).flatten()
        post_score_map = dict(zip(sorted_keys, scores))
        return post_score_map

    
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