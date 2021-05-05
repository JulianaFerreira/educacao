import pandas as pd
import numpy as np
from markov_diagram import Diagram

from pydtmc import MarkovChain, plot_graph, plot_walk

# Alterar aqui parametros para gerar matriz
nomeArquivo = "matrix/matrixBoumiAlterado.csv"
taxaRetencao = 1.0
taxaEvasao = 1.0
taxaEvasaoA1 = 1.0
taxaEvasaoA2 = 1.0
taxaTrancar = 1.0
taxaEvasaoR = 1.0
taxaTrancarR = 1.0
taxaProporcaoEvasao = 1.5
taxaProporcaoTrancar = 1.25


# T - representado por self loop
# A1T = 0.05 * taxaTrancar
# A1RT = A1T * taxaTrancarR * taxaProporcaoTrancar
# A2T = 0.04 * taxaTrancar
# A2RT = A2T * taxaTrancarR * taxaProporcaoTrancar
# A3T = 0.03 * taxaTrancar
# A3RT = A3T * taxaTrancarR * taxaProporcaoTrancar
# A4T = 0.02 * taxaTrancar
# A4RT = A4T * taxaTrancarR * taxaProporcaoTrancar
# A5T = 0.02 * taxaTrancar
# A5RT = A5T * taxaTrancarR * taxaProporcaoTrancar
# A6RT = 0.01 * taxaTrancarR
# A7RT = 0.01 * taxaTrancarR

# Reter
A1toA1R = 0.25 * taxaRetencao
A2toA2R = 0.3 * taxaRetencao
A3toA3R = 0.2 * taxaRetencao
A4toA4R = 0.15 * taxaRetencao
A5toA5R = 0.2 * taxaRetencao

# Evadir
A1toE = 0.12 * taxaEvasao * taxaEvasaoA1
A1RtoE = A1toE * taxaEvasaoR * taxaProporcaoEvasao
A2toE = 0.1 * taxaEvasao * taxaEvasaoA2
A2RtoE = A2toE * taxaEvasaoR * taxaProporcaoEvasao
A3toE = 0.07 * taxaEvasao
A3RtoE = A3toE * taxaEvasaoR * taxaProporcaoEvasao
A4toE = 0.05 * taxaEvasao
A4RtoE = A4toE * taxaEvasaoR * taxaProporcaoEvasao
A5toE = 0.03 * taxaEvasao
A5RtoE = A5toE * taxaEvasaoR * taxaProporcaoEvasao
A6RtoE = 0.02 * taxaEvasaoR
A7RtoE = 0.01 * taxaEvasaoR

# Próximo estado
A1toA2 = 1 - A1toA1R - A1toE
A1RtoA2R = 1 - A1RtoE
A2toA3 = 1 - A2toA2R - A2toE
A2RtoA3R = 1 - A2RtoE
A3toA4 = 1 - A3toA3R - A3toE
A3RtoA4R = 1 - A3RtoE
A4toA5 = 1 - A4toA4R - A4toE
A4RtoA5R = 1 - A4RtoE
# A1toA2 = 1 - A1toA1R - A1toE - A1T
# A1RtoA2R = 1 - A1RtoE - A1RT
# A2toA3 = 1 - A2toA2R - A2toE - A2T
# A2RtoA3R = 1 - A2RtoE - A2RT
# A3toA4 = 1 - A3toA3R - A3toE - A3T
# A3RtoA4R = 1 - A3RtoE - A3RT
# A4toA5 = 1 - A4toA4R - A4toE - A4T
# A4RtoA5R = 1 - A4RtoE - A4RT
A5RtoA6R = 0.3
A6RtoA7R = 0.2

# Graduar
A5toG = 1 - A5toA5R - A5toE
A5RtoG = 1 - A5RtoA6R - A5RtoE
A6RtoG = 1 - A6RtoE - A6RtoA7R
A7RtoG = 1 - A7RtoE
# A5toG = 1 - A5toA5R - A5toE - A5T
# A5RtoG = 1 - A5RtoA6R - A5RtoE - A5RT
# A6RtoG = 1 - A6RtoE - A6RtoA7R - A6RT
# A7RtoG = 1 - A7RtoE - A7RT


