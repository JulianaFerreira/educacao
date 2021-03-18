from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from pydtmc import MarkovChain, plot_graph, plot_walk
plt.ion()

taxa = 1.25

statenames = ['Y1', 'Y2', 'Y3', 'Y4', 'I', 'G', 'W']
state = np.array([[1, 0, 0, 0, 0, 0, 0]])
p = [[0.057, 0.31, 0.0, 0.0, 0.603, 0.0, 0.03],
     [0.0, 0.187, 0.528, 0.0, 0.285, 0.0, 0.0],
     [0.0, 0.0, 0.012, 0.563, 0.097, 0.328, 0.0],
     [0.0, 0.0, 0.0, 0.039, 0.094, 0.814, 0.053],
     [0.001, 0.036, 0.02, 0.0, 0.0, 0.003, 0.94],
     [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]
# statenames = ['Inicio', 'A1', 'A2', 'A3', 'A4', 'Graduado', 'Evadido']
# state = np.array([[1, 0, 0, 0, 0, 0, 0]])
# p = [[0.0, 0.89, 0.09, 0.02, 0.0, 0.0, 0.0], [0.0, 0.17, 0.64, 0.06, 0.0, 0.0, 0.13],
#      [0.0, 0.0, 0.1, 0.75, 0.08, 0.0, 0.07], [0.0, 0.0, 0.0, 0.08, 0.84, 0.04, 0.04],
#      [0.0, 0.0, 0.0, 0.0, 0.37, 0.61, 0.02], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]
stateHist = state
mc = MarkovChain(p, statenames)

q_df = pd.DataFrame(columns=statenames, index=statenames)
i = 0
for statename in statenames:
    q_df.loc[statename] = p[i]
    i=i+1

print("\n Matriz de Transição:")
print(q_df)

#print(mc) #informacoes sobre a matriz

print("\n Matriz Fundamental:")
N = np.round(mc.fundamental_matrix, 4)
print(N)

print("\n Tempos de Absorção:")#duração esperada do estudo começando em um estágio específico até a graduação ou evasão)
print(np.round(mc.absorption_times, 4))

print("\n Duração esperada do estudo:")
print(np.trace(np.asarray(N)))#A duração esperada do estudo desde o primeiro ano até a formatura


#print(mc.recurrent_states)
#print(mc.transient_states)
#print(mc.steady_states)
#print(mc.expected_transitions(2))
#print(mc.topological_entropy)
#print(mc.walk(20))
#plot_walk(mc, 20, 'sequence')

for x in range(10):
    #probalidade dos estado
    #print(np.round(state, 3))
    state = np.dot(state, p)
    stateHist = np.append(stateHist, state, axis=0)
    dfDistrHist = pd.DataFrame(stateHist, columns=statenames)

print("\n Probabilidade graduação e evasão:")#considerando do estado inicial - para cada ano alterar matriz inicial
print(np.round(state, 3))

dfDistrHist.plot()