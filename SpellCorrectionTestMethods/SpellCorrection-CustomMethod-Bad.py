import time

"""Garbage method not based on any algorithm just to see what would be required
 for the algorithm and to give a baseline to compare accuracy and speed of other algorithms"""

#Not very accurate
#Accuracy can be increased by accounting for the order of letters which is not yet done

def similarity(inputWord, dictWord):

    count = 0

    for inputChar in inputWord:

        for dictChar in dictWord:

            if inputChar == dictChar:

                count+= 1
                #favours words that share the same letters

    count+= -1*abs(len(inputWord) - len(dictWord))
    #favours words that are similar lengths

    return count

def main():

    f = open("LiterallyEveryWord.txt", "r")

    words = f.readlines()

    f.close()

    inp = open("InputText.txt", "r")

    text = inp.readline().split()

    inp.close()

    bestDist = 0

    bestWord = ""

    for totest in text:

        start = time.time()
        #ignores "words" that are not only letters
        if not totest.isalpha():

            continue

        bestDist = 0

        bestWord = ""

        for word in words:

            #Ignore the use of dist, in this case it's how similar the words are
            currDist = similarity(list(totest.lower()), list(word))

            if currDist > bestDist:

                bestDist = currDist
                bestWord = word

                #print(bestDist)
                #print(bestWord)

        end = time.time()

        print(end - start)

        print(bestDist)
        print(bestWord)

