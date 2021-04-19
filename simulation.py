from matplotlib import pyplot as plt
import numpy as np
from lifelines import KaplanMeierFitter
from Student import Student


def sobrevivencia(time, event_observed, label, color, title):
    kmf = KaplanMeierFitter()

    linestyles = ['-', '--', '-.', ':']
    for i in range(len(time)):
        kmf.fit(time[i], event_observed[i], label=label[i])
        # kmf.plot_survival_function(color=color[i])
        kmf.plot_survival_function(linestyle=linestyles[i], color = "black")

    plt.xlabel('Tempo')
    plt.ylabel('Probabilidade')
    plt.suptitle(f"Análise de Sobrevivência: {title}", fontsize=18)
    plt.title("IC de 95% para a Média", fontsize=10)
    plt.savefig(f"imgs/plot{title}.png")
    plt.show()
    # kmf.plot_cumulative_density(ci_show=False)
    # plt.show()


def prob_and_temp(state, x, tempo, quantAlunos):
    print(f"\nProbabilidade de ser {state}: {np.round(x / quantAlunos * 100, 1)} %")
    print(f"Tempo médio até ser {state}: {np.round(np.mean(tempo), 3)} anos")


def Simu(quantAlunos, matriz):
    e = 0
    g = 0
    r = 0
    t = 0
    # anos = 12  # ou a.nb_state dentro do for
    time = np.array([])
    tempo_ate_retido = []
    tempo_ate_trancado = []
    tempo_ate_evadido = []
    tempo_ate_graduado = []
    event_observedE = np.array([])
    event_observedG = np.array([])
    event_observedT = np.array([])
    event_observedR = np.array([])

    event_observedGTeste = []
    timeTeste = []

    for i in range(quantAlunos):
        a = Student(i, matriz)
        list(a.gen)
        arr = a.history
        anos = a.nb_state
        k = 0

        tempo = np.arange(0, anos, 1)
        time = np.concatenate((time, tempo))

        estados = np.zeros((anos,), dtype=int)
        if 'E' in arr:
            e += 1  # quantidade para probabilidade
            k = arr.index("E")
            tempo_ate_evadido.append(k)
            estados[k] = 1
        event_observedE = np.concatenate((event_observedE, estados))

        estados = np.zeros((anos,), dtype=int)
        if 'G' in arr:
            g += 1  # quantidade para probabilidade
            k = arr.index("G")
            tempo_ate_graduado.append(k)
            estados[k] = 1
            # Teste
            timeTeste.append(k)
            event_observedGTeste.append(1)
        event_observedG = np.concatenate((event_observedG, estados))

        # Trancado
        estados = np.zeros((anos,), dtype=int)
        i = 1
        while i < len(arr):
            if arr[i] == arr[i-1]:  # se estado igual ao estado anterior
                estados[i] = 1
            i += 1
        event_observedT = np.concatenate((event_observedT, estados))

        # Se ficou Trancado em algum dos estados
        i = 1
        while i < len(arr):
            if arr[i] == arr[i - 1]:  # se estado igual ao estado anterior
                t += 1
                tempo_ate_trancado.append(i)
                break
            i += 1

        # Retido
        estados = np.zeros((anos,), dtype=int)
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
                tempo_ate_retido.append(count)
                r += 1
                break
            count += 1

    prob_and_temp("Retido", r, tempo_ate_retido, quantAlunos)
    prob_and_temp("Trancado", t, tempo_ate_trancado, quantAlunos)
    prob_and_temp("Evadido", e, tempo_ate_evadido, quantAlunos)
    prob_and_temp("Graduado", g, tempo_ate_graduado, quantAlunos)

    # print(g)
    # print(tempo_ate_graduado)

    # return time, event_observedE, event_observedG, event_observedR, event_observedT
    return timeTeste, time, event_observedE, event_observedGTeste, event_observedR, event_observedT



quantAlunos = 1000


# # Simulação por Gênero
# print("\nFeminino")
# timeF, event_observedEF, event_observedGF, event_observedRF, event_observedTF = Simu(quantAlunos, 'matrix/matrixF.csv')
# print("\nMasculino - 25%")
# timeM, event_observedEM, event_observedGM, event_observedRM, event_observedTM = Simu(quantAlunos, 'matrix/matrixM.csv')
# # print("\nMasculino - 50%")
# # timeM50, event_observedEM50, event_observedGM50, event_observedRM50, event_observedTM50 = Simu(quantAlunos, 'matrix/matrixM50.csv')
#
# times = [timeF, timeM]
# eventsE = [event_observedEF, event_observedEM]
# eventsG = [event_observedGF, event_observedGM]
# eventsR = [event_observedRF, event_observedRM]
# eventsT = [event_observedTF, event_observedTM]
# colors = ["red", "blue"]
# labels = ["Feminino", "Masculino"]
#
# # times = [timeF, timeM, timeM50]
# # eventsE = [event_observedEF, event_observedEM, event_observedEM50]
# # eventsG = [event_observedGF, event_observedGM, event_observedGM50]
# # eventsR = [event_observedRF, event_observedRM, event_observedRM50]
# # eventsT = [event_observedTF, event_observedTM, event_observedTM50]
# # colors = ["red", "blue", "green"]
# # labels = ["Feminino", "Masculino - 25%", "Masculino - 50%"]
#
#
# sobrevivencia(times, eventsR, labels, colors, "Retenção")
# sobrevivencia(times, eventsT, labels, colors, "Trancado")
# sobrevivencia(times, eventsE, labels, colors, "Evasão")
# sobrevivencia(times, eventsG, labels, colors, "Graduação")


# Simulação Geral
# time, event_observedE, event_observedG, event_observedR, event_observedT = Simu(quantAlunos, 'matrix/matrixF.csv')
timeTeste, time, event_observedE, event_observedG, event_observedR, event_observedT = Simu(quantAlunos, 'matrix/matrixF.csv')

sobrevivencia([time], [event_observedE], ['Evadido'], ["red"], "Evasão")
sobrevivencia([timeTeste], [event_observedG], ['Graduado'], ["green"], "Graduação")
sobrevivencia([time], [event_observedR], ['Retido'], ["orange"], "Retenção")
sobrevivencia([time], [event_observedT], ['Trancado'], ["grey"], "Trancado")


