"""
This defines a Post class object that stores the relevant information from a post.
This is inovke in the programs parser, where the parser goes through the text file of post
and converts them into the Post class defined here.
"""

from collections import Counter

class Post:
    def __init__(self, date, subject, payload, verified):
        self.date = date    # datetime.datetime object.
        self.subject = subject # the subject of the post, hopefully relating to the post.
        self.payload = payload # The main body of the post. 
        self.verified = verified # A boolean that is TRUE if it is a lab demonstrator or Chris post, else FALSE.

    # This function returns a string with the details of the content the Post class has.
    def __str__(self):
        return f'Date: {self.date}\nSubject: {self.subject}\nVerified: {self.verified}\n\n{self.payload}\n\n'