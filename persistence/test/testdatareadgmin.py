'''
Created on 16 Dec 2013

@author: lewis
'''
import unittest
from persistence.datareadgmin import DataReadGMIN

class Test(unittest.TestCase):


    def setUp(self):
        self.dr = DataReadGMIN('min.data','ts.data')
        self.testdr = DataReadGMIN('min.data','ts.data')
        self.testdr.m = [14.4488253121,
                         14.0832411640,
                         12.7849943904,
                         15.0882532420,
                         15.1099343729,
                         19.0802277948]
                                 
        self.testdr.ts = [(18.3911584054, 1, 2),
                          (18.6159343448, 5, 3),
                          (58.2830620095, 5, 1),
                          (12.8449850419, 3, 3),
                          (16.5393012580, 1, 3),
                          (52.7474808984, 1, 2),
                          (54.7059708697, 1, 4),
                          (17.6419506053, 1, 4)]


    def tearDown(self):
        pass

    def testFileNames(self):
        self.assertEqual(self.dr.min_file,   self.testdr.min_file, 'File names inexplicably different')
        self.assertEqual(self.dr.ts_file,   self.testdr.ts_file, 'File names inexplicably different')
        
    def testReadMinima(self):
        self.dr.ReadMinima()
        self.assertEqual(self.testdr.m, self.dr.m , "Minima have not been read from file correctly")

    def testReadTransitionStates(self):
        self.dr.ReadTransitionStates()
        self.assertEqual(self.testdr.ts, self.dr.ts , "Transition States have not been read from file correctly")
        
    def testOrderMinima(self):
        self.dr.ReadMinima()        
        self.dr.ReadTransitionStates()
        self.dr.OrderStationaryPoints()
        self.testdr.m = [12.7849943904,
                         14.0832411640,
                         14.4488253121,
                         15.0882532420,
                         15.1099343729,
                         19.0802277948]
        try:
            self.assertEqual(self.dr.m, self.testdr.m, "Minima not sorted correctly")
        except AssertionError as e:
            print e
            print self.dr.m
            print self.testdr.m
            raise AssertionError
        
    def testOrderTransitionStates(self):
        self.dr.ReadMinima()        
        self.dr.ReadTransitionStates()
        self.dr.OrderStationaryPoints()
        self.testdr.ts = [(18.3911584054, 3, 2),
                          (18.6159343448, 5, 1),
                          (58.2830620095, 5, 3),
                          (12.8449850419, 1, 1),
                          (16.5393012580, 3, 1),
                          (52.7474808984, 3, 2),
                          (54.7059708697, 3, 4),
                          (17.6419506053, 3, 4)]
        try:
            self.assertEqual(self.dr.ts, self.testdr.ts, "Transition States not sorted correctly")
        except AssertionError as e:
            print e
            print self.dr.ts
            print self.testdr.ts
            raise AssertionError
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
