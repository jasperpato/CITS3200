"""
To use the code enter this code into the command line:

python3 similarity.py [text_data_file_with_posts]

The system will prompt you to write a subject and body of text.
Then it wil lreturn 3 of the most similiar post.
"""
import sys
from parse_file import parse_file
from thread_obj import Thread
from post import Post
from pipeline import pipeline
import nltk
from re import sub
from string import ascii_letters
from weights import verified_weight, date_weight
from utils import remove_non_alphabet, remove_stopwords, to_lower
nltk.download('punkt')
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')

from similarity_algorithms.cosine import Cosine
from similarity_algorithms.tfidf import Tfidf
from similarity_algorithms.jaccard import Jaccard
from similarity_algorithms.use import Use

def similarity(filename, post_subject, post_text, N=3):
    threads = parse_file(filename)
    
    new_post = Post(None,post_subject,post_text,None)
    W = 0.2 # weight of subject similarity, payload weight is (1.0 - W)

    filters = (remove_non_alphabet, remove_stopwords)

    weights = [verified_weight, date_weight]
    
    cleaners = (to_lower, lambda x: sub(r'\s+', ' ', x))

    substitutes = tuple([])

    similarity_classes = [Cosine, Tfidf, Jaccard, Use]
    
    algorithms = tuple([s().similarity for s in similarity_classes])
    return [p for p in pipeline(new_post, threads, cleaners, filters, substitutes,  weights, algorithms, W, N)]

if __name__ == "__main__":
    
    if len(sys.argv) < 3: exit()
    filename = sys.argv[1]
    N = int(sys.argv[2])
    subject = input("Subject: ")
    payload = input("Payload: ")
    
    posts = similarity(filename, subject, payload, N)
    for p in posts: print(f"{p.subject}\n{p.payload}\n")
