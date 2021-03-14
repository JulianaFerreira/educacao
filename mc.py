import quantecon as qe
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
#%matplotlib inline

#['Y1', 'Y2', 'Y3', 'Y4', 'I', 'G', 'W']
P = [[0.057, 0.31, 0.0, 0.0, 0.603, 0.0, 0.03], [0.0, 0.187, 0.528, 0.0, 0.285, 0.0, 0.0],
     [0.0, 0.0, 0.012, 0.563, 0.097, 0.328, 0.0], [0.0, 0.0, 0.0, 0.039, 0.094, 0.814, 0.053],
     [0.001, 0.036, 0.02, 0.0, 0.0, 0.003, 0.94], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

# def mc_sample_path(P, initial=None, sample_size=1000):
#
#     # set up
#     P = np.asarray(P)
#     X = np.empty(sample_size, dtype=int)
#
#     # Convert each row of P into a cummulative distribution
#     n = len(P)
#     P_dist = [np.cumsum(P[i, :]) for i in range(n)]
#
#     # draw initial state, defaulting to 0
#     if initial is not None:
#         X_0 = qe.random.draw(np.cumsum(initial))
#     else:
#         X_0 = 0
#
#     # simulate
#     X[0] = X_0
#     for t in range(sample_size - 1):
#         X[t+1] = qe.random.draw(P_dist[X[t]])
#
#     return X
#
# X = mc_sample_path(P, initial=[1, 0, 0, 0, 0, 0, 0], sample_size=1000)
# print(np.mean(X == 5))


# mc = qe.MarkovChain(P)
# X = mc.simulate(ts_length=1000000)
# print(np.mean(X == 5))


# mc = qe.MarkovChain(P, state_values=('Y1', 'Y2', 'Y3', 'Y4', 'I', 'G', 'W'))
# print(mc.simulate(ts_length=5, init='Y1'))

mc = qe.MarkovChain(P)
print(mc.stationary_distributions)