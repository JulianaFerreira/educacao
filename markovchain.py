from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from pydtmc import MarkovChain, plot_graph, plot_walk
from graph import Graph
from lifelines import KaplanMeierFitter

#TODO
#criar variável para proporção entre retidos e não retidos - FEITO
#adicionar estado trancado - FEITO
#analise de sobrevivencia/Survival regression/lifelines - FEITO
#tempo até retenção - FEITO
#criar versão considerando anos no curso # FEITO
#extrair formula - PARCIAL
#corrigir gráficos antigos


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
# Com Trancar
# A1
# A1toT = 0.1 * taxaTrancar
# A1toA1R = 0.25 * taxaRetencao
# A1toE = 0.12 * taxaEvasao
# A1toA2 = 1 - A1toA1R - A1toE - A1toT
# TtoA1 = 0.03 * taxaVoltar
#
# # A1R
# A1RtoT = A1toT * taxaTrancarR * taxaProporcaoTrancar
# A1RtoE = A1toE * taxaEvasaoR * taxaProporcaoEvasao
# A1RtoA2R = 1 - A1RtoE - A1RtoT
# TtoA1R = 0.02 * taxaVoltar
#
# # A2
# A2toT = 0.08 * taxaTrancar
# A2toA2R = 0.3 * taxaRetencao
# A2toE = 0.08 * taxaEvasao
# A2toA3 = 1 - A2toA2R - A2toE - A2toT
# TtoA2 = 0.03 * taxaVoltar
#
# # A2R
# A2RtoT = A2toT * taxaTrancarR * taxaProporcaoTrancar
# A2RtoE = A2toE * taxaEvasaoR * taxaProporcaoEvasao
# A2RtoA3R = 1 - A2RtoE - A2RtoT
# TtoA2R = 0.02 * taxaVoltar
#
# # A3
# A3toT = 0.04 * taxaTrancar
# A3toA3R = 0.2 * taxaRetencao
# A3toE = 0.1 * taxaEvasao
# A3toA4 = 1 - A3toA3R - A3toE - A3toT
# TtoA3 = 0.03 * taxaVoltar
#
# # A3R
# A3RtoT = A3toT * taxaTrancarR * taxaProporcaoTrancar
# A3RtoE = A3toE * taxaEvasaoR * taxaProporcaoEvasao
# A3RtoA4R = 1 - A3RtoE - A3RtoT
# TtoA3R = 0.02 * taxaVoltar
#
# # A4
# A4toT = 0.05 * taxaTrancar
# A4toA4R = 0.15 * taxaRetencao
# A4toE = 0.06 * taxaEvasao
# A4toA5 = 1 - A4toA4R - A4toE - A4toT
# TtoA4 = 0.03 * taxaVoltar
#
# # A4R
# A4RtoT = A4toT * taxaTrancarR * taxaProporcaoTrancar
# A4RtoE = A4toE * taxaEvasaoR * taxaProporcaoEvasao
# A4RtoA5R = 1 - A4RtoE - A4RtoT
# TtoA4R = 0.02 * taxaVoltar
#
# # A5
# A5toT = 0.02 * taxaTrancar
# A5toA5R = 0.2 * taxaRetencao
# A5toE = 0.03 * taxaEvasao
# A5toG = 1 - A5toA5R - A5toE - A5toT
# TtoA5 = 0.03 * taxaVoltar
#
# # A5R
# A5RtoT = A5toT * taxaTrancarR * taxaProporcaoTrancar
# A5RtoE = A5toE * taxaEvasaoR * taxaProporcaoEvasao
# A5RtoG = 1 - A5RtoE - A5RtoT
# TtoA5R = 0.02 * taxaVoltar
#
# # T
# TtoT = 0.6
# TtoE = 0.15



# Com mais anos e sem Trancar
# A1
A1toA1R = 0.25 * taxaRetencao
A1toE = 0.12 * taxaEvasao
A1toA2 = 1 - A1toA1R - A1toE

# A1R
A1RtoE = A1toE * taxaEvasaoR * taxaProporcaoEvasao
A1RtoA2R = 1 - A1RtoE

# A2
A2toA2R = 0.3 * taxaRetencao
A2toE = 0.08 * taxaEvasao
A2toA3 = 1 - A2toA2R - A2toE

# A2R
A2RtoE = A2toE * taxaEvasaoR * taxaProporcaoEvasao
A2RtoA3R = 1 - A2RtoE

# A3
A3toA3R = 0.2 * taxaRetencao
A3toE = 0.1 * taxaEvasao
A3toA4 = 1 - A3toA3R - A3toE

# A3R
A3RtoE = A3toE * taxaEvasaoR * taxaProporcaoEvasao
A3RtoA4R = 1 - A3RtoE

# A4
A4toA4R = 0.15 * taxaRetencao
A4toE = 0.06 * taxaEvasao
A4toA5 = 1 - A4toA4R - A4toE

