from spellchecker import SpellChecker

def main():

    spell = SpellChecker()

    inp = open("InputText.txt", "r")

    text = inp.readline().split()

    output = " ".join(text)

    inp.close()

    misspelled = spell.unknown(text)

    for word in misspelled:

        print(word)

        output = output.replace(word, spell.correction(word))

    print(output)
