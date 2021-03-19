from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from pydtmc import MarkovChain, plot_graph, plot_walk
from graph import Graph
from plot import Plot

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
A1RtoE = 0.35 * taxaEvasaoR
A1RtoA2R = 1 - A1RtoE

# A2
A2toA2R = 0.25 * taxaRetencao
A2toE = 0.1 * taxaEvasao
A2toA3 = 1 - A2toA2R - A2toE

# A2R
A2RtoE = 0.28 * taxaEvasaoR
A2RtoA3R = 1 - A2RtoE

# A3
A3toA3R = 0.2 * taxaRetencao
A3toE = 0.1 * taxaEvasao
A3toA4 = 1 - A3toA3R - A3toE

# A3R
A3RtoE = 0.25 * taxaEvasaoR
A3RtoA4R = 1 - A3RtoE

# A4
A4toA4R = 0.15 * taxaRetencao
A4toE = 0.06 * taxaEvasao
A4toA5 = 1 - A4toA4R - A4toE

# A4R
A4RtoE = 0.18 * taxaEvasaoR
A4RtoA5R = 1 - A4RtoE

# A5
A5toA5R = 0.2 * taxaRetencao
A5toE = 0.03 * taxaEvasao
A5toG = 1 - A5toA5R - A5toE

# A5R
A5RtoE = 0.1 * taxaEvasaoR
A5RtoG = 1 - A5RtoE

progres = [A1toA2, A2toA3, A3toA4, A4toA5, A5toG, A1RtoA2R, A2RtoA3R, A3RtoA4R, A4RtoA5R, A5RtoG]
ret = [A1toA1R, A2toA2R, A3toA3R, A4toA4R, A5toA5R]

statenames = ['A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'G', 'E']
state = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
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

# statenames = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'G', 'W']
# state = np.array([[1, 0, 0, 0, 0, 0, 0, 0]])

# statenames = ['Inicio', 'A1', 'A2', 'A3', 'A4', 'Graduado', 'Evadido']
# state = np.array([[1, 0, 0, 0, 0, 0, 0]])
# p = [[0.0, 0.89, 0.09, 0.02, 0.0, 0.0, 0.0], [0.0, 0.17, 0.64, 0.06, 0.0, 0.0, 0.13],
#      [0.0, 0.0, 0.1, 0.75, 0.08, 0.0, 0.07], [0.0, 0.0, 0.0, 0.08, 0.84, 0.04, 0.04],
#      [0.0, 0.0, 0.0, 0.0, 0.37, 0.61, 0.02], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

# normalize rows to ensure p is a valid right stochastic matrix
#p = p / np.sum(p, axis=1)

plot = Plot()
graph = Graph()

#Desenha Cadeia de Markov
graph.creategraph(p)

stateHist = state
mc = MarkovChain(p, statenames)

q_df = pd.DataFrame(columns=statenames, index=statenames)
i = 0
for statename in statenames:
    q_df.loc[statename] = p[i]
    i = i + 1

# informacoes sobre a cadeia de markov
# print(mc)

#Progressão dos alunos entre diferentes estados
print("\n Matriz de Transição:")
print(q_df)

#O tempo esperado que um aluno passa em um determinado estado e a duração prevista do estudo
print("\n Matriz Fundamental:")
N = np.round(mc.fundamental_matrix, 3)
print(N)

# Tempos de Absorção
print("\n Duração esperada em cada ano até a graduação ou evasão")
print(np.round(mc.absorption_times, 3))

print("\n Duração média esperada até graduação:")
print(np.round(np.trace(np.asarray(N)), 3))

#f=NR
x = np.array(p)
x1 = x[:len(x)-2, len(x)-2]
x2 = x[:len(x)-2, len(x)-1]
R = np.array([x1, x2])
probGE = np.round(np.dot(R, N.T).T, 3)

for i in range(len(probGE)):
    print("\n Probabilidade graduação e evasão no estado " + statenames[i] + ":")
    print(probGE[i])

#Gráficos Graduação e Evasão
# plot.barplot("G", probGE.T[0], statenames[:len(statenames)-2])
# plot.barplot("E", probGE.T[1], statenames[:len(statenames)-2])

#Gráfico Retenção
plot.barplot("Probalididade de Retenção", ret, statenames[:5])

#Gráfico Progressão
dfGE = pd.DataFrame({'Não Retidos': progres[:5],
                    'Retidos': progres[-5:]}, index=statenames[:5])
dfGE.plot.bar(rot=0, color={"Não Retidos": "green", "Retidos": "red"}, title="Probabilidade de Progressão")

#Gráfico Graduação e Evasão Agrupado
e = probGE.T[1]
g = probGE.T[0]

dfGE = pd.DataFrame({'Não Retidos': e[:5],
                    'Retidos': e[-5:]}, index=statenames[:5])
dfGE.plot.bar(rot=0, color={"Não Retidos": "green", "Retidos": "red"}, title="Probabilidade de Evasão")

dfGE = pd.DataFrame({'Não Retidos': g[:5],
                    'Retidos': g[-5:]}, index=statenames[:5])
dfGE.plot.bar(rot=0, color={"Não Retidos": "green", "Retidos": "red"}, title="Probabilidade de Graduação")

#Gráfico do histórico de distribuição
for x in range(10):
    # probalidade dos estado
    # print(np.round(state, 3))
    state = np.dot(state, p)
    stateHist = np.append(stateHist, state, axis=0)
    dfDistrHist = pd.DataFrame(stateHist, columns=statenames)

dfDistrHist.plot()
# print(dfDistrHist)


#outros
#print(mc.expected_transitions(6))
# print(mc.recurrent_states)
# print(mc.transient_states)
# print(mc.steady_states)
# print(mc.expected_transitions(1))
# print(mc.topological_entropy)
# print(mc.walk(20))
# plot_walk(mc, 10, 'A1')
