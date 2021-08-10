from re import sub
import nltk
from sys import argv
from typing import List

nltk.download('punkt')
nltk.download('stopwords')

def clean(txt : str) -> str:
    txt = sub('[^a-zA-Z]', ' ', txt)
    txt = sub(r'\s+', ' ', txt)
    return txt

def preprocess(txt : str) -> List[str]:
    # clean, tokenise, filter stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    return list(filter(lambda w: w not in stopwords, nltk.word_tokenize(clean(txt).lower())))

if __name__ == "__main__":
    if(len(argv) >= 2):
        # passing text by stdin
        print(preprocess(''.join(argv[1:])))
    else:
        print("Need to enter text to preprocess")