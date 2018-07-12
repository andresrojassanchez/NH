import numpy as np
import pandas as pd
import pygsheets
import matplotlib.pyplot as plt
import itertools
import networkx as nx
import sys
import pygraphviz
import pylab
from networkx.drawing.nx_agraph import graphviz_layout

# Class to store the name of the route and the path it takes
# Methods ensure no duplicates occur
class trainPath:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name       

# Column names for the dataframe; X is for not relevant information
cols = ['TPC Increment', 'Cumulative Distance', 'Cumulative Time', 'X4', 'X5', 'X6', 'X7', 'X8', 'Route Node', 'X10', 'Field Marker', 'X12', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18', 'X19', 'X20', 'X21', 'X22', 'X23']

# Authorize to send data to google sheets
gc = pygsheets.authorize(outh_file='/home/andres/Documents/NH/creds.json')

# skip counter to not iterate through useless lines in data
skip = 0

# Accumulate the class objects into a set
trainPaths = set()
with open('/home/andres/Documents/NH/tpc.csv') as tpc:
    for line in itertools.islice(tpc, None):
        skip +=1 
        if "Run-time train" in line:
            df = pd.read_csv('/home/andres/Documents/NH/tpc.csv', delim_whitespace = True, skiprows = skip + 6, header = None, names = cols).dropna()
            trainPath = trainPath(line.split()[2], nx.DiGraph())
            
            for i in range(0, df.shape[0] - 1):
                #print(df.iloc[i, 8])
                #print(df.iloc[i+1, 8])
                trainPath.path.add_edge(df.iloc[i, 8],df.iloc[i+1, 8], distance = df.iloc[i,2], color = 'r') 
            nodes = list(trainPath.path)
            print(nodes)
            with open('/home/andres/Documents/NH/link', 'r') as link:
                for line in itertools.islice(link, 12, None):
                    slices = [line[2:14], line[18:30], line[48:69], line[72:81], line[83:95], line[98:110]]
                    if any(slices[0] in s for s in nodes):
                        trainPath.path.add_edge(slices[0], slices[1], color = 'b')
            
            
            trainPaths.add(trainPath)
            #for row in df.itertuples():
            #    trainPath.path.add_node(row[9])


sh = gc.open('xfer generator')
wks = sh[0]
wks.set_dataframe(df, (1,1))


#nx.drawing.nx_pydot.write_dot(trainPath.path, sys.stdout)
#nx.draw(trainPath.path, with_labels = True)   
nx.draw_networkx_edges(trainPath.path, pos = graphviz_layout(trainPath.path), edge_color = [trainPath.path[u][v]['color'] for u, v in trainPath.path.edges()])       
plt.show()               

DG = nx.DiGraph()

cols = ['Origin Node', 'Destination Node', 'Link Class', 'Link Distance', 'Allowable Next Node 1', 'Allowable Next Node 2']
with open('/home/andres/Documents/NH/link', 'r') as link:
    for line in itertools.islice(link, 12, None):
        slices = [line[2:14], line[18:30], line[48:69], line[72:81], line[83:95], line[98:110]]
        DG.add_edge(slices[0], slices[1], distance = slices[3])
        #print(slices[2])





