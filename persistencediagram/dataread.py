'''
Created on 16 Dec 2013

@author: lewis
'''
__metaclass__ = type
class DataRead(object):
    '''
    Parent Class for reading stationary point data from file.
    Initiates two class attributes:
    
    m: List for storing minimum energies as floats
    
    ts: List for storing transition state energy and it's two connecting minima as a tuple
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.m = []
        self.ts = []
        
if __name__ == '__main__':
    dr = DataRead()
    print dr.m, dr.ts