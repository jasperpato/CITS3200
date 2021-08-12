"""
Basic visualisation and data analysis tools
"""

import numpy as np
import matplotlib.pyplot as plt
from parse_file import parse_file
from thread import Thread, all_posts
from typing import List
from thread import Thread
from itertools import chain
from sys import argv
from collections import Counter
from tokeniser import preprocess

# ew, sorry im bad with stats stuff - can someone come up with some smarter graphs?
def plot_word_freq(threads : List[Thread]):
   freqs = sorted(Counter(chain(*[preprocess(p.payload) for p in all_posts(threads)])).values())
   plt.hist(freqs, bins=500) # dunno mang
   plt.show()

def words_n_occurences(threads : List[Thread], n : int) -> List[str]:
    p = [(k,v) for k,v in Counter(chain(*[preprocess(p.payload) for p in all_posts(threads)])).items() if v > 100]
    p.sort(key=lambda x: x[1], reverse=True)
    return [k for k,v in p]

# intend to use this file as a CLI tool 
if __name__ == "__main__":
    threads = parse_file(argv[1])
    print(words_n_occurences(threads, 50)) # words that appear more than 50 times