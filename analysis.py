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

# intend to use this file as a CLI tool 
if __name__ == "__main__":
    plot_word_freq(parse_file(argv[1]))