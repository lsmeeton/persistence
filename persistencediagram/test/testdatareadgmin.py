'''
Created on 16 Dec 2013

@author: lewis
'''
import unittest
from persistencediagram.datareadgmin import DataReadGMIN

class Test(unittest.TestCase):


    def setUp(self):
        self.dr = DataReadGMIN('min.data','ts.data')
        self.dr.m = 


    def tearDown(self):
        pass


    def test(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()