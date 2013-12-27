from persistence.datareadgmin import DataReadGMIN
from persistence.persistencediagram import PersistenceDiagram 

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

read_group = parser.add_mutually_exclusive_group()
plot_group = parser.add_mutually_exclusive_group()

read_group.add_argument('-g',
                        nargs=2,
                        type=str,
                        metavar=('min.data','ts.data'),
                        default=['min.data','ts.data'],
                        dest='gmin',
                        help='Location of files containing minima and transition states in GMIN file format')
read_group.add_argument('-p',
                        nargs=1,
                        type=str,
                        metavar='pele.db',
                        default=None,
                        dest='pele',
                        help="Location of file containing minima and transition states in pele sql file format")

plot_group.add_argument('--matplotlib',
                        action='store_true',
                        default=True,
                        dest='matplotlib',
                        help="plot persistence diagram using matplotlib")
plot_group.add_argument('--mayavi2',
                        action='store_true',
                        default=False,
                        dest='mayavi2',
                        help="plot persistence diagram using mayavi2")

parser.add_argument('--threshold',
                    type=float,
                    default=None,
                    dest='threshold',
                    help="Energy threshold above which no minima or transition states are included in persistence diagram. Default energy units")
parser.add_argument('--colourbysize',
                    action='store_true',
                    default=None,
                    dest='cs',
                    help="Colour connected components according to number of minima they contain. Scaled logarithmically.")

args = parser.parse_args()

print args
#------------------------------------------------------------------------------#
if args.gmin:
    dr = DataReadGMIN(min_file=args.gmin[0], ts_file=args.gmin[1])
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

if args.mayavi2:
    UseMayaVI2()
    print "plotting persistence diagram"
    pl = PlotMayaVI2(pd)
if args.matplotlib:
    UseMatPlotLib()
    print "Plotting persistence diagram using matplotlib"
    pl = PlotMatPlotLib(pd)
    
pl.MakeFigure()
pl.SetAxes(dr.m[0], max([i[0] for i in dr.ts]))
pl.DrawDiagonal()

if not args.cs:
    pl.PlotConnectedComponents()
else:
    print "Colouring connected components according to size"
    pl.PlotConnectedComponentsColour()

pl.Show()


