import email
import datetime
from itertools import groupby

class Thread:
    def __init__(self, subject, posts):
        self.subject = subject
        self.posts = posts
        
class Post:
    def __init__(self, date, subject, payload, verified):
        self.date = date    # datetime.datetime object
        self.subject = subject
        self.payload = payload
        self.verified = verified

# expand this with other demonstrators
valid = set(["chris.mcdonald@uwa.edu.au"])

def parse_post(post_str): 
    message = email.message_from_string(post_str)
    header = dict(message)

    date = datetime.datetime.strptime(header["Date"], "%a %b %d %H:%M:%S %Y")
    subject = header["Subject"]
    payload = message.get_payload()
    verified = header["From"] in valid

    return Post(date,subject,payload,verified)

def group(posts):
    sub = lambda x: x.subject
    return [Thread(subject, list(posts)) for subject, posts in
                    groupby(sorted(posts, key = sub), key = sub)]

def parse_file(filename):
    with open(filename, 'r') as file:
        s = file.read()
        post_strings = ["Date: " + x for x in s.split("Date: ")][1:]
        posts = [parse_post(s) for s in post_strings]
        
    return group(posts)