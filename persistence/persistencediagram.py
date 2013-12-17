'''
Created on 17 Dec 2013

@author: lewis
'''
from persistence.connectedcomponent import ConnectedComponent
__metaclass__ = type
class PersistenceDiagram(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cc = None
        
    def Populate(self,m):
        '''
        Takes as argument ascending ordered list of minima energies, m,
        and births ConnectedComponents, storing them in cc.
        '''
        self.cc = [ConnectedComponent(birth, min_id + 1) for min_id, birth in enumerate(m)]
        
        
if __name__ == '__main__':
    from persistence.datareadgmin import DataReadGMIN
    dr = DataReadGMIN('test/min.data','test/ts.data')
    dr.ReadMinima()
    dr.ReadTransitionStates()
    dr.OrderStationaryPoints()
    
    pd = PersistenceDiagram()
    pd.Populate(dr.m)
    