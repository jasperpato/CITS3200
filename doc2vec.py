import numpy as np
import nltk
import string
import json
from gensim.models.doc2vec import Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity
from heapq import nlargest

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

model = None
post_text = lambda post: post.subject if len(post.subject.split(' ')) >= 10 else post.payload


def load_doc2vec_model():
    global model
    filename = '../pretrained_models/doc2vec/enwiki_dbow/doc2vec.bin'
    model = Doc2Vec.load(filename)


def preprocess(text):
    lowered = str.lower(text)
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(lowered)
    lemmatizer = WordNetLemmatizer()

    words = []
    for w in word_tokens:
        if w not in stop_words:
            if w not in string.punctuation:
                if len(w) > 1:
                    lemmatized = lemmatizer.lemmatize(w)
                    words.append(lemmatized)

    # Only handle words that appear in the doc2vec pretrained vectors. enwiki_ebow model contains 669549 vocabulary size.
    words = list(filter(lambda x: x in model.wv.vocab.keys(), words))
    return words


def encode_posts(posts, save_name):
    tokens_arr = [preprocess(post_text(post)) for post in posts]
    encoded_posts = [model.infer_vector(tokens) for tokens in tokens_arr]
    np.save(f'../encodings/doc2vec/{save_name}', encoded_posts)
    return encoded_posts


def doc2vec_similarity(post, encoded_posts, posts, n):
    tokens = preprocess(post_text(post))
    in_vec = model.infer_vector(tokens)
    scores = cosine_similarity(in_vec, encoded_posts)
    post_score_map = {posts[i]:scores[i] for i in range(len(posts))}
    return tuple(nlargest(n, post_score_map, key=post_score_map.get))


if __name__== '__main__':
    from testing.similaritytest import parse_post

    test_space_posts = json.load(open("testing/test_space_2019.json"))["testcases"]
    posts = [parse_post(p) for p in test_space_posts]
    load_doc2vec_model()
    encode_posts(posts, 'test_space.npy')
