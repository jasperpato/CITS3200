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

The main point of entry to this program is the function similar() in
similarity.py. However, the design is as modular as possible to allow the user
to alter their usage as needed.

The different algorithms for similarity scoring are Cosine, Jaccard,
Term Frequency–Inverse Document Frequency (TFIDF), and Universal Sentence
Encoder (USE). These can be chosen individually, or used together and averaged.
Based on manual tagging tests, our recommendation is to use the default option
of TFIDF for calculating similarity scores between posts.







