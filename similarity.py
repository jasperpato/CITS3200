"""
This is one of the scripts to run our project, however this has been abandoned for the pipeline.py.
To use the code enter this code into the command line:

python3 main.py [text_data_file_with_posts]

The system will prompt you to write a subject and body of text.
Then it wil lreturn 3 of the most similiar post.
"""
import sys
from parse_file import parse_file
from similarity_algorithms.cosine import cosine_similarity
from thread_obj import Thread
from post import Post
from pipeline import pipeline
import nltk
from re import sub
from string import ascii_letters
from weights import verified_weight, date_weight
from utils import remove_none_alphabet, remove_stopwords, to_lower
nltk.download('punkt')
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')

def similarity(filename, post_subject, post_text, N=3):
    threads = parse_file(filename)
    
    new_post = Post(None,post_subject,post_text,None)
    W = 0.2 # weight of subject similarity, payload weight is (1.0 - W)

    filters = (  remove_none_alphabet, # take non-alphabetical words out
                remove_stopwords)          # remove stopwords


    #weights = [ lambda x: 1.5 if x.verified else 1.0]   # give a bit more priority to Chris' posts
    weights = [verified_weight, date_weight] #uses the functions from the weights.py script
    
    cleaners =    ( to_lower,              # lowercase all text
                    lambda x: sub(r'\s+', ' ', x))

    substitutes = tuple([])

    from similarity_algorithms.tfidf import Tfidf

    algorithms = (cosine_similarity, Tfidf().similarity)

    return [p for p in pipeline(new_post, threads, cleaners, filters, substitutes,  weights, algorithms, W, N)]

if __name__ == "__main__":
    
    if len(sys.argv) < 3: exit()
    filename = sys.argv[1]
    N = int(sys.argv[2])
    subject = input("Subject: ")
    payload = input("Payload: ")
    
    posts = similarity(filename, subject, payload, N)
    for p in posts: print(f"{p.subject}\n{p.payload}\n")
