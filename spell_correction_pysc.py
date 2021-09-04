from spellchecker import SpellChecker
import time

#way better than difflib
def spell_correction(thread):

    thread_list = thread.split()

    numeric = []

    for i in range(0, len(thread_list)):

        #removes punctuation for spell correction
        #if punctuation needs to be removed for output then do this before return
        thread_list[i] = thread_list[i].strip("""!@#$%^&*()_+-={}[]|\~`:;"'<,>.?/""")

        #marks words with numbers in them for removal
        if not thread_list[i].isalpha():

            numeric.append(i)

    #removes words with numbers in them
    for i in numeric:
        thread_list.pop(i)
    
    #takes ~0.09s for this line to run, should initialize it once instead of for every thread
    spell = SpellChecker()

    #Library seems to already ignore capitialisation
    misspelled = spell.unknown(thread_list)

    for word in misspelled:

        thread = thread.replace(word, spell.correction(word))

    return thread

def main():

    #this sample run in ~0.18s
    input_text = """Juust wondeering hwo we 5are expEcted to repOrt termination oF backGROUND CASR casr processes? Currently I have a simpel implementation printnig to stderr "process blah has terminated" buut noticed bash initially gives a processs number and prints it and the pid, eg:"""
    print(input_text)
    start = time.time()

    output_text = spell_correction(input_text)

    end = time.time()

    print(output_text)

    print(end-start)
