from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from pydtmc import MarkovChain, plot_graph, plot_walk
from graph import Graph
from lifelines import KaplanMeierFitter
plt.ion()

#TODO
#criar variável para proporção entre retidos e não retidos - FEITO
#adicionar estado trancado - FEITO - ERRADO TEM QUE SER 1 PRA CADA ESTADO!!!
#extrair formula
#analise de sobrevivencia/lifelines
#A1+A1R até E com gráfico
#tempo até retenção - Não passa por varios estados, faz sentido? talvez com o estado trancado
#criar versão considerando anos no curso

#criar classe com a matriz e seus dados assim eu não enlouqueço


taxaRetencao = 1.0
taxaEvasao = 1.0
taxaEvasaoR = 1.0
taxaTrancar = 1.0
taxaTrancarR = 1.0
taxaVoltar = 1.0
taxaVoltarR = 1.0
taxaProporcaoEvasao = 1.75
taxaProporcaoTrancar = 2.0
taxaProporcaoVoltar = 1.0

# Probabilidade dos estados
# A1
A1toT = 0 * taxaTrancar
#A1toT = 0.15 * taxaTrancar
A1toA1R = 0.3 * taxaRetencao
A1toE = 0.1 * taxaEvasao
A1toA2 = 1 - A1toA1R - A1toE - A1toT
TtoA1 = 0.1 * taxaVoltar

# A1R
A1RtoT = A1toT * taxaTrancarR * taxaProporcaoTrancar
A1RtoE = A1toE * taxaEvasaoR * taxaProporcaoEvasao
A1RtoA2R = 1 - A1RtoE - A1RtoT
TtoA1R = 0.1 * taxaVoltar

# A2
A2toT = 0 * taxaTrancar
#A2toT = 0.12 * taxaTrancar
A2toA2R = 0.25 * taxaRetencao
A2toE = 0.1 * taxaEvasao
A2toA3 = 1 - A2toA2R - A2toE - A2toT
TtoA2 = 0.1 * taxaVoltar

# A2R
A2RtoT = A2toT * taxaTrancarR * taxaProporcaoTrancar
A2RtoE = A2toE * taxaEvasaoR * taxaProporcaoEvasao
A2RtoA3R = 1 - A2RtoE - A2RtoT
TtoA2R = 0.1 * taxaVoltar

# A3
A3toT = 0 * taxaTrancar
#A3toT = 0.08 * taxaTrancar
A3toA3R = 0.2 * taxaRetencao
A3toE = 0.1 * taxaEvasao
A3toA4 = 1 - A3toA3R - A3toE - A3toT
TtoA3 = 0.1 * taxaVoltar

# A3R
A3RtoT = A3toT * taxaTrancarR * taxaProporcaoTrancar
A3RtoE = A3toE * taxaEvasaoR * taxaProporcaoEvasao
A3RtoA4R = 1 - A3RtoE - A3RtoT
TtoA3R = 0.1 * taxaVoltar

# A4
A4toT = 0 * taxaTrancar
#A4toT = 0.1 * taxaTrancar
A4toA4R = 0.15 * taxaRetencao
A4toE = 0.06 * taxaEvasao
A4toA5 = 1 - A4toA4R - A4toE - A4toT
TtoA4 = 0.1 * taxaVoltar

# A4R
A4RtoT = A4toT * taxaTrancarR * taxaProporcaoTrancar
A4RtoE = A4toE * taxaEvasaoR * taxaProporcaoEvasao
A4RtoA5R = 1 - A4RtoE - A4RtoT
TtoA4R = 0.1 * taxaVoltar

# A5
A5toT = 0.0 * taxaTrancar
#A5toT = 0.05 * taxaTrancar
A5toA5R = 0.2 * taxaRetencao
A5toE = 0.03 * taxaEvasao
A5toG = 1 - A5toA5R - A5toE - A5toT
TtoA5 = 0.1 * taxaVoltar

# A5R
A5RtoT = A5toT * taxaTrancarR * taxaProporcaoTrancar
A5RtoE = A5toE * taxaEvasaoR * taxaProporcaoEvasao
A5RtoG = 1 - A5RtoE - A5RtoT
TtoA5R = 0.1 * taxaVoltar

progres = [A1toA2, A2toA3, A3toA4, A4toA5, A5toG, A1RtoA2R, A2RtoA3R, A3RtoA4R, A4RtoA5R, A5RtoG]
ret = [A1toA1R, A2toA2R, A3toA3R, A4toA4R, A5toA5R]
tranc = [A1toT, A2toT, A3toT, A4toT, A5toT, A1RtoT, A2RtoT, A3RtoT, A4RtoT, A5RtoT]

