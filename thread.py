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