'''
Created on 17 Dec 2013

@author: lewis
'''
from persistence.connectedcomponent import ConnectedComponent
__metaclass__ = type
class PersistenceDiagram(object):
    '''
    Persistence diagram class
    Initiates one class:
    
    cc: List of connected components, indexed by initial minimum contained
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cc = None
        
    def __str__(self):
        s = "Connected Components\nBirth\tContents\n"
        r = ''.join([s.join(str(cc.birth) + '\t' + str(cc.m) + '\n') for cc in self.cc])
        return r
        
    def Populate(self,m):
        '''
        Takes as argument ascending ordered list of minima energies, m,
        and births ConnectedComponents, storing them in cc.
        '''
        self.cc = [ConnectedComponent(birth, min_id + 1) for min_id, birth in enumerate(m)]
        
    def Merge(self,death, cc1, cc2):
        '''
        Merge connected components, cc1 and cc2.
        '''
        
        if cc1.birth < cc2.birth:
            cc1.Eat(cc2, death)
        else:
            cc2.Eat(cc1, death)
        
        
    def Evaluate(self,ts):
        '''
        Find which connected components, cc1 and cc2, are coupled by 
        transition state tuple ts (energy, min1, min2).
        '''
        m1 = ts[1]
        m2 = ts[2]
        
        cc1 = self.LocateConnectedComponent(m1)
        cc2 = self.LocateConnectedComponent(m2)
        
        if cc1 != cc2: self.Merge(ts[0], cc1, cc2)
    
    def LocateConnectedComponent(self,m):
        '''
        Given a minimum m, locate and return connected component cc
        '''
        cc = self.cc[m-1]
        while cc.eatenby:
            cc = cc.eatenby
        return cc
    
    def RemoveUnconnectedComponents(self):
        '''
        Removes all connected components with eatenby == None,
        with the exception of connected component containing the
        global minimum, which by definition never dies
        '''
        gcc = [self.cc[0]]
        self.cc = [cc for cc in self.cc[1:] if cc.eatenby]
        self.cc = gcc + self.cc
        
if __name__ == '__main__':
    from persistence.datareadgmin import DataReadGMIN
    dr = DataReadGMIN('test/min.data','test/ts.data')
    dr.ReadMinima()
    dr.ReadTransitionStates()
    dr.OrderStationaryPoints()
    
    pd = PersistenceDiagram()
    pd.Populate(dr.m)
    
    print [cc.__dict__ for cc in pd.cc]
    
    [pd.Evaluate(ts) for ts in dr.ts]
    
    print [cc.__dict__ for cc in pd.cc]
    
    pd.RemoveUnconnectedComponents()
    
    print '\n'
    print [cc.__dict__ for cc in pd.cc]
    