from similarity import similar

if __name__=="__main__":

    filename = "data_files/help2002-2017.txt"
    subject = "Lab5"
    payload = "What is it?"
    n       = 6

    posts = similar(filename, subject, payload, n)

    for p in posts: print(str(p))