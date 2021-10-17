"""
Default usage:
python3 similarity.py [text file with posts] [number of posts to return]
    
To choose specific similarity algorithms to invoke, use the option -alg followed by algorithms. Default is tfidf

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

parser.add_argument('filename', type=str, help='Filename of the text file containing posts to be returned by their text similarity.', nargs='?', default="help2002-2017.txt")

parser.add_argument('n', type=int, help='The number of similar posts to return.', nargs='?', default=3)

parser.add_argument('-a', '--algorithm', dest='algs', type=str, help='Similarity algorithms to utilise. Choose from the algorithms' + \
    ' [tfidf, use, cosine, jaccard], where results are averaged if more than 1 algorithm is used. Default is tfidf.', nargs='*', 
    default=['tfidf'])

parser.add_argument('-s', '--spellcheck', dest='spell', help='Whether to perform spell correction on the input text before text similarity' + \
    ' is performed. Increases compute time significantly.', action='store_true', default=False)


def similar(filename, subject, payload, algos=[Tfidf], N=3, use_spellcheck=False, W=0.1):
    
    posts = parse_file(filename)
    new_post = Post(None, None, subject, payload, None)

    filters = (remove_non_alphabet, remove_stopwords)
    weights = (verified_weight, date_weight)
    cleaners = (to_lower, lambda x: sub(r'\s+', ' ', x))
    substitutes = tuple([])
    
    algorithms = tuple([algo().similarity for algo in algos])
    return [p for p in pipeline(new_post, posts, cleaners, filters, substitutes, weights, algorithms, N, use_spellcheck, W)]


if __name__ == "__main__":
    args = parser.parse_args()
    subject = input("Subject: ")
    payload = input("Payload: ")
    
    filename = args.filename
    num_posts = args.n
    algos = [algos_dict[name] for name in args.algs]
    use_spellcheck = args.spell

    posts = similar(filename, subject, payload, algos, num_posts, use_spellcheck)
    for p in posts: print(f"{p.subject}\n{p.payload}\n")
