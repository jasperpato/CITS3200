import email
import datetime
from itertools import groupby

class Thread:
    def __init__(self, subject, posts):
        self.subject = subject
        self.posts = posts
        
    def __str__(self):
        thread_str = ""
        for p in self.posts:
            thread_str += str(p)
            if p is not self.posts[-1]:
                thread_str += '\n'
        return thread_str
        
class Post:
    def __init__(self, date, subject, payload, verified):
        self.date = date    # datetime.datetime object
        self.subject = subject
        self.payload = payload
        self.verified = verified

    def __str__(self):
        return f'Date: {self.date}\nSubject: {self.subject}\nVerified: {self.verified}\n\n{self.payload}\n\n'

# expand this with other demonstrators
valid = set(["chris.mcdonald@uwa.edu.au"])

def parse_post(post_str): 
    message = email.message_from_string(post_str)
    header = dict(message)

    date = datetime.datetime.strptime(header["Date"], "%a %b %d %H:%M:%S %Y")
    subject = header["Subject"]
    payload = message.get_payload().strip()
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

def print_threads(threads):
    for num, t in enumerate(threads):
        title = " Thread " + str(num) + ' '
        spaces = '-' * ((60 - len(title)) // 2)
        print("\n\n" + spaces + title + spaces + '\n')
        print(str(t))
        print('-' * 60 + '\n')
            
threads = parse_file("help2002-2017.txt")
print_threads(threads)
