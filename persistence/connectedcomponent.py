'''
Created on 17 Dec 2013

@author: lewis
'''
import exceptions

__metaclass__ = type
class ConnectedComponent(object):
    '''
    Class for defining connected components for persistence diagrams
    Initiates five class attributes:
    
    birth: Energy at which connected component is born
    death: Energy at which connected component dies
    eatenby: Connected component which current connected component is eaten by
    m: List of minima indices contained in connected component
    size: Number of minima contained in connected component
    '''


    def __init__(self, birth, min_id):
        '''
        Constructor
        '''
        self.birth = birth
        self.death = None
        self.eatenby = None
        self.m = [min_id]
        self.size = 1
        
    def AddMinima(self,m):
        '''
        Takes as argument list of minima indices, m, and adds them to self.m
        '''
        self.m += m
        self.size = len(self.m)
        
    def Kill(self, other, death):
        '''
        Kill connected component self with connected component other at energy death
        '''
        if death > self.birth:
            self.death = death
            self.eatenby = other
        else: 
            raise ConnectedComponentError(birth = self.birth, death = death)

    def Eat(self, other, death):
        '''
        Kill connected component other at energy death and add it's minima to m
        '''
        try:
            other.Kill(self,death)
        except ConnectedComponentError as cc_e:
            print "Connected Component w. Death: %2.6f before Birth: %2.6f found"%(cc_e.birth,cc_e.death)
        self.AddMinima(other.m)
        
class ConnectedComponentError(Exception):
    '''
    ConnectedComponent Error class
    '''
    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        super(ConnectedComponentError,self).__init__(*args, **kwargs)
        self.birth = 0.0
        self.death = 0.0

        if kwargs.has_key('birth'):
            self.birth = kwargs['birth']

        if kwargs.has_key('death'):
            self.death = kwargs['death']

if __name__ == '__main__':
    cc1 = ConnectedComponent(birth=0, min_id=1)
    cc2 = ConnectedComponent(birth=1, min_id=2)
    print cc1.__dict__, cc2.__dict__
    cc1.Eat(cc2,death=2)
    print cc1.__dict__, cc2.__dict__