# A4R
A4RtoE = A4toE * taxaEvasaoR * taxaProporcaoEvasao
A4RtoA5R = 1 - A4RtoE

# A5
A5toA5R = 0.2 * taxaRetencao
A5toE = 0.03 * taxaEvasao
A5toG = 1 - A5toA5R - A5toE

# A5R
A5RtoA6R = 0.3
A5RtoE = A5toE * taxaEvasaoR * taxaProporcaoEvasao
A5RtoG = 1 - A5RtoA6R - A5RtoE

# A6R
A6RtoA7R = 0.2
A6RtoE = 0.03 * taxaEvasaoR
A6RtoG = 1 - A6RtoE - A6RtoA7R

# A7R
A7RtoE = 0.02 * taxaEvasaoR
A7RtoG = 1 - A7RtoE



progres = [A1toA2, A2toA3, A3toA4, A4toA5, A5toG, A1RtoA2R, A2RtoA3R, A3RtoA4R, A4RtoA5R, A5RtoG]
ret = [A1toA1R, A2toA2R, A3toA3R, A4toA4R, A5toA5R]
#tranc = [A1toT, A2toT, A3toT, A4toT, A5toT, A1RtoT, A2RtoT, A3RtoT, A4RtoT, A5RtoT]

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
#      [TtoA1, TtoA2, TtoA3, TtoA4, TtoA5, TtoA1R, TtoA2R, TtoA3R, TtoA4R, TtoA5R, TtoT, 0.0, TtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

