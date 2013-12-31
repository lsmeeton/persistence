'''
Created on 17 Dec 2013

@author: lewis
'''
try:
    import matplotlib.pyplot as plt
    import matplotlib.colors as colors
    import matplotlib.cm as cm
    import matplotlib.colorbar as cb
    
    def UseMatPlotLib(): pass
    
except ImportError as e:
    def UseMatPlotLib(): raise e

try:
    from mayavi import mlab
    
    def UseMayaVI2(): pass
    
except ImportError as e:
    def UseMayaVI2(): raise e

__metaclass__ = type
class Plot(object):
    '''
    Parent class for plotting persistence diagrams
    Initiates one attribute:
    
    pd: Persistence Diagram
    
    Initiates five methods which act as place holders which may/should be replaced in any of the derived plotting objects
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
    
class PlotMatPlotLib(Plot):
    '''
    Plots persistence diagrams using matplotlib
    
    '''
    def __init__(self, pd):
        '''
        Constructor
        '''
        super(PlotMatPlotLib,self).__init__(pd)
        UseMatPlotLib()
        
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
        
    def PlotConnectedComponentsColour(self):
        
        self.BuildColourMap()
        
        col_map = cm.ScalarMappable(norm = self.norm, 
                                    cmap = self.cmap)
        [plt.scatter(cc.birth, 
                     cc.death,
                     color=col_map.to_rgba(cc.size, 
                                           alpha=0.4))
          for cc in self.pd.cc[1:]]
        
        self.AddColourBar()
        
    def BuildColourMap(self):
        
        self.cmap = cm.get_cmap('brg_r')
        
        self.col = [cc.size for cc in self.pd.cc[1:]]
        
        self.norm = colors.LogNorm(vmin = min(self.col),
                                   vmax = max(self.col))        
        
    def AddColourBar(self):
                
        cax, kw = cb.make_axes(self.ax)
        self.cb = cb.ColorbarBase(cax,
                                  cmap=self.cmap,
                                  norm=self.norm,
                                  orientation='vertical')

    def Show(self):
        plt.show()
        

class PlotMayaVI2(Plot):
    '''
    classdocs
    '''

    def __init__(self, pd):
        '''
        Constructor
        '''
        super(PlotMayaVI2,self).__init__(pd)
        UseMayaVI2()
        
    def MakeFigure(self):
        self.fig = mlab.figure()
        
    def PlotConnectedComponents(self):
        x = [cc.birth for cc in self.pd.cc[1:]]
        y = [cc.death for cc in self.pd.cc[1:]]
        z = [cc.size for cc in self.pd.cc[1:]]
        mlab.points3d(x, y, z)
        
    def Show(self):
        mlab.show()
        
if __name__ == '__main__':
    from persistence.dataread import DataReadGMIN
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