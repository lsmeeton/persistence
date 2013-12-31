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
    
    threshold: above which no minima or transtion states are read from file
    '''


    def __init__(self,threshold=None):
        '''
        Constructor
        '''
        self.m = []
        self.ts = []
        self.threshold = threshold

    def OrderStationaryPoints(self):
        '''
        Orders self.m by in ascending energy and re-evaluates all transition state indices
        '''
        m = sorted(self.m)
        # Return list of sorted minima indices

        index = [m.index(i) for i in self.m]
        # Change corresponding minima indices in self.ts
        # The +1 -1 bit is for python FORTRAN array/list index conversion
        self.ts = [tuple([float(t[0]),
                          int(index[t[1]-1]+1), 
                          int(index[t[2]-1]+1)]) for t in self.ts]
        
        # Sort transition states by energy
        self.ts = sorted(self.ts, key=lambda x: x[0], reverse=False)

        self.m = m


class DataReadGMIN(DataRead):
    '''
    Class to read minimum and transition state data from GMIN min.data and ts.data files
    '''

    def __init__(self,min_file,ts_file):
        '''
        Constructor
        '''
        super(DataReadGMIN,self).__init__()
        self.min_file = min_file
        self.ts_file = ts_file

    
    def ReadMinima(self):
        '''
        Read minima from file self.min_file
        '''
        try:
            f = open(self.min_file)
        except IOError as e:
            print e
            raise e
        self.m = [float(i.split()[0]) for i in f.readlines() if float(i.split()[0])]
        
    def ReadTransitionStates(self):
        '''
        Read transition states from file self.ts_file
        '''
        try:
            f = open(self.ts_file)
        except IOError as e:
            print e
        
        self.ts = [tuple([float(i.split()[0]), 
                          int(i.split()[3]), 
                          int(i.split()[4])]) for i in f.readlines()]
        
if __name__ == '__main__':
    dr = DataReadGMIN('test/min.data','test/ts.data')
    dr.ReadMinima()
    dr.ReadTransitionStates()
    dr.OrderStationaryPoints()