'''
Created on 16 Dec 2013

@author: lewis
'''
import itertools as it

from pele.storage import Database, Minimum, TransitionState
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


    def __init__(self,threshold=float('inf')):
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

    def RemoveInvalidTS(self):
        '''
        Remove transition states where 1. One or both of the connecting minima have
        energies higher than that of the transition state; 2. the transition state is degenerate
        '''
        del_lst = []
        for e, m1, m2 in self.ts:
            e1 = self.m[m1-1]
            e2 = self.m[m2-1]

            if e1 > e or e2 > e:
                del_lst.append(False)
            else:
                del_lst.append(True)

        self.ts = [ts for ts,element in it.izip(self.ts,del_lst) if element]


class DataReadGMIN(DataRead):
    '''
    Class to read minimum and transition state data from GMIN min.data and ts.data files
    '''

    def __init__(self,min_file,ts_file,*args,**kwargs):
        '''
        Constructor
        '''
        self.min_file = min_file
        self.ts_file = ts_file
        try:
            threshold = kwargs['threshold']
        except KeyError:
            threshold = float('inf')
        super(DataReadGMIN,self).__init__(threshold=threshold)

    
    def ReadMinima(self):
        '''
        Read minima from file self.min_file
        '''
        try:
            f = open(self.min_file)
        except IOError as e:
            print e
            raise e
        
        self._m = {}
        for index, line in enumerate(f.readlines()):
            energy = float(line.split()[0])
            if energy <= self.threshold:
                self._m[index+1] = energy

        self._AssignMinima()


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
                          int(i.split()[4])]) for i in f.readlines() if float(i.split()[0]) <= self.threshold]
        
        self._Relabel()

    def _AssignMinima(self):
        '''
        Initialise self.m
        '''
        keys = sorted(self._m.keys())
        
        self.m = [self._m[k] for k in keys] # Ensures that minima indices are contiguous

    def _Relabel(self):
        '''
        Re-label minima indices in transition state tuples to account for missing minima due to
        threshold constraint
        '''
        keys = {}
        for index, element in enumerate(sorted(self._m.keys())):
            keys[element] = index+1

        for i, t in enumerate(self.ts):
            self.ts[i] = tuple([t[0], keys[t[1]], keys[t[2]]])

class DataReadpele(DataRead):
    '''
    Class to read minimum and transition state data from a pele sql database
    '''

    def __init__(self,db_file,*args,**kwargs):
        '''
        Constructor
        '''
        try:
            threshold = kwargs['threshold']
        except KeyError:
            threshold = float('inf')
        super(DataReadpele,self).__init__(threshold=threshold)
        self.db_file = db_file

    
    def ReadMinima(self):
        '''
        Read minima from file self.min_file
        '''
        try:
            db = Database(self.db_file)
        except IOError as e:
            print e
            raise e
        self._m = {}
        for m in db.session.query(Minimum).filter(Minimum.energy <= self.threshold):
            energy = m.energy
            index = m._id
            self._m[index] = energy

        self._AssignMinima()

        
    def ReadTransitionStates(self):
        '''
        Read transition states from file self.ts_file
        '''
        try:
            db = Database(self.db_file)
        except IOError as e:
            print e
            raise e
        
        for ts in db.session.query(TransitionState).filter(TransitionState.energy <= self.threshold):
            energy = ts.energy
            m1 = ts._minimum1_id
            m2 = ts._minimum2_id
            self.ts.append(tuple([energy,
                                  m1,
                                  m2]))

        self._Relabel()

        self.RemoveInvalidTS()

    def _AssignMinima(self):
        '''
        Initialise self.m
        '''
        keys = sorted(self._m.keys())
        
        self.m = [self._m[k] for k in keys] # Ensures that minima indices are contiguous

    def _Relabel(self):
        '''
        Re-label minima indices in transition state tuples to account for missing minima due to
        threshold constraint
        '''
        keys = {}
        for index, element in enumerate(sorted(self._m.keys())):
            keys[element] = index+1

        for i, t in enumerate(self.ts):
            self.ts[i] = tuple([t[0], keys[t[1]], keys[t[2]]])
        
if __name__ == '__main__':
    dr = DataReadGMIN('test/min.data','test/ts.data')
    dr.ReadMinima()
    dr.ReadTransitionStates()
    dr.OrderStationaryPoints()