import time

#This is the funtion that performs the spell correction.
#It requires the spell library and the thread as input and it will 
#Return a thread that have non, or minimal, spelling errors.
def spell_correction(thread, spell):
    misspelled = spell.unknown([thread])
    if misspelled !=[]:
        thread = spell.correction(thread)
    return thread

#This main function is just a test function to test the speed of the spell correction
#Not actually used in the main project
def main():
    #this sample run in ~0.18s
    input_text = """Just wondeering hwo we 5are expected to report termination of backgound processes? Currently I have a simpel implementation printnig to stderr "process blah has terminated" buut noticed bash initially gives a processs number and prints it and the pid, eg:"""
    start = time.time()
    output_text = spell_correction(input_text)
    end = time.time()
    print(output_text)
    print(end-start)
