import pandas as pd
import numpy as np
from markov_diagram import Diagram

#Alterar aqui parametros para gerar matriz
nomeArquivo = "matrix/matrixM.csv"
taxaRetencao = 1.25
taxaEvasao = 1.25
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
# # A1
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
# tranc = [A1toT, A2toT, A3toT, A4toT, A5toT, A1RtoT, A2RtoT, A3RtoT, A4RtoT, A5RtoT]

# states = ['A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'T', 'G', 'E']
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

states = ['A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'A6R', 'A7R', 'G', 'E']
state = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
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

# states = ['A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'G', 'E']
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

# states = ['Y1', 'Y2', 'Y3', 'Y4', 'I', 'G', 'W']
# state = np.array([[1, 0, 0, 0, 0, 0, 0]])
# p = [[0.057, 0.31, 0.0, 0.0, 0.603, 0.0, 0.03],
#      [0.0, 0.187, 0.528, 0.0, 0.285, 0.0, 0.0],
#      [0.0, 0.0, 0.012, 0.563, 0.097, 0.328, 0.0],
#      [0.0, 0.0, 0.0, 0.039, 0.094, 0.814, 0.053],
#      [0.001, 0.036, 0.02, 0.0, 0.0, 0.003, 0.94],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

# states = ['Inicio', 'A1', 'A2', 'A3', 'A4', 'Graduado', 'Evadido']
# state = np.array([[1, 0, 0, 0, 0, 0, 0]])
# p = [[0.0, 0.89, 0.09, 0.02, 0.0, 0.0, 0.0], [0.0, 0.17, 0.64, 0.06, 0.0, 0.0, 0.13],
#      [0.0, 0.0, 0.1, 0.75, 0.08, 0.0, 0.07], [0.0, 0.0, 0.0, 0.08, 0.84, 0.04, 0.04],
#      [0.0, 0.0, 0.0, 0.0, 0.37, 0.61, 0.02], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]


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
    n = 1+ max(transitions) #number of states

    M = [[0]*n for _ in range(n)]

    for (i,j) in zip(transitions, transitions[1:]):
        M[i][j] += 1

    #now convert to probabilities:
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]
    return M


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

# states = ['A1', 'A2', 'A3', 'A4', 'A5', 'G', 'E']
# n = [100, 90, 80, ]
#
# #calcula o p
# p = 0
#
# transitionMatrix = np.zeros((len(states), len(states)))