progres = [A1toA2, A2toA3, A3toA4, A4toA5, A5toG, A1RtoA2R, A2RtoA3R, A3RtoA4R, A4RtoA5R, A5RtoG]
ret = [A1toA1R, A2toA2R, A3toA3R, A4toA4R, A5toA5R]
# tranc = [A1toT, A2toT, A3toT, A4toT, A5toT, A1RtoT, A2RtoT, A3RtoT, A4RtoT, A5RtoT]

states = ['A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'A6R', 'A7R', 'G', 'E']
state = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
# Sem tracamento
p = [[0.0, A1toA2, 0.0, 0.0, 0.0, A1toA1R, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A1toE],
     [0.0, 0.0, A2toA3, 0.0, 0.0, 0.0, A2toA2R, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A2toE],
     [0.0, 0.0, 0.0, A3toA4, 0.0, 0.0, 0.0, A3toA3R, 0.0, 0.0, 0.0, 0.0, 0.0, A3toE],
     [0.0, 0.0, 0.0, 0.0, A4toA5, 0.0, 0.0, 0.0, A4toA4R, 0.0, 0.0, 0.0, 0.0, A4toE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5toA5R, 0.0, 0.0, A5toG, A5toE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A1RtoA2R, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A1RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A2RtoA3R, 0.0, 0.0, 0.0, 0.0, 0.0, A2RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A3RtoA4R, 0.0, 0.0, 0.0, 0.0, A3RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A4RtoA5R, 0.0, 0.0, 0.0, A4RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5RtoA6R, 0.0, A5RtoG, A5RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A6RtoA7R, A6RtoG, A6RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A7RtoG, A7RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

# Com trancamento
# p = [[A1T, A1toA2, 0.0, 0.0, 0.0, A1toA1R, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A1toE],
#      [0.0, A2T, A2toA3, 0.0, 0.0, 0.0, A2toA2R, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A2toE],
#      [0.0, 0.0, A3T, A3toA4, 0.0, 0.0, 0.0, A3toA3R, 0.0, 0.0, 0.0, 0.0, 0.0, A3toE],
#      [0.0, 0.0, 0.0, A4T, A4toA5, 0.0, 0.0, 0.0, A4toA4R, 0.0, 0.0, 0.0, 0.0, A4toE],
#      [0.0, 0.0, 0.0, 0.0, A5T, 0.0, 0.0, 0.0, 0.0, A5toA5R, 0.0, 0.0, A5toG, A5toE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, A1RT, A1RtoA2R, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A1RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A2RT, A2RtoA3R, 0.0, 0.0, 0.0, 0.0, 0.0, A2RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A3RT, A3RtoA4R, 0.0, 0.0, 0.0, 0.0, A3RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A4RT, A4RtoA5R, 0.0, 0.0, 0.0, A4RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5RT, A5RtoA6R, 0.0, A5RtoG, A5RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A6RT, A6RtoA7R, A6RtoG, A6RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A7RT, A7RtoG, A7RtoE],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]


# # Simples para testes
# states = ['A1', 'A2', 'G', 'E']
# p = [[0.0, 0.7, 0.0, 0.3],
#      [0.0, 0.0, 0.8, 0.2],
#      [0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 1.0]]



# Bairagi
# states = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S1R', 'S2R', 'S3R', 'S4R', 'S5R', 'S6R', 'G', 'E']
# state = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
# p = [[0.0, 0.5753, 0.0, 0.0, 0.0, 0.0, 0.3973, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0274],
#      [0.0, 0.0, 0.3750, 0.0, 0.0, 0.0, 0.0, 0.5104, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1146],
#      [0.0, 0.0, 0.0, 0.477, 0.0, 0.0, 0.0, 0.0, 0.4615, 0.0, 0.0, 0.0, 0.0, 0.0615],
#      [0.0, 0.0, 0.0, 0.0, 0.6383, 0.0, 0.0, 0.0, 0.0, 0.3617, 0.0, 0.0, 0.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.8286, 0.0, 0.0, 0.0, 0.0, 0.1714, 0.0, 0.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1142, 0.7429, 0.1429],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1 - 0.0411, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0411],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1 - 0.1719, 0.0, 0.0, 0.0, 0.0, 0.1719],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1 - 0.09225, 0.0, 0.0, 0.0, 0.09225],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8571, 0.1429],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]


# Brezav
# states = ['A1', 'A2', 'A3', 'A4', 'A1R', 'A2R', 'A3R', 'A4R', 'G', 'E']
# states = ['A1', 'A2', 'A3', 'A4', 'T', 'G', 'E']
# state = np.array([[1, 0, 0, 0, 0, 0, 0]])
# p = [[0.057, 0.31, 0.0, 0.0, 0.603, 0.0, 0.03],
#      [0.0, 0.187, 0.528, 0.0, 0.285, 0.0, 0.0],
#      [0.0, 0.0, 0.012, 0.563, 0.097, 0.328, 0.0],
#      [0.0, 0.0, 0.0, 0.039, 0.094, 0.814, 0.053],
#      [0.001, 0.036, 0.02, 0.0, 0.0, 0.003, 0.94],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]


# Boumi
# Chance de graduar 68,12%
# states = ['Inicio', 'A1', 'A2', 'A3', 'A4', 'G', 'E']
# state = np.array([[1, 0, 0, 0, 0, 0, 0]])
# p = [[0.0, 0.89, 0.09, 0.02, 0.0, 0.0, 0.0],
#      [0.0, 0.17, 0.64, 0.06, 0.0, 0.0, 0.13],
#      [0.0, 0.0, 0.1, 0.75, 0.08, 0.0, 0.07],
#      [0.0, 0.0, 0.0, 0.08, 0.84, 0.04, 0.04],
#      [0.0, 0.0, 0.0, 0.0, 0.37, 0.61, 0.02],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]


# Reter
A1toA1R = 0.17 * taxaRetencao
A2toA2R = 0.1 * taxaRetencao
A3toA3R = 0.08 * taxaRetencao
A4toA4R = 0.37 * taxaRetencao

# Evadir
A1toE = 0.13 * taxaEvasao * taxaEvasaoA1
A1RtoE = A1toE * taxaEvasaoR * taxaProporcaoEvasao
A2toE = 0.07 * taxaEvasao * taxaEvasaoA2
A2RtoE = A2toE * taxaEvasaoR * taxaProporcaoEvasao
A3toE = 0.04 * taxaEvasao
A3RtoE = A3toE * taxaEvasaoR * taxaProporcaoEvasao
A4toE = 0.02 * taxaEvasao
A4RtoE = A4toE * taxaEvasaoR * taxaProporcaoEvasao
A5RtoE = 0.02 * taxaEvasaoR
A6RtoE = 0.02/2 * taxaEvasaoR

# Próximo estado
A1toA2 = 1 - A1toA1R - A1toE - 0.06
A1RtoA2R = 1 - A1RtoE
A2toA3 = 1 - A2toA2R - A2toE - 0.08
A2RtoA3R = 1 - A2RtoE
A3toA4 = 1 - A3toA3R - A3toE
A3RtoA4R = 1 - A3RtoE
A4RtoA5R = 0.37
A5RtoA6R = 0.37/2

A4toG = 1 - A4toA4R - A4toE
A4RtoG = 1 - A4RtoA5R - A4RtoE
A5RtoG = 1 - A5RtoA6R - A5RtoE
A6RtoG = 1 - A6RtoE

states = ['A1', 'A2', 'A3', 'A4', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'A6R', 'G', 'E']
state = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

p = [[0.0, A1toA2, 0.06, 0.0, A1toA1R, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A1toE],
     [0.0, 0.0, A2toA3, 0.08, 0.0, A2toA2R, 0.0, 0.0, 0.0, 0.0, 0.0, A2toE],
     [0.0, 0.0, 0.0, A3toA4, 0.0, 0.0, A3toA3R, 0.0, 0.0, 0.0, 0.0, A3toE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A4toA4R, 0.0, 0.0, A4toG, A4toE],
     [0.0, 0.0, 0.0, 0.0, 0.0, A1RtoA2R, 0.0, 0.0, 0.0, 0.0, 0.0, A1RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A2RtoA3R, 0.0, 0.0, 0.0, 0.0, A2RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A3RtoA4R, 0.0, 0.0, 0.0, A3RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A4RtoA5R, 0.0, A4RtoG, A4RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5RtoA6R, A5RtoG, A5RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A6RtoG, A6RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]


# Gerar csv com matriz de transicao e desenho da cadeia de markov
def generate_csv_and_diagram(arquivo, states, p):
    q_df = pd.DataFrame(columns=states, index=states)
    i = 0
    for state in states:
        q_df.loc[state] = p[i]
        i += 1

    q_df.to_csv(arquivo)

    # Desenha Cadeia de Markov
    d = Diagram(arquivo)
    d.make_markov_diagram()


# Cria matriz de transição passando um array com os estados transicionando
def transition_matrix(transitions):
    n = 1 + max(transitions) #number of states

    M = [[0]*n for _ in range(n)]

    for (i, j) in zip(transitions, transitions[1:]):
        M[i][j] += 1

    #now convert to probabilities:
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]
    return M


def aplicar_parametros(p):
    p[:, 0] = 1

    return p



# estados transicionando
# t = [1,1,2,6,8,5,5,7,8,8,1,1,4,5,5,0,0,0,1,1,4,4,5,1,3,3,4,5,4,1,1]
# states = np.unique(t)
# p = transition_matrix(t)


p = np.round(p, 4)
generate_csv_and_diagram(nomeArquivo, states, p)


# Transition probabilities matrix
p = pd.read_csv(nomeArquivo, index_col=0)
print("\n Matriz de Transição:")
print(p)



#Teste gerar matriz de transicao

# states = ['A1', 'A2', 'A3', 'G', 'E']
# n = [100, 90, 80, 70, 0]
#
# #calcula o p
#
# p = np.zeros((len(states), len(states)))
#
# for i in range(len(p)-1):
#     for j in range(len(p)-1):
#         if j == i+1:
#             p[i][j] = 1
#
# print(p)


# df["E"] = 1.25 * df["E"]
# df["col"] = 0.75 * df["col"]



# Testes

# def prob_absor(p, N):
#     # f=NR
#     x = np.array(p)
#     x1 = x[:len(x) - 2, len(x) - 2]
#     x2 = x[:len(x) - 2, len(x) - 1]
#     R = np.array([x1, x2])
#
#     return np.round(np.dot(R, N.T).T, 3)
#
# stateHist = state
# mc = MarkovChain(p, states)
#
# # informacoes sobre a cadeia de markov
# # print(mc)
#
# # O tempo esperado que um aluno passa em um determinado estado e a duração prevista do estudo
# print("\n Matriz Fundamental:")
# N = np.round(mc.fundamental_matrix, 3)
# print(N)
#
# # Tempos de Absorção
# print("\n Duração esperada em cada ano até a graduação ou evasão")
# print(np.round(mc.absorption_times, 3))
#
# print("\n Duração média esperada até graduação:")
# # Sem estados retidos
# print(np.round(np.trace(np.asarray(N)), 3))
# # Com estados retidos
# # print(np.round(np.trace((np.asarray(N) / 2)), 3))
#
# probGE = prob_absor(p, N)
# for i in range(len(probGE)):
#     print("\n Probabilidade graduação e evasão no estado " + states[i] + ":")
#     print(probGE[i])