# statenames = ['A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'T', 'G', 'E']
# state = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
# p = [[0.0, A1toA2, 0.0, 0.0, 0.0, A1toA1R, 0.0, 0.0, 0.0, 0.0, A1toT, 0.0, A1toE],
#      [0.0, 0.0, A2toA3, 0.0, 0.0, 0.0, A2toA2R, 0.0, 0.0, 0.0, A2toT, 0.0, A2toE],
#      [0.0, 0.0, 0.0, A3toA4, 0.0, 0.0, 0.0, A3toA3R, 0.0, 0.0, A3toT, 0.0, A3toE],
#      [0.0, 0.0, 0.0, 0.0, A4toA5, 0.0, 0.0, 0.0, A4toA4R, 0.0, A4toT, 0.0, A4toE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5toA5R, A5toT, A5toG, A5toE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A1RtoA2R, 0.0, 0.0, 0.0, A1RtoT, 0.0, A1RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A2RtoA3R, 0.0, 0.0, A2RtoT, 0.0, A2RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A3RtoA4R, 0.0, A3RtoT, 0.0, A3RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A4RtoA5R, A4RtoT, 0.0, A4RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5RtoT, A5RtoG, A5RtoE],
#      [TtoA1, TtoA2, TtoA3, TtoA4, TtoA5, TtoA1R, TtoA2R, TtoA3R, TtoA4R, TtoA5R, 0.0, 0.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

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

#Desenha Cadeia de Markov
graph = Graph()
graph.creategraph(p)

stateHist = state
mc = MarkovChain(p, statenames)

def barplot(title, height, bars):
    # Make a dataset:
    y_pos = np.arange(len(bars))

    # Create bars
    plt.bar(y_pos, height)
    plt.title(title)

    # Create names on the x-axis
    plt.xticks(y_pos, bars)

    # Show graphic
    plt.show()

def matriz_transicao():
    q_df = pd.DataFrame(columns=statenames, index=statenames)
    i = 0
    for statename in statenames:
        q_df.loc[statename] = p[i]
        i += 1

    # Progressão dos alunos entre diferentes estados
    print("\n Matriz de Transição:")
    print(q_df)

def prob_absor():
    # f=NR
    x = np.array(p)
    x1 = x[:len(x) - 2, len(x) - 2]
    x2 = x[:len(x) - 2, len(x) - 1]
    R = np.array([x1, x2])

    return np.round(np.dot(R, N.T).T, 3)

# informacoes sobre a cadeia de markov
# print(mc)

matriz_transicao()

#O tempo esperado que um aluno passa em um determinado estado e a duração prevista do estudo
print("\n Matriz Fundamental:")
N = np.round(mc.fundamental_matrix, 3)
print(N)

# Tempos de Absorção
print("\n Duração esperada em cada ano até a graduação ou evasão")
print(np.round(mc.absorption_times, 3))

print("\n Duração média esperada até graduação:")
# Sem estados retidos
#print(np.round(np.trace(np.asarray(N)), 3))
# Com estados retidos
print(np.round(np.trace((np.asarray(N)/2)), 3))


probGE = prob_absor()
for i in range(len(probGE)):
    print("\n Probabilidade graduação e evasão no estado " + statenames[i] + ":")
    print(probGE[i])

#Gráfico Retenção
barplot("Probabilidade de Retenção", ret, statenames[:5])

print("\n Probabilidade de Retenção: ")
print(ret)

#Gráfico Progressão
dfGE = pd.DataFrame({'Não Retidos': progres[:5],
                    'Retidos': progres[-5:]}, index=statenames[:5])
dfGE.plot.bar(rot=0, color={"Não Retidos": "green", "Retidos": "red"}, title="Probabilidade de Progressão")

print("\n Probabilidade de Progressão: ")
print(progres)

#Gráficos Graduação e Evasão individuais
# barplot("G", probGE.T[0], statenames[:len(statenames)-2])
# barplot("E", probGE.T[1], statenames[:len(statenames)-2])

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
for x in range(15):
    # probalidade dos estado
    #print(np.round(state, 3))
    state = np.dot(state, p)
    stateHist = np.append(stateHist, state, axis=0)
    dfDistrHist = pd.DataFrame(stateHist, columns=statenames)


dfDistrHist.plot()
#print(dfDistrHist)


#Simulação
n = 100
e = 0
g = 0
r = 0
for i in range(n):
    arr = mc.walk(8, 'A1')

    #Se ficou Retido em algum dos estados
    if ():
        r += 1

    #Quantos Graduados e Evadidos
    if (arr[-1] == 'G'):
        g += 1
    else:
        e += 1


print("Probabilidade de evasão: " + e/n)
print("Probabilidade de graduação: " + g/n)
print("Probabilidade de ser retido: " + r/n)


#lifelines
# dfDistrHist.insert(0, 'T', [0, 1, 2, 3, 4, 5, 6, 7, 8], True)
#
# T = dfDistrHist['T']
# E = dfDistrHistTotal['E']
#
# kmf = KaplanMeierFitter()
# kmf.fit(T, event_observed=E)
# kmf.survival_function_
# kmf.cumulative_density_
# kmf.plot_survival_function()



#outros
# print(mc.expected_transitions(1))
# print(mc.recurrent_states)
# print(mc.transient_states)
# print(mc.steady_states)
# print(mc.topological_entropy)
# plot_walk(mc, 10, 'A1')