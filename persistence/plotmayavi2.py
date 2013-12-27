'''
Created on 17 Dec 2013

@author: lewis
'''
from mayavi import mlab
from persistence.plot import Plot
__metaclass__ = type
class PlotMayaVI2(Plot):
    '''
    classdocs
    '''


    def __init__(self, pd):
        '''
        Constructor
        '''
        super(PlotMayaVI2,self).__init__(pd)
        
    def MakeFigure(self):
        self.fig = mlab.figure()
#         self.ax = self.fig.add_subplot(111)
        
    def SetAxes(self,ax_min, ax_max):
        pass
#         mlab.axes()
#         self.ax.set_xlim(xmin=ax_min)
#         self.ax.set_ylim(ymin=ax_min)
        
#         self.ax.set_xlim(xmax=ax_max)
#         self.ax.set_ylim(ymax=ax_max)
        
    def DrawDiagonal(self):
        pass
#         ax_min, ax_max = plt.xlim()   # return the current xlim
#         plt.plot([ax_min, ax_max], [ax_min, ax_max])
        
    def PlotConnectedComponents(self):
        x = [cc.birth for cc in self.pd.cc[1:]]
        y = [cc.death for cc in self.pd.cc[1:]]
        z = [cc.size for cc in self.pd.cc[1:]]
        mlab.points3d(x, y, z)
        
    def Show(self):
        mlab.show()
        
if __name__ == '__main__':
    from persistence.datareadgmin import DataReadGMIN
    from persistence.persistencediagram import PersistenceDiagram
#     directory = "/home/lewis/DISCONNECTIO/DISCONNECTinput/BLN46/"
    directory = "/home/lewis/CTP/AGGG-Landscape/pathsample-wat/"
#     directory = "/home/lewis/CTP/PbAKbA-Landscape/pathsample-wat/"
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
    pl = PlotMayaVI2(pd)
    pl.MakeFigure()
    pl.SetAxes(dr.m[0], dr.ts[-1][0])
    pl.DrawDiagonal()
    pl.PlotConnectedComponents()
    pl.Show()