from similarity import similar

if __name__=="__main__":

    filename = "help2002-2017.txt"
    subject = "Lab5"
    payload = "What is it?"

    posts = similar(filename, subject, payload)
    
    for p in posts: print(str(p))