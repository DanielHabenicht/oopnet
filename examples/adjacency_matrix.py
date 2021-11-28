import os

import networkx as nx

from oopnet.api import *
from oopnet.graph.graph import onlinks2nxlinks


filename = os.path.join('..', 'examples', 'data', 'anytown.inp')

net = Read(filename)

G = Graph(net)

nodes = get_node_ids(net)
links = onlinks2nxlinks(net)

A = nx.incidence_matrix(G, nodelist=nodes, edgelist=links)
print('Incidence Matrix - not oriented')
print(A)

B = nx.incidence_matrix(G, nodelist=nodes, edgelist=links, oriented=True)
print('Incidence matrix - oriented')
print(B)


G = Graph(net, weight='length', default=0.0)
C = nx.adjacency_matrix(G, nodelist=nodes)
print('Adjacency matrix; undirected graph')
print(C)

G = DiGraph(net, weight='length', default=0.0)
D = nx.adjacency_matrix(G, nodelist=nodes)
print('Adjacency matrix; directed graph')
print(D)

plt.figure(1)
plt.imshow(A.todense(), cmap='viridis', interpolation='nearest')
plt.title('Incidence matrix - not oriented')
plt.colorbar()

plt.figure(2)
plt.imshow(B.todense(), cmap='viridis', interpolation='nearest')
plt.title('Incidence matrix - oriented')
plt.colorbar()

plt.figure(3)
plt.imshow(C.todense(), cmap='viridis', interpolation='nearest')
plt.title('Adjacency matrix; undirected graph')
plt.colorbar()

plt.figure(4)
plt.imshow(D.todense(), cmap='viridis', interpolation='nearest')
plt.title('Adjacency matrix; directed graph')
plt.colorbar()

Show()
