import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def save_tfidf_embeddings(posts, filename):
	vectorizer = TfidfVectorizer()
	embeddings = vectorizer.fit_transform([p.payload for p in posts])
	np.save(f'../encodings/tfidf/{filename}', embeddings)


def add_encoding(post, npfile):
	vectorizer = TfidfVectorizer()
	new_vec = vectorizer.fit_transform([post.payload])
	embeddings = np.load(npfile)
	np.save(f'../encodings/tfidf/{npfile}', np.append(embeddings, new_vec))


def tfidf_similarity(post, posts):
	vectorizer = TfidfVectorizer()
	vec = vectorizer.fit_transform([post.payload])
	
