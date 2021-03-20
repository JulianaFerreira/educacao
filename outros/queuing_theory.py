import queueing_tool as qt
import numpy as np
import networkx as nx

adja_list = {0: [1], 1: [k for k in range(2, 5)]}
edge_list = {0: {1: 1}, 1: {k: 2 for k in range(2, 5)}}
g = qt.adjacency2graph(adjacency=adja_list, edge_type=edge_list)

def rate(t):
    return 25 + 350 * np.sin(np.pi * t / 2)**2

def arr_f(t):
    return qt.poisson_random_measure(t, rate, 375)

def ser_f(t):
    return t + np.random.exponential(0.2 / 2.1)

q_classes = {1: qt.QueueServer, 2: qt.QueueServer}
q_args    = {
    1: {
        'arrival_f': arr_f,
        'service_f': lambda t: t,
        'AgentFactory': qt.GreedyAgent
    },
    2: {
        'num_servers': 1,
        'service_f': ser_f
    }
}

qn = qt.QueueNetwork(g=g, q_classes=q_classes, q_args=q_args, seed=13)

qn.g.new_vertex_property('pos')
pos = {}
for v in qn.g.nodes():
    if v == 0:
        pos[v] = [0, 0.8]
    elif v == 1:
        pos[v] = [0, 0.4]
    else:
        pos[v] = [-5. + (v - 2.0) / 2, 0]

qn.g.set_pos(pos)
qn.draw(figsize=(5, 5))

qn.draw(fname="store.png", figsize=(12, 3), bbox_inches='tight')

qn.initialize(edge_type=1)

#To simulate for a specified amount of simulation time
qn.simulate(t=1.9)
print(qn.num_events)
qn.draw(fname="sim.png", figsize=(12, 3), bbox_inches='tight')

#save the arrival, departure, and service start times of arrivals
qn.start_collecting_data()
qn.simulate(t=1.8)
data = qn.get_queue_data()
print(data)
data.shape

#The above data also include the number of agent in the queue upon arrival to a queue
qn.clear_data()
qn.start_collecting_data(edge_type=0)
qn.simulate(t=3)
data = qn.get_queue_data(edge_type=0)
#print(data)
data.shape