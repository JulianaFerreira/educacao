import quantecon as qe
import numpy as np

from Aluno import Aluno
statenames = ['A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'T', 'G', 'E']

# statenames = ['Inicio', 'A1', 'A2', 'A3', 'A4', 'Graduado', 'Evadido']
# state = np.array([[1, 0, 0, 0, 0, 0, 0]])
# p = [[0.0, 0.89, 0.09, 0.02, 0.0, 0.0, 0.0], [0.0, 0.17, 0.64, 0.06, 0.0, 0.0, 0.13],
#      [0.0, 0.0, 0.1, 0.75, 0.08, 0.0, 0.07], [0.0, 0.0, 0.0, 0.08, 0.84, 0.04, 0.04],
#      [0.0, 0.0, 0.0, 0.0, 0.37, 0.61, 0.02], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]
#
# mc = qe.MarkovChain(p, statenames)
# X = mc.simulate(ts_length=10, init='Inicio')
# print(X)
#print(np.mean(X == 'Inicio'))


#teste
for i in range(10):
    a = Aluno(1, statenames)
    list(a.gen)
    states = a.history
    print(states)
    #print(a.get_quant_trans())
