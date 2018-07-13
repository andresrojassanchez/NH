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
import matplotlib.image as mpimg
from cStringIO import StringIO


G = nx.Graph()
cols = ['Origin Node', 'Destination Node', 'Link Class', 'Link Distance', 'Allowable Next Node 1', 'Allowable Next Node 2']
gc = pygsheets.authorize(outh_file='/home/andres/Documents/NH/creds.json')
data = []



fig = plt.figure()
with open('/home/andres/Documents/NH/node', 'r') as node:
    for line in itertools.islice(node, 10, None):
        node = [line[2:14], line[70:79], line[81:90], line[254:259], line[262:265]]
        node = map(str.strip, node)
        G.add_node(node[0], pos = (int(node[3]),int(node[4])))
    with open('/home/andres/Documents/NH/link', 'r') as link:
        for line in itertools.islice(link, 12, None):
            slices = [line[2:14], line[17:29], line[48:69], line[72:81], line[82:94], line[98:110]]
            slices = map(str.strip, slices)
            data.append(slices)
            if slices[2] == 'Crossover':
                G.add_edge(slices[0], slices[1], color = 'w')
            elif slices[2] == 'Foul':
                G.add_edge(slices[0], slices[1], color = 'r')
            elif slices[2] == 'Turnout':
                G.add_edge(slices[0], slices[1], color = 'g')
            else:
                G.add_edge(slices[0], slices[1], color = 'b')
    
#nx.draw_networkx(MDG, pos = graphviz_layout(MDG), node_size = 40, font_size = 8)
#plt.show()
#print(nx.get_node_attributes(MDG,'pos'))
nx.draw(G, pos = nx.get_node_attributes(G, 'pos'), edge_color = [G[u][v]['color'] for u, v in G.edges()], node_size = 40)

#nx.draw_networkx(trainPath.path, pos = graphviz_layout(trainPath.path), edge_color = [trainPath.path[u][v]['color'] for u, v in trainPath.path.edges()], node_size = 40, font_size = 8)  

fig.set_facecolor('#00000F')
pylab.show()
#p = nx.drawing.nx_pydot.to_pydot(MDG)
#p.write_png('example.png')


'''
d = nx.drawing.nx_pydot.to_pydot(MDG)
png_str = d.create_png()
sio = StringIO()
sio.write(png_str)
sio.seek(0)

img = mpimg.imread(sio)
imgplot = plt.imshow(img)
'''
df = pd.DataFrame(data, columns = cols)
gc = pygsheets.authorize(outh_file='/home/andres/Documents/NH/creds.json')
sh = gc.open('xfer generator')
wks = sh[2]
wks.set_dataframe(df, (1,1))