statenames = ['A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'A6R', 'A7R', 'G', 'E']
state = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
p = [[0.0, A1toA2, 0.0, 0.0, 0.0, A1toA1R, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A1toE],
     [0.0, 0.0, A2toA3, 0.0, 0.0, 0.0, A2toA2R, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A2toE],
     [0.0, 0.0, 0.0, A3toA4, 0.0, 0.0, 0.0, A3toA3R, 0.0, 0.0, 0.0, 0.0, 0.0, A3toE],
     [0.0, 0.0, 0.0, 0.0, A4toA5, 0.0, 0.0, 0.0, A4toA4R, 0.0, 0.0, 0.0, 0.0, A4toE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5toA5R, A5toG, 0.0, 0.0, A5toE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A1RtoA2R, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A1RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A2RtoA3R, 0.0, 0.0, 0.0, 0.0, 0.0, A2RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A3RtoA4R, 0.0, 0.0, 0.0, 0.0, A3RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A4RtoA5R, 0.0, 0.0, 0.0, A4RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5RtoA6R, 0.0, A5RtoG, A5RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A6RtoA7R, A6RtoG, A6RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A7RtoG, A7RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

# statenames = ['A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'G', 'E']
# state = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
# p = [[0.0, A1toA2, 0.0, 0.0, 0.0, A1toA1R, 0.0, 0.0, 0.0, 0.0, 0.0, A1toE],
#      [0.0, 0.0, A2toA3, 0.0, 0.0, 0.0, A2toA2R, 0.0, 0.0, 0.0, 0.0, A2toE],
#      [0.0, 0.0, 0.0, A3toA4, 0.0, 0.0, 0.0, A3toA3R, 0.0, 0.0, 0.0, A3toE],
#      [0.0, 0.0, 0.0, 0.0, A4toA5, 0.0, 0.0, 0.0, A4toA4R, 0.0, 0.0, A4toE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5toA5R, A5toG, A5toE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A1RtoA2R, 0.0, 0.0, 0.0, 0.0, A1RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A2RtoA3R, 0.0, 0.0, 0.0, A2RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A3RtoA4R, 0.0, 0.0, A3RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A4RtoA5R, 0.0, A4RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5RtoG, A5RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

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

p = np.round(p, 4)

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

    q_df.to_csv("matrix.csv")

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

# O tempo esperado que um aluno passa em um determinado estado e a duração prevista do estudo
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

# Gráfico Retenção
barplot("Probabilidade de Retenção", ret, statenames[:5])
plt.show()

print("\n Probabilidade de Retenção: ")
print(ret)

# Gráfico Progressão
dfGE = pd.DataFrame({'Não Retidos': progres[:5],
                    'Retidos': progres[-5:]}, index=statenames[:5])
dfGE.plot.bar(rot=0, color={"Não Retidos": "green", "Retidos": "red"}, title="Probabilidade de Progressão")
plt.show()

print("\n Probabilidade de Progressão: ")
print(np.round(progres, 4))

# Gráficos Graduação e Evasão individuais
# barplot("G", probGE.T[0], statenames[:len(statenames)-2])
# barplot("E", probGE.T[1], statenames[:len(statenames)-2])

# Gráfico Graduação e Evasão Agrupado
e = probGE.T[1]
g = probGE.T[0]

dfGE = pd.DataFrame({'Não Retidos': e[:5],
                    'Retidos': e[-5:]}, index=statenames[:5])
dfGE.plot.bar(rot=0, color={"Não Retidos": "green", "Retidos": "red"}, title="Probabilidade de Evasão")
plt.show()

dfGE = pd.DataFrame({'Não Retidos': g[:5],
                    'Retidos': g[-5:]}, index=statenames[:5])
dfGE.plot.bar(rot=0, color={"Não Retidos": "green", "Retidos": "red"}, title="Probabilidade de Graduação")
plt.show()


# Quantidade de anos para simulação
passosSimu = 10 # Sem trancar
# passosSimu = 15 # Com trancar

# Gráfico do histórico de distribuição
for x in range(passosSimu):
    # probalidade dos estado
    # print(np.round(state, 3))
    state = np.dot(state, p)
    stateHist = np.append(stateHist, state, axis=0)
    dfDistrHist = pd.DataFrame(stateHist, columns=statenames)


dfDistrHist.plot()
plt.show()
# print(dfDistrHist)


# Simulação
n = 1000
e = 0
g = 0
r = 0
t = 0
tempo = np.arange(0, passosSimu, 1)
time = np.array([])
tempo_ate_retido = []
tempo_ate_trancado = []
tempo_ate_evadido = []
tempo_ate_graduado = []
event_observedE = np.array([])
event_observedG = np.array([])
event_observedT = np.array([])
event_observedR = np.array([])

print(f"\nSimulação com {n} alunos")
for i in range(n):
    arr = mc.walk(passosSimu, 'A1')

    # Cria Arrays para analise de sobrevivencia e Verificar se foi G, E, T ou R em algum dos estados
    time = np.concatenate((tempo, time))
    estados = np.zeros((passosSimu,), dtype=int)
    if 'E' in arr:
        e += 1  # quantidade para probabilidade
        k = arr.index("E")
        tempo_ate_evadido.append(k + 1)
        estados[k] = 1
        # for k in range(len(estados)):
        #     estados[k] = 1
    event_observedE = np.concatenate((event_observedE, estados))

    estados = np.zeros((passosSimu,), dtype=int)
    if 'G' in arr:
        g += 1  # quantidade para probabilidade
        k = arr.index("G")
        tempo_ate_graduado.append(k + 1)
        estados[k] = 1
        # for k in range(len(estados)):
        #     estados[k] = 1
    event_observedG = np.concatenate((event_observedG, estados))

    #Trancado
    estados = np.zeros((passosSimu,), dtype=int)
    count = 0
    for estado in arr:
        if estado == 'T':
            estados[count] = 1
        count += 1
    event_observedT = np.concatenate((event_observedT, estados))

    if 'T' in arr:
        t += 1
        k = arr.index("T")
        tempo_ate_trancado.append(k + 1)

    # Retido
    estados = np.zeros((passosSimu,), dtype=int)
    count = 0
    for estado in arr:
        if 'R' in estado:
            estados[count] = 1
        count += 1
    event_observedR = np.concatenate((event_observedR, estados))

    # Se ficou Retido em algum dos estados
    count = 0
    for estado in arr:
        if 'R' in estado:
            tempo_ate_retido.append(count+1)
            r += 1
            break
        count += 1


print(f"\nProbabilidade de ser retido: {r/n*100} %")
print(f"Probabilidade de ser trancado: {t/n*100} %")
print(f"Probabilidade de evasão: {e/n*100} %")
print(f"Probabilidade de graduação: {g/n*100} %")
print(f"Tempo médio até ser retido: {np.round(np.mean(tempo_ate_retido),3)} anos")
print(f"Tempo médio até ser trancado: {np.round(np.mean(tempo_ate_trancado),3)} anos")
print(f"Tempo médio até ser evadido: {np.round(np.mean(tempo_ate_evadido),3)} anos")
print(f"Tempo médio até ser graduado: {np.round(np.mean(tempo_ate_graduado),3)} anos")

# Gráficos Análise de Sobrevivência
kmf = KaplanMeierFitter()
kmf.fit(time, event_observedE, label='Evadido')
kmf.plot_survival_function()
plt.show()
# kmf.plot_cumulative_density(ci_show=False)
# plt.show()

kmf = KaplanMeierFitter()
kmf.fit(time, event_observedG, label='Graduado')
kmf.plot_survival_function()
plt.show()
# kmf.plot_cumulative_density(ci_show=False)
# plt.show()

kmf = KaplanMeierFitter()
kmf.fit(time, event_observedR, label='Retido')
kmf.plot_survival_function()
plt.show()
# kmf.plot_cumulative_density(ci_show=False)
# plt.show()

kmf = KaplanMeierFitter()
kmf.fit(time, event_observedT, label='Trancado')
kmf.plot_survival_function()
plt.show()
# kmf.plot_cumulative_density(ci_show=False)
# plt.show()


# Desenha Cadeia de Markov
graph = Graph()
graph.creategraph(p)

# Outros
# print(mc.expected_transitions(1))
# print(mc.recurrent_states)
# print(mc.transient_states)
# print(mc.steady_states)
# print(mc.topological_entropy)
# plot_walk(mc, 10, 'A1')
