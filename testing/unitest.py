import json 
import unittest
import datetime
import parse_file
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

