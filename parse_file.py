import email
import datetime

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
            
        posts = ["Date: " + x for x in s.split("\nDate: ")][1:]
        
        thread = Thread()
        
        for p in posts:
            post = Post()
            
            message = email.message_from_string(p)
            post.payload = message.get_payload()
            
            header = dict(message)
            
            post.date = datetime.datetime.strptime(header["Date"], "%a %b %d %H:%M:%S %Y")
            post.subject = header["Subject"]
            
            post.verified = header["From"] == "chris.mcdonald@uwa.edu.au" # + demonstrators
            
            if thread.subject == "" or post.subject == thread.subject:
                thread.subject = post.subject
                thread.posts.append(post)
            
            else:
                threads.append(thread)
                thread = Thread()
                thread.subject = post.subject
                thread.posts.append(post)
                
    return threads # list of Thread objects

#parse_file("~/desktop/computing/help2002/help2002-2017.txt")
            
    
