# python -m flask run 

from flask import Flask, request
from post import Post
from parse_file import parse_file
from algorithm import find_similar_posts

app = Flask("Evaluator")

threads = []
for path in ['help2002-2017.txt', 'help2002-2018.txt', 'help2002-2019.txt']:
    threads.append(parse_file(path))

@app.route("/", methods=["GET", "POST"])
def main():

    css = """
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
        """

    form =  """
                <aside>
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
                    <input type="radio" id="2017" name="year" value="0">
                    <label for="2017">help2002-2017.txt</label><br> 
                    <input type="radio" id="2018" name="year" value="1">
                    <label for="2018">help2002-2018.txt</label><br> 
                    <input type="radio" id="2019" name="year" value="2">
                    <label for="2019">help2002-2019.txt</label><br> 
                    <input type=submit value=Yall>
                </form>
                </aside>
        """
    if(request.method == "GET"):
        return css + form
    else:
        post = Post(None, request.form['subject'], request.form['payload'], None)
        posts =  "<ul>" + "".join(["<li>"+str(p).replace('\n', '<br>')+"</li>"
                    for p in find_similar_posts(post, threads[int(request.form['year'])], int(request.form['nposts']), False)]) + "</ul>"
        return css + form + "<article>" + posts + "</article>" +  "<aside><h2>Subject: </h2><h3>{0}</h3><br><h2>Payload: </h2><h3>{1}</h3><br></aside>".format(request.form['subject'], request.form['payload'])