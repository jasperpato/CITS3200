"""
Default usage:
python3 similarity.py [text file with posts] [number of posts to return]
    
To choose specific similarity algorithms to invoke, use the option -alg followed by algorithms. Default is tfidf

The system will prompt you to write a subject and body of text.
By default, the program will return 3 posts unless specified
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import argparse
import importlib
import nltk
from parse_file import parse_file
from post import Post
from pipeline import pipeline
from re import sub
from weights import verified_weight, date_weight
from utils import remove_non_alphabet, remove_stopwords, to_lower
nltk.download('punkt')
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')


prog_description = "This program returns posts from an input file that are similar in meaning to an input post."
parser = argparse.ArgumentParser(description=prog_description, epilog='Enjoy the program! :D')

parser.add_argument('filename', type=str, help='Filename of the text file containing posts to be returned by their text similarity.', nargs='?', default="help2002-2017.txt")

parser.add_argument('n', type=int, help='The number of similar posts to return.', nargs='?', default=3)

parser.add_argument('-a', '--algorithm', dest='algs', type=str, help='Similarity algorithms to utilise. Choose from the algorithms' + \
    ' [tfidf, use, cosine, jaccard], where results are averaged if more than 1 algorithm is used. Default is tfidf.', nargs='*', 
    default=['tfidf'])

parser.add_argument('-s', '--spellcheck', dest='spell', help='Whether to perform spell correction on the input text before text similarity' + \
    ' is performed. Increases compute time significantly.', action='store_true', default=False)


def similar(filename, subject, payload, N=3, algo_names=['tfidf'], use_spellcheck=False, W=0.1):
    posts = parse_file(filename)
    new_post = Post(None, None, subject, payload, None)

    filters = (remove_non_alphabet, remove_stopwords)
    weights = (verified_weight, date_weight)
    cleaners = (to_lower, lambda x: sub(r'\s+', ' ', x))
    substitutes = tuple([])
    
    algo_names = [name.lower() for name in algo_names]
    algos = generate_algo_list(algo_names)
    algorithms = tuple([a().similarity for a in algos])
    return [p for p in pipeline(new_post, posts, cleaners, filters, substitutes, weights, algorithms, N, use_spellcheck, W)]


def generate_algo_list(algo_names):
    algos = []
    for algo_name in algo_names:
        module = importlib.import_module(f'similarity_algorithms.{algo_name}')
        algos.append(getattr(module, algo_name.capitalize()))
    return algos


if __name__ == "__main__":
    args = parser.parse_args()
    
    print(f"\n{'-' * 100}\nInput post:\n{'-' * 100}\n")
    subject = input("Subject: ")
    payload = input("Payload: ")
    print('\n', end='')
    
    filename = args.filename
    num_posts = args.n

    algos = [a for a in args.algs]
    use_spellcheck = args.spell

    posts = similar(filename, subject, payload, num_posts, algos, use_spellcheck)
    print('-' * 100)
    for post_number, p in enumerate(posts): 
        s = f"Post {post_number + 1}:\n" + \
            f"{'-' * 100}\n\n" + \
            f"Subject: {p.subject}\n" + \
            f"Body:\n{p.payload}\n\n" + \
            f"{'-' * 100}\n"
        print(s, end='')
