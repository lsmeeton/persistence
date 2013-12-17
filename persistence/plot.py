'''
Created on 17 Dec 2013

@author: lewis
'''
__metaclass__ = type
class Plot(object):
    '''
    Parent class for plotting persistence diagrams
    Initiates one attribute:
    
    pd: Persistence Diagram
    '''


    def __init__(self, pd):
        '''
        Constructor
        '''
        self.pd = pd