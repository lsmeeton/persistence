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
        
        self.testcc = [ConnectedComponent(12.7849943904,1),
                       ConnectedComponent(14.0832411640,2),
                       ConnectedComponent(14.4488253121,3),
                       ConnectedComponent(15.0882532420,4),
                       ConnectedComponent(15.1099343729,5)]
        
        self.pd = PersistenceDiagram()
        self.pd.Populate(self.dr.m)
        
    def tearDown(self):
        pass


    def testPopulate(self):
        '''
        Tests that correct number of connected components are formed, and that they have the expected birth energy, size and minima id.
        '''
                                 
        # Test birth energies
        [self.assertEqual(cc1.birth, cc2.birth, 'Birth energies should be equivalent') for cc1, cc2 in izip(self.pd.cc, self.testcc)]
        
        # Test minima contents
        [self.assertEqual(cc1.m, cc2.m, 'Minima contents should be equivalent') for cc1, cc2 in izip(self.pd.cc, self.testcc)]
        
        # Test cc size
        [self.assertEqual(cc1.size, cc2.size, 'Connected Component size should be equivalent') for cc1, cc2 in izip(self.pd.cc, self.testcc)]

    def testComponentsNotEqual(self):
        [self.assertNotEqual(cc1, cc2, 'cc should not be equal') for cc1, cc2 in permutations(self.pd.cc,r=2)]

    def testEat(self):
        '''
        Tests that a connected component, cc1, is capable of eating another, cc2.
        '''
        cc1 = ConnectedComponent(12.7849943904,1)
        cc1.m.append(3)
        cc1.size = 2
        
        cc2 = ConnectedComponent(14.4488253121,3)
        cc2.death = 16.5393012580
        cc2.eatenby = cc1
        
        self.pd.cc[0].Eat(self.pd.cc[2], 16.5393012580)
        
        self.assertDictEqual(self.pd.cc[0].__dict__, cc1.__dict__, 'Connected Component not eaten correctly')
        
        # Dictionaries will be different because they will point to different (though identical)
        # cc objects in eatenby
        
        d1 = self.pd.cc[2].__dict__
        d2 = cc2.__dict__
        
        for d in [d1,d2]: del d['eatenby']
        
        self.assertDictEqual(d1, d2, 'Connected Component not BEEN eaten correctly')
        
    def testEvaluate(self):
        '''
        Test that correct (ie. cc containing lowest energy minimum) eats the other
        '''
        cc1 = ConnectedComponent(12.7849943904,1)
        cc1.m.append(3)
        cc1.size = 2
        
        cc2 = ConnectedComponent(14.4488253121,3)
        cc2.death = 16.5393012580
        cc2.eatenby = cc1
        
#         self.pd.cc[0].Eat(self.pd.cc[2], 16.5393012580)
        self.pd.Evaluate(self.dr.ts[1])
        
        self.assertDictEqual(self.pd.cc[0].__dict__, cc1.__dict__, 'Connected Component not eaten correctly')
        
        # Dictionaries will be different because they will point to different (though identical)
        # cc objects in eatenby
        
        d1 = self.pd.cc[2].__dict__
        d2 = cc2.__dict__
        
        for d in [d1,d2]: del d['eatenby']
        
        self.assertDictEqual(d1, d2, 'Connected Component not BEEN eaten correctly')
        
    def testEvaluateDegenerate(self):
        '''
        Test that if a transition state is degenerate (points to one minimum twice) nothing happens
        '''
        cc1 = ConnectedComponent(12.7849943904,1)
        
        self.pd.Evaluate(self.dr.ts[0])
        
        self.assertDictEqual(self.pd.cc[0].__dict__, cc1.__dict__, 'Connected Component not eaten correctly')
        
    def testPersistenceDiagramConstruction(self):
        '''
        Test that a model persistence diagram can be created correctly
        '''
        cc1 = ConnectedComponent(12.7849943904,1)
        cc1.m += [3,4,2,5]
        cc1.size = 5
        
        cc2 = ConnectedComponent(14.0832411640,2)
        cc2.death = 18.3911584054
        cc2.eatenby = cc1
                
        cc3 = ConnectedComponent(14.4488253121,3)
        cc3.death = 16.5393012580
        cc3.eatenby = cc1
        
        cc4 = ConnectedComponent(15.0882532420,4)
        cc4.death = 17.6419506053
        cc4.eatenby = cc1
        
        cc5 = ConnectedComponent(15.1099343729,5)
        cc5.death = 18.6159343448
        cc5.eatenby = cc1
        
        [self.pd.Evaluate(ts) for ts in self.dr.ts]
        
        # Dictionaries will be different because they will point to different (though identical)
        # cc objects in eatenby

        d = [cc.__dict__ for cc in self.pd.cc]
        testd = [cc.__dict__ for cc in [cc1, cc2, cc3, cc4, cc5]]
        
        for element in [d, testd]: 
            for cc in element: del cc['eatenby']
            
        [self.assertDictEqual(d1, d2, 'Connected Component error') for d1, d2 in izip(d, testd)]
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
