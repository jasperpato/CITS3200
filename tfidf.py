import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from heapq import nlargest
import json


def save_tfidf_embeddings(posts, filename):
	vectorizer = TfidfVectorizer()
	embeddings = vectorizer.fit_transform([p.payload for p in posts])
	np.save(f'../encodings/tfidf/{filename}', embeddings)


def add_encoding(post, npfile):
	vectorizer = TfidfVectorizer()
	new_vec = vectorizer.fit_transform([post.payload])
	embeddings = np.load(npfile)
	np.save(f'../encodings/tfidf/{npfile}', np.append(embeddings, new_vec))


def tfidf_similarity(post, embeddings, posts, n):
	vectorizer = TfidfVectorizer()
	vec = vectorizer.fit_transform([post.payload])
	scores = cosine_similarity(vec, embeddings).flatten()
	post_scores = {posts[i]:scores[i] for i in range(len(posts))}
	return nlargest(n, post_scores, key=post_scores.get)


if __name__ == '__main__':
	from testing.similaritytest import parse_post
	test_space = json.load(open('./testing/test_space_2019.json'))['testcases']
	posts = [parse_post(p) for p in test_space]
	save_tfidf_embeddings(posts, 'test_space.npy')
	
