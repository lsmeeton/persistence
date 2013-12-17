'''
Created on 16 Dec 2013

@author: lewis
'''
from persistence.dataread import DataRead
__metaclass__ = type
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
