from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from pydtmc import MarkovChain, plot_graph, plot_walk
from graph import Graph

plt.ion()

taxaRetencao = 1.0
taxaEvasao = 1.0
taxaEvasaoR = 1.0

# taxa dos estados
# A1
A1toA1R = 0.3 * taxaRetencao
A1toE = 0.1 * taxaEvasao
A1toA2 = 1 - A1toA1R - A1toE

# A1R
A1RtoE = 0.4 * taxaEvasaoR
A1RtoA2R = 1 - A1RtoE

# A2
A2toA2R = 0.25 * taxaRetencao
A2toE = 0.1 * taxaEvasao
A2toA3 = 1 - A2toA2R - A2toE

# A2R
A2RtoE = 0.3 * taxaEvasaoR
A2RtoA3R = 1 - A2RtoE

# A3
A3toA3R = 0.2 * taxaRetencao
A3toE = 0.15 * taxaEvasao
A3toA4 = 1 - A3toA3R - A3toE

# A3R
A3RtoE = 0.35 * taxaEvasaoR
A3RtoA4R = 1 - A3RtoE

# A4
A4toA4R = 0.15 * taxaRetencao
A4toE = 0.1 * taxaEvasao
A4toA5 = 1 - A4toA4R - A4toE

# A4R
A4RtoE = 0.2 * taxaEvasaoR
A4RtoA5R = 1 - A4RtoE

# A5
A5toA5R = 0.2 * taxaRetencao
A5toE = 0.05 * taxaEvasao
A5toG = 1 - A5toA5R - A5toE

# A5R
A5RtoE = 0.15 * taxaEvasaoR
A5RtoG = 1 - A5RtoE

statenames = ['A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'Graduado', 'Evadido']
state = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]])
p = [[0.0, A1toA2, 0.0, 0.0, 0.0, A1toA1R, 0.0, 0.0, 0.0, 0.0, 0.0, A1toE],
     [0.0, 0.0, A2toA3, 0.0, 0.0, 0.0, A2toA2R, 0.0, 0.0, 0.0, 0.0, A2toE],
     [0.0, 0.0, 0.0, A3toA4, 0.0, 0.0, 0.0, A3toA3R, 0.0, 0.0, 0.0, A3toE],
     [0.0, 0.0, 0.0, 0.0, A4toA5, 0.0, 0.0, 0.0, A4toA4R, 0.0, 0.0, A4toE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5toA5R, A5toG, A5toE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A1RtoA2R, 0.0, 0.0, 0.0, 0.0, A1RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A2RtoA3R, 0.0, 0.0, 0.0, A2RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A3RtoA4R, 0.0, 0.0, A3RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A4RtoA5R, 0.0, A4RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5RtoG, A5RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

# statenames = ['Ingressante', 'A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'Trancado', 'Graduado', 'Evadido']
# state = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

# statenames = ['Y1', 'Y2', 'Y3', 'Y4', 'I', 'G', 'W']
# state = np.array([[1, 0, 0, 0, 0, 0, 0]])
# p = [[0.057, 0.31, 0.0, 0.0, 0.603, 0.0, 0.03],
#      [0.0, 0.187, 0.528, 0.0, 0.285, 0.0, 0.0],
#      [0.0, 0.0, 0.012, 0.563, 0.097, 0.328, 0.0],
#      [0.0, 0.0, 0.0, 0.039, 0.094, 0.814, 0.053],
#      [0.001, 0.036, 0.02, 0.0, 0.0, 0.003, 0.94],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

# statenames = ['Inicio', 'A1', 'A2', 'A3', 'A4', 'Graduado', 'Evadido']
# state = np.array([[1, 0, 0, 0, 0, 0, 0]])
# p = [[0.0, 0.89, 0.09, 0.02, 0.0, 0.0, 0.0], [0.0, 0.17, 0.64, 0.06, 0.0, 0.0, 0.13],
#      [0.0, 0.0, 0.1, 0.75, 0.08, 0.0, 0.07], [0.0, 0.0, 0.0, 0.08, 0.84, 0.04, 0.04],
#      [0.0, 0.0, 0.0, 0.0, 0.37, 0.61, 0.02], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

stateHist = state
mc = MarkovChain(p, statenames)

q_df = pd.DataFrame(columns=statenames, index=statenames)
for i, statename in statenames:
    q_df.loc[statename] = p[i]

print("\n Matriz de Transição:")
print(q_df)

# print(mc) #informacoes sobre a matriz

print("\n Matriz Fundamental:")
N = np.round(mc.fundamental_matrix, 4)
print(N)

print("\n Tempos de Absorção:")  # duração esperada do estudo começando em um estágio específico até a graduação ou evasão)
print(np.round(mc.absorption_times, 4))

print("\n Duração esperada do estudo:")
print(np.trace(np.asarray(N)))  # A duração esperada do estudo desde o primeiro ano até a formatura

print("\n test:")
print(mc.expected_transitions(1))

# print(mc.recurrent_states)
# print(mc.transient_states)
# print(mc.steady_states)
# print(mc.expected_transitions(2))
# print(mc.topological_entropy)
# print(mc.walk(20))
# plot_walk(mc, 20, 'sequence')

for x in range(10):
    # probalidade dos estado
    # print(np.round(state, 3))
    state = np.dot(state, p)
    stateHist = np.append(stateHist, state, axis=0)
    dfDistrHist = pd.DataFrame(stateHist, columns=statenames)

print("\n Probabilidade graduação e evasão:")  # considerando do estado inicial - para cada ano alterar matriz inicial
print(np.round(state, 3))

dfDistrHist.plot()

graph = Graph()
graph.creategraph(p)
