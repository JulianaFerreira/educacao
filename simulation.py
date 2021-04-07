from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from pydtmc import MarkovChain, plot_graph, plot_walk
from lifelines import KaplanMeierFitter
from Student import Student


# def prob_absor(p, N):
#     # f=NR
#     x = np.array(p)
#     x1 = x[:len(x) - 2, len(x) - 2]
#     x2 = x[:len(x) - 2, len(x) - 1]
#     R = np.array([x1, x2])
#
#     return np.round(np.dot(R, N.T).T, 3)

# informacoes sobre a cadeia de markov
# print(mc)

# p = np.round(p, 4)
# matriz_transicao()
#
# stateHist = state
# mc = MarkovChain(p, statenames)
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
# # print("\n Duração média esperada até graduação:")
# # Sem estados retidos
# # print(np.round(np.trace(np.asarray(N)), 3))
# # Com estados retidos
# # print(np.round(np.trace((np.asarray(N) / 2)), 3))
#
# probGE = prob_absor(p, N)
# for i in range(len(probGE)):
#     print("\n Probabilidade graduação e evasão no estado " + statenames[i] + ":")
#     print(probGE[i])


def sobrevivencia(time, event_observed, label, color, title):
    kmf = KaplanMeierFitter()

    for i in range(len(time)):
        kmf.fit(time[i], event_observed[i], label=label[i])
        kmf.plot_survival_function(color=color[i])

    plt.xlabel('Tempo')
    plt.ylabel('Probabilidade')
    plt.suptitle(f"Análise de Sobrevivência: {title}", fontsize=18)
    plt.title("IC de 95% para a Média", fontsize=10)
    plt.savefig(f"imgs/plot{title}.png")
    plt.show()
    # kmf.plot_cumulative_density(ci_show=False)
    # plt.show()


def prob_and_temp(state, x, tempo, quantAlunos):
    print(f"\nProbabilidade de ser {state}: {np.round(x / quantAlunos * 100)} %")
    print(f"Tempo médio até ser {state}: {np.round(np.mean(tempo), 3)} anos")


def Simu(quantAlunos, matriz):
    e = 0
    g = 0
    r = 0
    t = 0
    time = np.array([])
    tempo_ate_retido = []
    tempo_ate_trancado = []
    tempo_ate_evadido = []
    tempo_ate_graduado = []
    event_observedE = np.array([])
    event_observedG = np.array([])
    event_observedT = np.array([])
    event_observedR = np.array([])

    for i in range(quantAlunos):
        a = Student(i, matriz)
        list(a.gen)
        arr = a.history

        tempo = np.arange(0, a.nb_state, 1)
        time = np.concatenate((time, tempo))

        estados = np.zeros((a.nb_state,), dtype=int)
        if 'E' in arr:
            e += 1  # quantidade para probabilidade
            k = arr.index("E")
            tempo_ate_evadido.append(k)
            estados[k] = 1
        event_observedE = np.concatenate((event_observedE, estados))

        estados = np.zeros((a.nb_state,), dtype=int)
        if 'G' in arr:
            g += 1  # quantidade para probabilidade
            k = arr.index("G")
            tempo_ate_graduado.append(k)
            estados[k] = 1
        event_observedG = np.concatenate((event_observedG, estados))

        # Trancado
        estados = np.zeros((a.nb_state,), dtype=int)
        count = 0
        for estado in arr:
            if estado == 'T' and count < a.nb_state - 1:
                estados[count] = 1
            count += 1
        event_observedT = np.concatenate((event_observedT, estados))

        if 'T' in arr:
            t += 1
            k = arr.index("T")
            tempo_ate_trancado.append(k)

        # Retido
        estados = np.zeros((a.nb_state,), dtype=int)
        count = 0
        for estado in arr:
            if 'R' in estado and count < a.nb_state - 1:
                estados[count] = 1
            count += 1
        event_observedR = np.concatenate((event_observedR, estados))

        # Se ficou Retido em algum dos estados
        count = 0
        for estado in arr:
            if 'R' in estado:
                tempo_ate_retido.append(count)
                r += 1
                break
            count += 1

    prob_and_temp("Retido", r, tempo_ate_retido, quantAlunos)
    prob_and_temp("Evadido", e, tempo_ate_evadido, quantAlunos)
    prob_and_temp("Graduado", g, tempo_ate_graduado, quantAlunos)
    # prob_and_temp("Trancado", t, tempo_ate_trancado, quantAlunos)


    return time, event_observedE, event_observedG, event_observedR, event_observedT



quantAlunos = 500


# Simulação por Gênero
print("\nFeminino")
timeF, event_observedEF, event_observedGF, event_observedRF, event_observedTF = Simu(quantAlunos, 'matrix/matrixF.csv')
print("\nMasculino")
timeM, event_observedEM, event_observedGM, event_observedRM, event_observedTM = Simu(quantAlunos, 'matrix/matrixM.csv')

times = [timeF, timeM]
eventsE = [event_observedEF, event_observedEM]
eventsG = [event_observedGF, event_observedGM]
eventsR = [event_observedRF, event_observedRM]
colors = ["red", "blue"]
labels = ["Feminino", "Masculino"]

sobrevivencia(times, eventsE, labels, colors, "Evasão")
sobrevivencia(times, eventsG, labels, colors, "Graduação")
sobrevivencia(times, eventsR, labels, colors, "Retenção")


# Simulação Geral
# time, event_observedE, event_observedG, event_observedR, event_observedT = Simu(quantAlunos, 'matrix/matrix.csv')
#
# sobrevivencia([time], [event_observedE], ['Evadido'], ["red"])
# sobrevivencia([time], [event_observedG], ['Graduado'], ["green"])
# sobrevivencia([time], [event_observedR], ['Retido'], ["orange"])
# sobrevivencia([time], [event_observedT], ['Trancado'], ["grey"])


