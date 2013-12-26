'''
Created on 17 Dec 2013

@author: lewis
'''
import matplotlib.pyplot as plt
from persistence.plot import Plot
__metaclass__ = type
class PlotMatPlotLib(Plot):
    '''
    Plots persistence diagrams using matplotlib
    
    '''
    def __init__(self, pd):
        '''
        Constructor
        '''
        super(PlotMatPlotLib,self).__init__(pd)
        
    def MakeFigure(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        
    def SetAxes(self,ax_min, ax_max):
        self.ax.set_xlim(xmin=ax_min)
        self.ax.set_ylim(ymin=ax_min)
        
        self.ax.set_xlim(xmax=ax_max)
        self.ax.set_ylim(ymax=ax_max)
        
    def DrawDiagonal(self):
        ax_min, ax_max = plt.xlim()   # return the current xlim
        plt.plot([ax_min, ax_max], [ax_min, ax_max])
        
    def PlotConnectedComponents(self):
        [plt.scatter(cc.birth, cc.death, alpha=0.4) for cc in self.pd.cc[1:]]
        
    def Show(self):
        plt.show()
    
if __name__ == '__main__':
    from persistence.datareadgmin import DataReadGMIN
    from persistence.persistencediagram import PersistenceDiagram
#     directory = "/home/lewis/DISCONNECTIO/DISCONNECTinput/BLN46/"
#     directory = "/home/lewis/CTP/AGGG-Landscape/pathsample-wat/"
    directory = "/home/lewis/CTP/PbAKbA-Landscape/pathsample-wat/"
    threshold = -97.0
    print "Creating dataread object"
    dr = DataReadGMIN(directory+'min.data',directory+'ts.data')
    print "Reading Minima"
    dr.ReadMinima()
    print "Reading Transition States"
    dr.ReadTransitionStates()
    print "Ordering Stationary points by energy"
    dr.OrderStationaryPoints()
    
    print "Creating persistence diagram object"
    pd = PersistenceDiagram()
    print "Populating persistence diagram"
    pd.Populate(dr.m)
    print "Connecting"
    [pd.Evaluate(ts) for ts in dr.ts]
    print "Removing unconnected components"
    pd.RemoveUnconnectedComponents()
    
    print "plotting persistence diagram"
    pl = PlotMatPlotLib(pd)
    pl.MakeFigure()
    pl.SetAxes(dr.m[0], max([i[0] for i in dr.ts]))
    pl.DrawDiagonal()
    pl.PlotConnectedComponents()
    pl.Show()