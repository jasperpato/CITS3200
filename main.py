import sys
from parse_file import *
from thread import Thread
from post import Post
from algorithm import find_similar_posts

if __name__=="__main__":
    threads = parse_file(sys.argv[1])
    new_post = Post()
    print("Enter a new post and view the most similar existing posts.")
    new_post.subject = input("Subject: ")
    new_post.payload = input("Question body: ")
    for p in find_similar_posts(new_post):
        print(p)
    


