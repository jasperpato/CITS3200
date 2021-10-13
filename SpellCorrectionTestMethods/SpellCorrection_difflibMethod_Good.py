import time
import difflib

"""Currently the best spell correction algorithm, uses method "SequenceMatcher"
 from "difflib" library to find how similar words are"""

#Quite accurate
#Would be optimal to increase speed
#Speed could be increased by ordering "LiterallyEveryWord" file by occurance so that common words are looked at first 

def spellCheck(seq):
    
    f = open("LiterallyEveryWord.txt", "r")

    words = f.readlines()

    f.close()

    for i in range(0, len(words)):

        words[i] = words[i].strip()

    one = [1]*len(words)

    wordDict = dict(zip(words, one))

    # inp = open("InputText.txt", "r")

    # text = inp.readline().split()

    # inp.close()

    bestDist = 0

    bestWord = ""

    start = time.time()

    out = []
    for totest in seq:

        #starts = time.time()
        #ignores "words" that are not only letters
        if not totest.isalpha():
            out.append(totest)
            continue

        bestDist = 0

        bestWord = ""

        
        #checks dict of words to check for exact match
        if wordDict.get(totest, -1) == 1:

            bestDist = 1
            bestWord = totest

            #ends = time.time()

            #print(ends-starts)

            #print(bestDist)
            out.append(bestWord)
            continue


        for word in words:

            #returns a value between 0 and 1 depending on how similar words are
            currDist = difflib.SequenceMatcher(None,totest.lower(), word).ratio()

            if currDist == 1:

                bestDist = 1
                bestWord = word

                break

            if currDist > bestDist:

                bestDist = currDist
                bestWord = word

                #print(bestDist)
                #print(bestWord)

        #ends = time.time()

        #print(ends - starts)

        #print(bestDist)
        out.append(bestWord)

    end = time.time()
    print(end - start)
    return out
