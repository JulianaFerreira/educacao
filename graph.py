from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt

class Graph:

    def creategraph(self, Q):
        G = nx.MultiDiGraph()
        mapping = {(0, 0): "A1", (1, 0): "A2", (2, 0): "A3", (3, 0): "A4", (4, 0): "A5", (5, 0): "A1R", (6, 0): "A2R",
                   (7, 0): "A3R", (8, 0): "A4R", (9, 0): "A5R", (10, 0): "G", (11, 0): "E"}
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
        nx.relabel_nodes(G, mapping)
        plt.axis('off')

        nx.nx_pydot.write_dot(G, 'mc.dot')


