from sentence_transformers import SentenceTransformer
from nltk import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from heapq import nlargest
import numpy as np
import torch
import json

if not torch.cuda.is_available():
    raise("CUDA is not configured properly")

model = None
post_text = lambda post: post.subject if len(post.subject.split(' ')) >= 10 else post.payload


def load_bert_model(use_cpu=False):
    global model 
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    if use_cpu:
        model = model.cpu()


def encode_posts(posts, save_name):
    load_bert_model()
    encoded_posts = [0] * len(posts)
    for i in range(len(posts)):
        sentences = sent_tokenize(post_text(posts[i]))
        encoded_posts[i] = np.mean(model.encode(sentences), axis=0)
    np.save(f'../encodings/bert/{save_name}', encoded_posts)
    return encoded_posts


def gen_sentence_weights(num_weights, initial):
    weights = [initial / i for i in range(1, num_weights)]
    weights.insert(0, initial / 2)
    return weights


def bert_similarity(post, encoded_posts, posts, n):
    sentences = sent_tokenize(post_text(post))
    vec = np.mean(model.encode(sentences), axis=0)
    scores = cosine_similarity([vec], encoded_posts)[0]
    post_score_map = {posts[i]:scores[i] for i in range(len(posts))}
    return tuple(nlargest(n, post_score_map, key=post_score_map.get))


if __name__== '__main__':
    from testing.similaritytest import parse_post

    test_space_posts = json.load(open("testing/test_space_2019.json"))["testcases"]
    posts = [parse_post(p) for p in test_space_posts]
    encode_posts(posts, 'test_space.npy')