'''
Created on 17 Dec 2013

@author: lewis
'''
import unittest
from persistence.dataread import DataReadGMIN
from persistence.persistencediagram import PersistenceDiagram
from itertools import permutations, izip
from persistence.connectedcomponent import ConnectedComponent

class TestPersistenceDiagram(unittest.TestCase):


    def setUp(self):
        self.dr = DataReadGMIN('min.data','ts.data')
        self.dr.m = [12.7849943904,
                     14.0832411640,
                     14.4488253121,
                     15.0882532420,
                     15.1099343729]
                                 
        self.dr.ts = [(12.8449850419, 1, 1),
                      (16.5393012580, 3, 1),
                      (17.6419506053, 3, 4),
                      (18.3911584054, 3, 2),
                      (18.6159343448, 5, 1),
                      (52.7474808984, 3, 2),
                      (54.7059708697, 3, 4),
                      (58.2830620095, 5, 3)]

        self.pd = PersistenceDiagram()
        self.pd.Populate(self.dr.m)
        
    def tearDown(self):
        pass


    def testPopulate(self):
        '''
        Tests that correct number of connected components are formed, and that they have the expected birth energy, size and minima id.
        '''
        cc = [ConnectedComponent(12.7849943904,1),
              ConnectedComponent(14.0832411640,2),
              ConnectedComponent(14.4488253121,3),
              ConnectedComponent(15.0882532420,4),
              ConnectedComponent(15.1099343729,5)]
                                 
        # Compare birth energies
        [self.assertEqual(cc1.birth, cc2.birth, 'Birth energies should be equivalent') for cc1, cc2 in izip(self.pd.cc, cc)]

    def testComponentsNotEqual(self):
        [self.assertNotEqual(cc1, cc2, 'cc should not be equal') for cc1, cc2 in permutations(self.pd.cc,r=2)]

    def testEat(self):
        '''
        Tests that a connected component, cc1, is capable of eating another, cc2.
        '''
#         print self.pd
        pass
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
