"""
The utils.py has functions to facillitate the running of our web testing site for our project. 
This is setup in a way where we just need to specify the order of functions to run in the pipe() function
and the program will run them in that order, carrying the results through,
Other function such as pipe weight and merge help to format data that will be used in the pipe.
"""
from functools import reduce, lru_cache
from string import ascii_letters

# This function merges two dictionary together.
# Returns a dictionary that has combined entries from dictionary a (da)
# and dictionary b (db).
def merge(da : dict, db : dict) -> dict:
    z = da.copy()
    z.update(db)
    return z

# apply a list of functions LEFT-TO-RIGHT.
# e.g. pipe(double, double, increment)(10) = 41.
# Returns a list of scores after passing the input through all the functions in the parameters.
def pipe(*args):
    return lambda x: reduce(lambda y, z:z(y), args, x)

#This function helps to carry the score over from one function in weight.py to the other.
#This will return the score after checking if the post is recent and verified.
def pipe_weight(x,*args):
    score = 1
    for arg in args:
        score *= arg(x) 
    return score

# This function caches the result from a function
# This is mainly used to help speed up our program
def cached(f):

    @lru_cache(maxsize=None)
    def helper(*args):
        return f(*args)

    return helper

#removes any alphabets not in ascii from the string.
def remove_none_alphabet(x):
    return x not in ascii_letters

#removes any stopwords (i,me,myself...) from the string.
def remove_stopwords(x, stopwords):
    return x in stopwords

#Sets all letters in the string to lower case.
def to_lower(x):
    return x.lower()

