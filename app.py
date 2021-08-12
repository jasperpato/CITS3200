# python -m flask run 

from flask import Flask, request
from post import Post
from parse_file import parse_file
from algorithm import find_similar_posts

app = Flask("Evaluator")

threads = parse_file('help2002-2017.txt')

@app.route("/", methods=["GET", "POST"])
def main():
    form =  """
            <h1>Enter a new post</h1>
            <form method="post" action="/" id="new_post">
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
                <input type=number name=nposts>
                <br>
                <input type=submit value=Yall>
            </form>
        """
    if(request.method == "GET"):
        return form
    else:
        post = Post(None, request.form['subject'], request.form['payload'], None)
        return form + "<ul>" + "".join(["<li>"+str(p).replace('\n', '<br>')+"</li>"
                    for p in find_similar_posts(post, threads, int(request.form['nposts']), False)]) + "</ul>"