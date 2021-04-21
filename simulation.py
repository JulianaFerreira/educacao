from matplotlib import pyplot as plt
import numpy as np
from lifelines import KaplanMeierFitter
from Student import Student


def sobrevivencia(time, event_observed, label, title):
    kmf = KaplanMeierFitter()

    linestyles = ['-', '--', '-.', ':']
    for i in range(len(time)):
        kmf.fit(time[i], event_observed[i], label=label[i])
        # kmf.plot_survival_function(color=color[i])
        kmf.plot_survival_function(linestyle=linestyles[i], color="black")

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
    time = []
    event_g = []
    event_e = []
    # anos = 12  # ou a.nb_state dentro do for
    times = np.array([])
    tempo_ate_retido = []
    tempo_ate_trancado = []
    tempo_ate_evadido = []
    tempo_ate_graduado = []
    event_observedT = np.array([])
    event_observedR = np.array([])


    for i in range(quantAlunos):
        a = Student(i, matriz)
        list(a.gen)
        arr = a.history
        anos = a.nb_state

        tempo = np.arange(0, anos, 1)
        times = np.concatenate((times, tempo))

        if 'E' in arr:
            e += 1  # quantidade para probabilidade
            tempo_ate_evadido.append(len(arr) - 1)
            time.append(len(arr) - 1)
            event_e.append(1)
        else:
            event_e.append(0)

        if 'G' in arr:
            g += 1  # quantidade para probabilidade
            tempo_ate_graduado.append(len(arr) - 1)
            time.append(len(arr) - 1)
            event_g.append(1)
        else:
            event_g.append(0)

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

    return time, times, event_e, event_g, event_observedR, event_observedT



quantAlunos = 1000


# # Simulação por Gênero
# print("\nFeminino")
# timeF, timesF, event_observedEF, event_observedGF, event_observedRF, event_observedTF = Simu(quantAlunos, 'matrix/matrixF.csv')
# print("\nMasculino - 25%")
# timeM, timesM, event_observedEM, event_observedGM, event_observedRM, event_observedTM = Simu(quantAlunos, 'matrix/matrixM.csv')
# print("\nMasculino - 50%")
# timeM50, timesM50, event_observedEM50, event_observedGM50, event_observedRM50, event_observedTM50 = Simu(quantAlunos, 'matrix/matrixM50.csv')
#
# times = [timeF, timeM, timeM50]
# eventsE = [event_observedEF, event_observedEM, event_observedEM50]
# eventsG = [event_observedGF, event_observedGM, event_observedGM50]
# labels = ["Feminino", "Masculino - 25%", "Masculino - 50%"]
#
# sobrevivencia(times, eventsE, labels, "Evasão")
# sobrevivencia(times, eventsG, labels, "Graduação")



# Simulação Evasão A1
# time20, times, event_observed_e20, event_observed_g20, event_observedR, event_observedT = Simu(quantAlunos, 'matrix/matrixMenos20EvasaoA1.csv')
# time40, times, event_observed_e40, event_observed_g40, event_observedR, event_observedT = Simu(quantAlunos, 'matrix/matrixMenos40EvasaoA1.csv')
# time60, times, event_observed_e60, event_observed_g60, event_observedR, event_observedT = Simu(quantAlunos, 'matrix/matrixMenos60EvasaoA1.csv')
#
#
# times = [time20, time40, time60]
# eventsE = [event_observed_e20, event_observed_e40, event_observed_e60]
# eventsG = [event_observed_g20, event_observed_g40, event_observed_g60]
# labels = ["Menos 20%", "Menos 40%", "Menos 60%"]
#
# sobrevivencia(times, eventsE, labels, "Evasão")
# sobrevivencia(times, eventsG, labels, "Graduação")



# Simulação Geral
# time, times, event_observedE, event_observedG, event_observedR, event_observedT = Simu(quantAlunos, 'matrix/matrixPadrao.csv')
#
# sobrevivencia([time], [event_observedE], ['Evadido'], "Evasão")
# sobrevivencia([time], [event_observedG], ['Graduado'], "Graduação")
# sobrevivencia([times], [event_observedR], ['Retido'], "Retenção")
# sobrevivencia([times], [event_observedT], ['Trancado'], "Trancado")




