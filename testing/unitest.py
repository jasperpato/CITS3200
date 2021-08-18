from itertools import chain
import json 
import unittest
import datetime
import parse_file
import tokeniser
import algorithm
from post import Post

class testConfig():
    pass


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


class TokeniserCase(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_clean(self):
        text1 = 'JDJ2$x@esL'
        test_str = 'JDJ x esL'
        tbt_str = tokeniser.clean(text1)
        self.assertEqual(test_str, tbt_str)
        text2 = ''.join([str(i) for i in range(0, 255)])
        test_str = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz '
        tbt_str = tokeniser.clean(text2)
        self.assertTrue(test_str, tbt_str)

    def test_preprocess(self):
        text = 'Greeting, traveller. Will you save the dog stuck in the well?'
        test_tokens = ['greeting', 'traveller', 'save', 'dog', 'stuck', 'well']
        tbt_tokens = tokeniser.preprocess(text)
        self.assertEqual(test_tokens, tbt_tokens)


class AlgorithmTestCase(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_find_similar_posts(self):
        threads = parse_file.parse_file('help2002-2019.txt')
        input = threads[0].posts[0]
        num_posts = 10
        similar_posts = algorithm.find_similar_posts(input, threads, num_posts, True)
        self.assertEqual(num_posts, len(similar_posts))
        self.assertTrue(all(type(x) is Post for x in similar_posts))


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

if __name__=='__main__':
    unittest.main(verbosity=2)

