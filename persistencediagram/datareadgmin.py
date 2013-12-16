'''
Created on 16 Dec 2013

@author: lewis
'''
from persistencediagram.dataread import DataRead
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
    
        
        
if __name__ == '__main__':
    dr = DataReadGMIN('min.data','ts.data')
    dr.ReadMinima()
    print dr.__dict__