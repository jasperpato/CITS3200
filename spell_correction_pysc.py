from spellchecker import SpellChecker
import time

#way better than difflib
def spell_correction(thread):

    thread_list = thread.split()

    spell = SpellChecker()

    misspelled = spell.unknown(thread_list)

    for word in misspelled:

        thread = thread.replace(word, spell.correction(word))

    return thread

def main():

    #this sample run in ~0.18s
    input_text = "Just wondeering hwo we are expected to report termination of backgound processes? Currently I have a simpel implementation printnig to stderr process blah has terminated buut noticed bash initially gives a processs number and prints it and the pid, eg:"

    start = time.time()

    output_text = spell_correction(input_text)

    end = time.time()

    print(output_text)

    print(end-start)
