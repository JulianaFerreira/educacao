from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from pydtmc import MarkovChain, plot_graph, plot_walk

plt.ion()
# statenames = ['Y1', 'Y2', 'Y3', 'Y4', 'I', 'G', 'W']
# state = np.array([[1, 0, 0, 0, 0, 0, 0]])
# p = [[0.057, 0.31, 0.0, 0.0, 0.603, 0.0, 0.03], [0.0, 0.187, 0.528, 0.0, 0.285, 0.0, 0.0],
#      [0.0, 0.0, 0.012, 0.563, 0.097, 0.328, 0.0], [0.0, 0.0, 0.0, 0.039, 0.094, 0.814, 0.053],
#      [0.001, 0.036, 0.02, 0.0, 0.0, 0.003, 0.94], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]
statenames = ['Inicio', 'A1', 'A2', 'A3', 'A4', 'Graduado', 'Evadido']
state = np.array([[1, 0, 0, 0, 0, 0, 0]])
p = [[0.0, 0.89, 0.09, 0.02, 0.0, 0.0, 0.0], [0.0, 0.17, 0.64, 0.06, 0.0, 0.0, 0.13],
     [0.0, 0.0, 0.1, 0.75, 0.08, 0.0, 0.07], [0.0, 0.0, 0.0, 0.08, 0.84, 0.04, 0.04],
     [0.0, 0.0, 0.0, 0.0, 0.37, 0.61, 0.02], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]
stateHist = state
mc = MarkovChain(p, statenames)

print(mc)
print("Matriz Fundamental:")
print(mc.fundamental_matrix)
print("Tempos de Absorção:")
print(mc.absorption_times)
#print(mc.recurrent_states)
#print(mc.transient_states)
#print(mc.steady_states)
#print(mc.expected_transitions(1))
#print(mc.topological_entropy)
#print(mc.walk(10))
#plot_walk(mc, 20, 'sequence')

for x in range(10):
    #probalidade de cada estado por ano
    #print(state)
    state = np.dot(state, p)
    stateHist = np.append(stateHist, state, axis=0)
    dfDistrHist = pd.DataFrame(stateHist, columns=statenames)

dfDistrHist.plot()