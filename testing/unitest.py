import json 
import unittest

class testConfig():
    pass

class fileParseCase(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_parse():
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(fileParseCase('test_parse'))
    return suite

if __name__=='__main__':
    unittest.main(verbosity=2)