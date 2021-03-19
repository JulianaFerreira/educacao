from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt
from subprocess import check_call

import pydot


class Graph:

    def creategraph(self, Q):
        G = nx.MultiDiGraph()
        labels = {}
        edge_labels = {}
        states = []

        for i in range(len(Q)):
            states.append((i,0))


        for i, origin_state in enumerate(states):
            for j, destination_state in enumerate(states):
                rate = Q[i][j]
                if rate > 0:
                    G.add_edge(origin_state,
                               destination_state,
                               weight=rate,
                               label="{:.02f}".format(rate))
                    edge_labels[(origin_state, destination_state)] = label = "{:.02f}".format(rate)

        plt.figure(figsize=(14, 7))
        node_size = 200
        pos = {state: list(state) for state in states}
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
        nx.draw_networkx_labels(G, pos, font_weight=2)
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        plt.axis('off')

        nx.nx_pydot.write_dot(G, 'mc.dot')


