from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from heapq import nlargest
import os, sys

from .algorithm import Algorithm

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

post_text = lambda post: post.subject if len(post.subject.split(' ')) >= 10 else post.payload

class Tfidf(Algorithm):
    vectorizer = None

    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def similarity(self, in_toks, toks_array, **kwargs):
        in_text = ' '.join(str(in_toks))
        document_list = [' '.join(str(toks)) for toks in toks_array]
        document_list.insert(0, in_text)
        embeddings = self.vectorizer.fit_transform(document_list)
        scores = cosine_similarity(embeddings[0], embeddings[1:]).flatten()
        return scores