from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt

states = [(0, 0),(1, 0),(2, 0),(3, 0),(4, 0),(5, 0),(6, 0)]
#states = ['Inicio', 'A1', 'A2', 'A3', 'A4', 'Graduado', 'Parou']
Q = [[0.057, 0.31, 0.0, 0.0, 0.603, 0.0, 0.03],
     [0.0, 0.187, 0.528, 0.0, 0.285, 0.0, 0.0],
     [0.0, 0.0, 0.012, 0.563, 0.097, 0.328, 0.0],
     [0.0, 0.0, 0.0, 0.039, 0.094, 0.814, 0.053],
     [0.001, 0.036, 0.02, 0.0, 0.0, 0.003, 0.94],
     [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

G = nx.MultiDiGraph()
labels={}
edge_labels={}

for i, origin_state in enumerate(states):
    for j, destination_state in enumerate(states):
        rate = Q[i][j]
        if rate > 0:
            G.add_edge(origin_state,
                       destination_state,
                       weight=rate,
                       label="{:.03f}".format(rate))
            edge_labels[(origin_state, destination_state)] = label="{:.03f}".format(rate)


plt.figure(figsize=(14,7))
node_size = 200
pos = {state:list(state) for state in states}
nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)
nx.draw_networkx_labels(G, pos, font_weight=2)
nx.draw_networkx_edge_labels(G, pos, edge_labels)
plt.axis('off')

nx.nx_pydot.write_dot(G,'mc.dot')