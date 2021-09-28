from functools import reduce, lru_cache
from string import ascii_letters
from re import sub
import nltk
# in python 3.9 we can just 'da | db'
def merge(da : dict, db : dict) -> dict:
    z = da.copy()
    z.update(db)
    return z

# apply a list of functions LEFT-TO-RIGHT
# e.g. pipe(double, double, increment)(10) = 41
def pipe(*args):
    return lambda x: reduce(lambda y, z:z(y), args, x)

def pipe_weight(x,*args):
    score = 1
    for arg in args:
        score *= arg(x) 
    return score

# memoising a function
# it'd be great if we could get this to memoize in between program executions
def cached(f):

    @lru_cache(maxsize=None)
    def helper(*args):
        return f(*args)

    return helper

def remove_none_alphabet(x):
    return x not in ascii_letters
    
def remove_stopwords(x, stopwords):
    return x in stopwords

def to_lower(x):
    return x.lower()

def space(x):
    return sub(r'\s+', ' ', x)

def stemmer(x):
    stemmer = nltk.stem.snowball.SnowballStemmer("english")
    return stemmer.stem