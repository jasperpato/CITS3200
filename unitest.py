"""
This script contains the unittest to test out the different functions required in our project.
"""
from itertools import chain
import json
from os import remove 
from spellchecker import SpellChecker
import unittest
import datetime
import parse_file
from testing.parse_spell_test import remove_one_letter, replace_one_letter
from spell_correction_pysc import spell_correction
from utils import remove_none_alphabet, remove_stopwords, to_lower
import algorithms
from post import Post

class testConfig():
    pass

# Unit test for the parse_file.py
# Expect the script to succsessful extract and organise data from a text file
# All output should be in a list belonging to class Post
class FileParseCase(unittest.TestCase):
    def setUp(self):
        self.f = open('help2002-2019.txt')
        s = self.f.read()
        self.post_strings = ['Date: ' + x for x in s.split('Date: ')][1:]
        return super().setUp()

    def tearDown(self):
        self.f.close()
        return super().tearDown()

    def test_parse_post(self):
        for post in self.post_strings:
            test_post = manual_post_parse(post)
            tbt_post = parse_file.parse_post(post)
            self.assertEqual(test_post.date, tbt_post.date)
            self.assertEqual(test_post.subject, tbt_post.subject)
            self.assertEqual(test_post.payload, tbt_post.payload)
            self.assertEqual(test_post.verified, tbt_post.verified)
    
    def test_parse_file(self):
        threads = parse_file.parse_file('help2002-2019.txt')
        for thread in threads:
            self.assertTrue(all(post.subject == thread.posts[0].subject for post in thread.posts))
        posts = [manual_post_parse(post) for post in self.post_strings]
        test_subject_set = set([post.subject for post in posts])
        tbt_subject_set = set([thread.subject for thread in threads])
        self.assertEqual(test_subject_set, tbt_subject_set)



# Unit test for the spell_correction_pysc.py
# expected to successfully correct any mispelling
# either by adding, removing or changing words.
class SpellcheckTestCase(unittest.TestCase):
    def setUp(self):
        self.spellchecker = SpellChecker()
        with open("./testing/commonWords.txt") as f:
            read_data = f.read().split("\n")
            self.one_letter_removed,self.one_letter_orig = remove_one_letter(read_data)
            self.one_letter_replaced,self.one_replace_orig = replace_one_letter(read_data)
            f.close
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()

    def test_letter_missing(self):
        result = []
        result2 = []
        print(spell_correction("hapenning", self.spellchecker))
        for this in self.one_letter_removed:
            result.append(spell_correction(this, self.spellchecker)) 
        for this in self.one_letter_orig:
            result2.append(spell_correction(this, self.spellchecker)) 
        
        print(f"one letter removed :         {self.one_letter_removed}")
        print(f"orig :                       {self.one_letter_orig}")
        print("one letter diff spellcheck length:", len(result), "origional spellcheck length: ", len(result2))
        print("one letter diff spellcheck: ",result[0])
        print("orig spellcheck:            ", result2)
        self.assertTrue(len(result) == len(result2))
        diff = 0
        for item in result:
            if item not in result2:
                diff +=1 
        score = 1-(diff / len(result))
        print("score: ",score)
        self.assertTrue(score >= 0.8)
    
    def test_letter_replaced(self):
        result = []
        result2 = []
        print(spell_correction("hapenning", self.spellchecker))
        for this in self.one_letter_replaced:
            result.append(spell_correction(this, self.spellchecker)) 
        for this in self.one_replace_orig:
            result2.append(spell_correction(this, self.spellchecker)) 
        
        print(f"one letter removed :         {self.one_letter_replaced}")
        print(f"orig :                       {self.one_replace_orig}")
        print("one letter diff spellcheck length:", len(result), "origional spellcheck length: ", len(result2))
        print("one letter diff spellcheck: ",result[0])
        print("orig spellcheck:            ", result2)
        self.assertTrue(len(result) == len(result2))
        diff = 0
        for item in result:
            if item not in result2:
                diff +=1 
        score = 1-(diff / len(result))
        print("score: ",score)
        self.assertTrue(score >= 0.8)

# Unit test to test the functions in util.py
# This mainly tested whether utils successfully removes symbols that are not alphabets
class UtilityTestCase(unittest.TestCase):

    def test_remove_non_alph(self):
        text1 = 'JDJ2$x@esL'
        text2 = ' ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '
        self.assertTrue(remove_none_alphabet(text1))
        self.assertFalse(remove_none_alphabet(text2))
        
    def test_weight(self):
        pass

def manual_post_parse(post):
    post_lines = post.split('\n')
    date_str = post_lines[0][6:]
    date = datetime.datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
    payload = '\n'.join(post_lines[8:]).strip()
    subject = post_lines[3][9:]
    author = post_lines[4][6:]
    verified = author in parse_file.valid
    return Post(date, subject, payload, verified)
        

def suite():
    suite = unittest.TestSuite()
    suite.addTest(FileParseCase('test_parse'))
    return suite

# Main coomand to run the test
if __name__=='__main__':
    unittest.main(verbosity=2)

