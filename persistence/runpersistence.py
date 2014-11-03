from persistence.dataread import DataReadGMIN, DataReadpele
from persistence.persistencediagram import PersistenceDiagram 
from persistence.plot import PlotMatPlotLib, PlotMayaVI2, PlotPlotly, PlotToText
    
import argparse


#------------------------------------------------------------------------------#
# argparse is a module which makes it easy to write user-friendly                                                                     
# command-line interfaces.                                                                                                            
# http://docs.python.org/2.7/library/argparse.html                                                                                    
parser = argparse.ArgumentParser(description="Read arguments for the calculation, plotting and storage of persistence diagrams")

read_group = parser.add_mutually_exclusive_group(required=True)
plot_group = parser.add_mutually_exclusive_group(required=True)

read_group.add_argument('-g',
                        nargs=2,
                        type=str,
                        metavar=('min.data','ts.data'),
                        default=None,
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
                        default=None,
                        dest='matplotlib',
                        help="plot persistence diagram using matplotlib")
plot_group.add_argument('--mayavi2',
                        action='store_true',
                        default=None,
                        dest='mayavi2',
                        help="plot persistence diagram using mayavi2")
plot_group.add_argument('--plotly',
                        nargs=2,
                        type=str,
                        metavar=('username_or_email','api_key'),
                        default=None,
                        dest='plotly',
                        help="plot persistence diagram using plotly")

plot_group.add_argument('--text',
                        nargs=1,
                        type=str,
                        metavar='fname',
                        default=None,
                        dest='text',
                        help="write co-ordinates of persistence diagram to text file")

parser.add_argument('--threshold',
                    type=float,
                    default=float('inf'),
                    metavar='e',
                    dest='threshold',
                    help="Energy threshold above which no minima or transition states are included in persistence diagram. Default energy units")
parser.add_argument('--colourbysize',
                    action='store_true',
                    default=None,
                    dest='cs',
                    help="Colour connected components according to number of minima they contain. Scaled logarithmically.")
parser.add_argument('--flatten',
                    action='store_true',
                    default=None,
                    dest='flatten',
                    help="Plot birth against life for connected components, as opposed to birth against death")
args = parser.parse_args()

#------------------------------------------------------------------------------#
if args.gmin:
    dr = DataReadGMIN(min_file=args.gmin[0], ts_file=args.gmin[1],threshold=args.threshold)
else: 
    dr = DataReadpele(db_file=args.pele[0],threshold=args.threshold)

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

    print "Plotting persistence diagram"
    pl = PlotMayaVI2(pd)
    
if args.plotly:
    print "Plotting persistence diagram using Plot.ly python api with username or email: %s and api key: %s"%(tuple(args.plotly))
    pl = PlotPlotly(pd, 
                    username_or_email=args.plotly[0], 
                    key=args.plotly[1])
    
if args.matplotlib:

    print "Plotting persistence diagram using matplotlib"
    pl = PlotMatPlotLib(pd)

if args.text:
    print "Writing persistence diagram co-ordiantes to file %s"%args.text[0]
    pl = PlotToText(pd,
                    fname = args.text)
pl.MakeFigure()

if args.cs: 
    print "Colouring connected components according to size"
if args.flatten:
    pl.SetAxes(dr.m[0], dr.ts[-1][0], 0, dr.ts[-1][0] - dr.m[0])
    pl.LabelAxes(x_label="Birth",y_label="Life")
else:
    pl.SetAxes(dr.m[0], dr.ts[-1][0],dr.m[0], dr.ts[-1][0])
    pl.DrawDiagonal()
    pl.LabelAxes(x_label="Birth",y_label="Death")

pl.PlotConnectedComponents(cs=args.cs,
                           flatten=args.flatten)

pl.Show()
