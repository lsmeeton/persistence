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
    
    Initiates five methods which act as place holders which may/should be replaced in any of the derived plottig objects
    '''


    def __init__(self, pd):
        '''
        Constructor
        '''
        self.pd = pd
        
    def MakeFigure(self):
        pass
    
    def SetAxes(self):
        pass
    
    def DrawDiagonal(self):
        pass
    
    def PlotConnectedComponents(self):
        pass
    
    def PlotConnectedComponentsColour(self):
        pass
    
    def Show(self):
        pass