from persistence.datareadgmin import DataReadGMIN
from persistence.persistencediagram import PersistenceDiagram 
from persistence.connectedcomponent import ConnectedComponent

try:
    from persistence.plotmatplotlib import PlotMatPlotLib
    def UseMatPlotLib(): pass
except ImportError as e:
    def UseMatPlotLib(): raise e

try:
    from persistence.plotmayavi2 import PlotMayaVI2
    def UseMayaVI2(): pass
except ImportError as e:
    def UseMayaVI2(): raise e
    
import argparse


#------------------------------------------------------------------------------#
# argparse is a module which makes it easy to write user-friendly                                                                     
# command-line interfaces.                                                                                                            
# http://docs.python.org/2.7/library/argparse.html                                                                                    
parser = argparse.ArgumentParser(description="Read arguments for the calculation, plotting and storage of persistence diagrams")
group = parser.add_mutually_exclusive_group()
parser.add_argument('-m','--minima',
                    type=str,
                    default='min.data',
                    dest='m',
                    help='Location of file containing minima in GMIN file format')
parser.add_argument('-t','--ts',
                    type=str,
                    default='ts.data',
                    dest='t',
                    help="Location of file containing transition states in GMIN file format")
parser.add_argument('--matplotlib',
                    action='store_true',
                    default=True,
                    dest='matplotlib')
parser.add_argument('--threshold',
                    type=float,
                    default=None,
                    dest='threshold',
                    help="Energy threshold above which no minima or transition states are included in persistence diagram. Default energy units")

args = parser.parse_args()


#------------------------------------------------------------------------------#
if args.m:
    dr = DataReadGMIN(min_file=args.m, ts_file=args.t)
else: pass # Add pele data file reading here

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



if args.matplotlib:
    print "plotting persistence diagram using matplotlib"
    pl = PlotMatPlotLib(pd)
    pl.MakeFigure()
    pl.SetAxes(dr.m[0], max([i[0] for i in dr.ts]))
    pl.DrawDiagonal()
    pl.PlotConnectedComponents()
    pl.Show()



