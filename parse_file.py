import email
import datetime
from itertools import groupby

class Thread:
    def __init__(self):
        self.subject = ""
        self.posts = []
        
class Post:
    def __init__(self):
        self.date = None    # datetime.datetime object
        self.subject = ""
        self.payload = ""
        self.verified = False
        
def parse_file(filename):
    
    threads = []
    
    with open(filename, 'r') as file: # text file must begin with a new line
        
        s = file.read()
            
        posts_strings = ["Date: " + x for x in s.split("\nDate: ")][1:]
        posts = []
        
        for p in posts_strings:
            post = Post()
            
            message = email.message_from_string(p)
            post.payload = message.get_payload()
            
            header = dict(message)
            
            post.date = datetime.datetime.strptime(header["Date"], "%a %b %d %H:%M:%S %Y")
            post.subject = header["Subject"]
            
            post.verified = header["From"] == "chris.mcdonald@uwa.edu.au" # + demonstrators
            
            posts.append(post)
            
    threads = []
    
    for _, post in groupby(sorted(posts, key = lambda x: x.subject), key = lambda x: x.subject):
        threads.append(list(post))
    
    
    for t in threads:
        for p in t:
            print(p.date)
            print(p.subject)
    
    return threads
        

threads = parse_file("help2002/help2002-2017.txt")

    
