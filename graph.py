from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt

states = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0)]

class Graph:

    def creategraph(self, Q, n):
        G = nx.MultiDiGraph()
        labels = {}
        edge_labels = {}

        #criar array de estados
        #for i to n:


        for i, origin_state in enumerate(states):
            for j, destination_state in enumerate(states):
                rate = Q[i][j]
                if rate > 0:
                    G.add_edge(origin_state,
                               destination_state,
                               weight=rate,
                               label="{:.03f}".format(rate))
                    edge_labels[(origin_state, destination_state)] = label = "{:.03f}".format(rate)

        plt.figure(figsize=(14, 7))
        node_size = 200
        pos = {state: list(state) for state in states}
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
        nx.draw_networkx_labels(G, pos, font_weight=2)
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        plt.axis('off')

        nx.nx_pydot.write_dot(G, 'mc.dot')


