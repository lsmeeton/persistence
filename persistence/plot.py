'''
Created on 17 Dec 2013

@author: lewis
'''
try:
    import matplotlib.pyplot as plt
    import matplotlib.colors as colors
    import matplotlib.cm as cm
    import matplotlib.colorbar as cb
    from matplotlib.patches import Circle
    from matplotlib.collections import PatchCollection
    
    def UseMatPlotLib(): pass
    
except ImportError as e:
    def UseMatPlotLib(): raise e

try:
    from mayavi import mlab
    
    def UseMayaVI2(): pass
    
except ImportError as e:
    def UseMayaVI2(): raise e
    
try:
    import plotly as ply
    def UsePlotly(): pass
except ImportError as e:
    def UsePlotly(): raise e

__metaclass__ = type
class Plot(object):
    '''
    Parent class for plotting persistence diagrams
    Initiates one attribute:
    
    pd: Persistence Diagram
    
    Initiates five methods which act as place holders which may/should be replaced in any of the derived plotting objects
    '''
    
    def __init__(self, pd,*args,**kwargs):
        '''
        Constructor
        '''
        self.pd = pd
        
    def MakeFigure(self,*args,**kwargs):
        pass
    
    def SetAxes(self,*args,**kwargs):
        pass

    def LabelAxes(self,*args,**kwargs):
        pass
    
    def DrawDiagonal(self,*args,**kwargs):
        pass
    
    def PlotConnectedComponents(self,*args,**kwargs):
        pass
    
    def PlotConnectedComponentsColour(self,*args,**kwargs):
        pass
    
    def Show(self,*args,**kwargs):
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
        
    def SetAxes(self,x_ax_min, x_ax_max, y_ax_min, y_ax_max):
        self.ax.set_xlim(xmin=x_ax_min)
        self.ax.set_ylim(ymin=y_ax_min)
        
        self.ax.set_xlim(xmax=x_ax_max)
        self.ax.set_ylim(ymax=y_ax_max)

    def LabelAxes(self, x_label="Birth", y_label="Death"):
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        
    def DrawDiagonal(self):
        ax_min, ax_max = plt.xlim()   # return the current xlim
        plt.plot([ax_min, ax_max], [ax_min, ax_max])
        
    def PlotConnectedComponents(self,cs=None,flatten=None):

        if cs:
            cmap, col, norm = self.BuildColourMap()
        
            col_map = cm.ScalarMappable(norm = norm, 
                                        cmap = cmap)
            colour = col_map.to_rgba(col,alpha=0.4)

            self.AddColourBar(cmap,norm)
        else:
            colour = 'b'

        radius = 0.1
        if flatten:
            patches = [Circle((cc.birth,cc.death - cc.birth), radius) for cc in self.pd.cc[1:]]
        else:
            patches = [Circle((cc.birth,cc.death), radius) for cc in self.pd.cc[1:]]

        p = PatchCollection(patches, 
                            color = colour,
                            edgecolor = 'black',
                            linewidth = '0.05')
        self.ax.add_collection(p)
        
    def BuildColourMap(self):
        
        cmap = cm.get_cmap('winter_r')
        
        col = [cc.size for cc in self.pd.cc[1:]]
        
        norm = colors.LogNorm(vmin = min(col),
                              vmax = max(col))

        return cmap, col, norm
        
    def AddColourBar(self,cmap,norm):
                
        cax, kw = cb.make_axes(self.ax)
        cb.ColorbarBase(cax,
                        cmap=cmap,
                        norm=norm,
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
        
        
class PlotPlotly(Plot):
    '''
    classdocs
    '''
    def __init__(self, pd, username_or_email, key):
        '''
        Constructor
        '''
        super(PlotPlotly,self).__init__(pd)
        UsePlotly()
        
        self.fig = ply.plotly(username_or_email=username_or_email, key=key)
        
    def PlotConnectedComponents(self, *args):

        scatter = [[cc.birth, cc.death ] for cc in self.pd.cc[1:]]
        
        self.scatter = {'x':[x[0] for x in scatter],
                         'y':[y[1] for y in scatter],
                         'type':'scatter','mode':'markers',
                         'marker':{'color':'rgb(0, 0, 255)','opacity':0.5 }}
        
    def SetAxes(self,ax_min, ax_max):
        self.xaxesstyle = {"title" : "Birth Energy",
                           "type" : "linear",
                           "rangemode" : "normal",
                           "range" : [ax_min,ax_max]}

        self.yaxesstyle = {"title" : "Death Energy",
                           "type" : "linear",
                           "rangemode" : "normal",
                           "range" : [ax_min,ax_max]}

    def DrawDiagonal(self):
        x = self.xaxesstyle['range'][:]
        y = self.yaxesstyle['range'][:]
        self.diagonal = {'x': x,
                         'y': y,
                         'type': 'scatter',
                         'mode': 'lines'}
        
    def Show(self):
        
        self.legendstyle = {"x" : 100, "y" : 1}
        
        self.layout = {"xaxis" : self.xaxesstyle,
                       "yaxis" : self.yaxesstyle,
                       'autosize': False,
                       'width': 650,
                       'height': 650,
                       'title':'Persistence Diagram',
                       'hovermode' : 'closest',
                       'legend' : self.legendstyle,
                       'showlegend' : False}
        
        self.fig.plot([self.scatter,self.diagonal],
                      layout=self.layout,
                      world_readable=False)

class PlotToText(Plot):
    '''
    classdocs
    '''
    def __init__(self, pd, fname):
        '''
        Constructor
        '''
        super(PlotToText,self).__init__(pd)
        self.fname = fname[0]

    def PlotConnectedComponents(self, flatten=None,*args,**kwargs):

        self.x = [cc.birth for cc in self.pd.cc[1:]]
        
        if flatten:
            self.y = [cc.death - cc.birth for cc in self.pd.cc[1:]]
        else:
            self.y = [cc.death for cc in self.pd.cc[1:]]
        self.z = [cc.size for cc in self.pd.cc[1:]]
    
    def Show(self,*args,**kwargs):
        with open(self.fname,'w') as f:
            f.write("#Birth\tDeath\tSize\n")
            for i, x in enumerate(self.x):
                s = "%2.6f\t%2.6f\t%d\n"%(x,self.y[i],self.z[i])
                f.write(s)
        
        
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