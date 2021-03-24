import quantecon as qe
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

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
#A1toT = 0 * taxaTrancar
A1toT = 0.15 * taxaTrancar
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
#A2toT = 0 * taxaTrancar
A2toT = 0.12 * taxaTrancar
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
#A3toT = 0 * taxaTrancar
A3toT = 0.08 * taxaTrancar
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
#A4toT = 0 * taxaTrancar
A4toT = 0.1 * taxaTrancar
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
#A5toT = 0.0 * taxaTrancar
A5toT = 0.05 * taxaTrancar
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

statenames = ['A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'T', 'G', 'E']
state = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
P = [[0.0, A1toA2, 0.0, 0.0, 0.0, A1toA1R, 0.0, 0.0, 0.0, 0.0, A1toT, 0.0, A1toE],
     [0.0, 0.0, A2toA3, 0.0, 0.0, 0.0, A2toA2R, 0.0, 0.0, 0.0, A2toT, 0.0, A2toE],
     [0.0, 0.0, 0.0, A3toA4, 0.0, 0.0, 0.0, A3toA3R, 0.0, 0.0, A3toT, 0.0, A3toE],
     [0.0, 0.0, 0.0, 0.0, A4toA5, 0.0, 0.0, 0.0, A4toA4R, 0.0, A4toT, 0.0, A4toE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5toA5R, A5toT, A5toG, A5toE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A1RtoA2R, 0.0, 0.0, 0.0, A1RtoT, 0.0, A1RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A2RtoA3R, 0.0, 0.0, A2RtoT, 0.0, A2RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A3RtoA4R, 0.0, A3RtoT, 0.0, A3RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A4RtoA5R, A4RtoT, 0.0, A4RtoE],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, A5RtoT, A5RtoG, A5RtoE],
     [TtoA1, TtoA2, TtoA3, TtoA4, TtoA5, TtoA1R, TtoA2R, TtoA3R, TtoA4R, TtoA5R, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]


def mc_sample_path(P, ψ_0, sample_size):

    # set up
    P = np.asarray(P)
    X = np.empty(sample_size, dtype=int)

    # Convert each row of P into a cdf
    n = len(P)
    P_dist = [np.cumsum(P[i, :]) for i in range(n)]

    # draw initial state, defaulting to 0
    if ψ_0 is not None:
        X_0 = qe.random.draw(np.cumsum(ψ_0))
    else:
        X_0 = 0

    # simulate
    X[0] = X_0
    for t in range(sample_size - 1):
        X[t+1] = qe.random.draw(P_dist[X[t]])

    return X



X = mc_sample_path(P, ψ_0=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], sample_size=10)
print(X)
#print(np.mean(X == 0))