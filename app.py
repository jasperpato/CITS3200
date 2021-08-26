# python -m flask run 

from flask import Flask, request
from post import Post
from parse_file import parse_file
from algorithm import pipe_line, process_post
from re import sub
from string import ascii_letters
import nltk
import time

app = Flask("Evaluator")

files = ['help2002-2017.txt', 'help2002-2018.txt', 'help2002-2019.txt']
all_threads = [parse_file(f) for f in files]

nltk.download('punkt')
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')

##################### cleaners ######################################

lower = lambda x: x.lower()
space = lambda x: sub(r'\s+', ' ', x)

##################### Filters ######################################

not_ascii = lambda x: x not in ascii_letters
stopword = lambda x: x in stopwords

##################### substitutes ######################################
stemmer = nltk.stem.snowball.SnowballStemmer("english")
stem = stemmer.stem

#################### Weights #######################################

# weight by y on post x
verified = lambda y: lambda x: y if x.verified else 1.0

########################

page = """
            <style>
                aside{
                    float: left;
                    width: 30%;
                    background-color: #f1f1f1;
                }

                article{
                    float: right;
                    width: 70%;
                    background-color: #f1f1f1;
                }

                scrollbox{
                    overflow:scroll
                }

            </style>
        
            <aside>
                <form method="GET" action="/search" id="new_post">
                    <label for="subject">Subject</label>
                    <br>
                    <input type=text name=subject>
                    <br>
                    <label for="payload">Payload</label>
                    <br>
                    <textarea name="payload" form="new_post" rows=5 cols=50></textarea>
                    <br>
                    <label for="nposts">Number of posts</label>
                    <br>
                    <input type=number name=nposts min="1" value="5" max="10">
                    <br>
                    <input type="radio" id="2017" name="year" value="0" checked>
                    <label for="2017">help2002-2017.txt</label><br> 
                    <input type="radio" id="2018" name="year" value="1">
                    <label for="2018">help2002-2018.txt</label><br> 
                    <input type="radio" id="2019" name="year" value="2">
                    <label for="2019">help2002-2019.txt</label><br>

                    <input type="checkbox" id="lower" name="lower" checked>
                    <label for="lower">search with lowercase</label><br> 

                    <input type="checkbox" id="space" name="space" checked>
                    <label for="space">remove extraneous spaces</label><br> 

                    <input type="checkbox" id="ascii" name="ascii" checked>
                    <label for="ascii">limit search to non-ascii</label><br>

                    <input type="checkbox" id="stopwords" name="stopwords" checked>
                    <label for="stopwords">filter out stopwords</label><br>

                    <input type="checkbox" id="stem" name="stem" checked>
                    <label for="stem">Apply stemming</label><br>

                    <input type=number name="weight" min="1" value="1">
                    <label for="weight">scaling applied to Chris' posts</label><br>
                    <input type=submit value=Yall>
                </form>
                </aside>
                """

@app.route("/search")
def search():
    time_start = time.time()
    post = Post(None, request.args['subject'], request.args['payload'], None)
    threads = all_threads[int(request.args['year'])]
    
    nposts = int(request.args['nposts'])
    cleaners = []
    if('lower' in request.args): cleaners.append(lower)
    if('space' in request.args): cleaners.append(space)
    
    filters = []
    if('ascii' in request.args): filters.append(not_ascii)
    if('stopwords' in request.args): filters.append(stopword)

    substitutes = []
    if('stem' in request.args): substitutes.append(stem)

    weights = []
    weights.append(verified(float(request.args['weight'])))
    
    posts = pipe_line(post, threads, tuple(cleaners), tuple(filters), tuple(substitutes), weights, nposts)

    ########## DEBUG
    print(process_post(post, cleaners, filters, substitutes))
    for p in posts:
        print(process_post(p, cleaners, filters, substitutes))
    ############

    time_taken = time.time() - time_start
    return page + f"<article><h3>{time_taken} seconds</h3><br><h2>Subject: {request.args['subject']}<br>Payload: {request.args['payload']}</h2><ul>" + "".join(["<li>{0}</li><br>".format(str(p).replace('\n', '<br>')) for p in posts])+ "</ul>"

@app.route("/")
def main():
    return page 