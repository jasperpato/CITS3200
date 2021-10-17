This program returns posts from an input file that are similar to an input post.
See help2002-2017.txt for an example of the input file of posts.

To use the program right away:

1. Clone this repository using
> git clone https://github.com/jasperpato/CITS3200.git

2. (optional) Create a python virtual environment
> python3 -m venv venv

3. (optional) Enter the virtual environment
> source venv/bin/activate

4. Navigate to CITS3200 directory
> cd CITS3200

5. Download requirements
> python3 -m pip install -r requirements.txt

6. Run example program
> python3 similarity.py

The different algorithms for similarity scoring are Cosine, Jaccard,
Term Frequency–Inverse Document Frequency (TFIDF), and Universal Sentence
Encoder (USE). These can be chosen individually, or used together and averaged.
Based on manual tagging tests, our recommendation is to use the default option
of TFIDF for calculating similarity scores between posts.

The intended usage is to call similar() from an outer program. The signature is:
similar(filename,subject,payload,algos=[Tfidf],N=3,use_spellcheck=False,W=0.1):

Filename is the name of the txt file that contains a series of posts in rfc2822
format.

Subject and payload are strings containing the subject and payload text of an
input post for which similar posts are to be found.

Algos is a list of similarity algorithms to be used. It can contain any
combination of [Cosine, Jaccard, Tfidf, Use].

N is the number of similar posts to be returned.

Use_spellcheck specifies
whether to implement spell correction during pre-processing. It can yield more
accurate results, however takes more time.

For each post a subject similarity and payload similarity are calculated
separately. W is a weighting between 0 and 1 given to the subject similarity.
The payload similarity will be given a weighting of (1-W). It is recommended
not to alter W from the default value of 0.1.

Import this function into your python program by including this statement:
from CITS3200.similarity import similar







