import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from heapq import nlargest
import json


def tfidf_similarity(post, posts, n):
	vectorizer = TfidfVectorizer()
	vec = vectorizer.fit_transform([post.payload])


	document_list = [p.payload for p in posts]
	document_list.insert(0, post.payload)
	embeddings = vectorizer.fit_transform(document_list)

	scores = cosine_similarity(embeddings[0:1], embeddings[1:]).flatten()
	post_scores = {posts[i]:scores[i] for i in range(len(posts))}
	return nlargest(n, post_scores, key=post_scores.get)
	
