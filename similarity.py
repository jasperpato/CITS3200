"""
To use the code enter this code into the command line:

python3 similarity.py [text_data_file_with_posts] [Number of post to return]

The system will prompt you to write a subject and body of text.
By default, the program will return 3 posts unless specified
"""

import argparse
from parse_file import parse_file
from post import Post
from pipeline import pipeline
import nltk
from re import sub
from weights import verified_weight, date_weight
from utils import remove_non_alphabet, remove_stopwords, to_lower
nltk.download('punkt')
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')

from similarity_algorithms.cosine import Cosine
from similarity_algorithms.tfidf import Tfidf
from similarity_algorithms.jaccard import Jaccard
from similarity_algorithms.use import Use

algos_dict = {'tfidf': Tfidf, 'use': Use, 'jaccard': Jaccard, 'cosine': Cosine}

prog_description = "------------ TO DO ----------------"
parser = argparse.ArgumentParser(description=prog_description, epilog='Enjoy the program! :D')

parser.add_argument('filename', type=str, help='filename of the text file containing posts to be returned by their text similarity')

parser.add_argument('n', type=int, help='the number of similar posts to return', default=3)

parser.add_argument('--algorithm', type=str, help='similarity algorithm to utilise. Invoke multiple times to use multiple algorithms' + \
    ', where result will be averaged between algorithms. Choose from the algorithms [tfidf, use, cosine, jaccard]', 
    action='append', default='Tfidf')


def similar(filename, subject, payload, algos=[Tfidf], N=3, W=0.2):
    
    threads = parse_file(filename)
    new_post = Post(None, subject, payload, None)

    filters = (remove_non_alphabet, remove_stopwords)
    weights = [verified_weight, date_weight]
    cleaners = (to_lower, lambda x: sub(r'\s+', ' ', x))
    substitutes = tuple([])
    
    algorithms = tuple([algo().similarity for algo in algos])
    return [p for p in pipeline(new_post, threads, cleaners, filters, substitutes,  weights, algorithms, W, N)]


if __name__ == "__main__":
    args = parser.parse_args()
    subject = input("Subject: ")
    payload = input("Payload: ")
    
    filename = args.filename
    num_posts = args.n
    algos = [algos_dict[name] for name in args.algorithm]

    posts = similar(filename, subject, payload, algos, num_posts)
    for p in posts: print(f"{p.subject}\n{p.payload}\n")
