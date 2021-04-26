from lifelines.statistics import logrank_test
from matplotlib import pyplot as plt
import numpy as np
from lifelines import KaplanMeierFitter
from Student import Student


def sobrevivencia(time, event_observed, label, title):
    kmf = KaplanMeierFitter()

    linestyles = ['-', '--', ':', '-.']
    for i in range(len(time)):
        kmf.fit(time[i], event_observed[i], label=label[i])
        # kmf.plot_survival_function(color=color[i])
        kmf.plot_survival_function(linestyle=linestyles[i], color="black")
        kmf.event_table.to_csv(f"docs/event_table{i}.csv")


    plt.xlabel('Tempo (em anos)')
    plt.ylabel('Probabilidade de graduação')
    plt.suptitle(f"{title}", fontsize=18)
    plt.title("IC de 95% para a Média", fontsize=10)
    plt.savefig(f"imgs/plot{title}.png")
    plt.show()
    # kmf.plot_cumulative_density(ci_show=False)
    # plt.show()



def prob_and_temp(state, x, tempo, quantAlunos):
    archive = open("docs/prob_and_temp.txt", "a")
    archive.write(f"Probabilidade de ser {state}: {np.round(x / quantAlunos * 100, 1)} %" + "\n")
    archive.write(f"Tempo médio até ser {state}: {np.round(np.mean(tempo), 3)} anos" + "\n")
    print(f"\nProbabilidade de ser {state}: {np.round(x / quantAlunos * 100, 1)} %")
    print(f"Tempo médio até ser {state}: {np.round(np.mean(tempo), 3)} anos")


def Simu(quantAlunos, matriz):
    e = 0
    g = 0
    r = 0
    t = 0
    time = []
    event = []
    tempo_ate_retido = []
    tempo_ate_trancado = []
    tempo_ate_evadido = []
    tempo_ate_graduado = []


    for i in range(quantAlunos):
        a = Student(i, matriz)
        list(a.gen)
        arr = a.history
        anos = a.size

        if arr[anos-1] == 'E':  # evadido
            e += 1
            tempo_ate_evadido.append(len(arr) - 1)
            time.append(len(arr) - 1)
            event.append(1)
        else:  # graduado
            g += 1
            tempo_ate_graduado.append(len(arr) - 1)
            time.append(len(arr) - 1)
            event.append(0)

        # Se ficou Trancado em algum dos estados
        i = 1
        while i < len(arr):
            if arr[i] == arr[i - 1]:  # se estado igual ao estado anterior
                t += 1
                tempo_ate_trancado.append(i)
                break
            i += 1

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

    return time, event



quantAlunos = 10000


# Simulação por Gênero
# print("\nFeminino")
# timeF, event_observedEF = Simu(quantAlunos, 'matrix/matrixF.csv')
# print("\nMasculino - 25%")
# timeM,  event_observedEM = Simu(quantAlunos, 'matrix/matrixM.csv')
# print("\nMasculino - 50%")
# timeM50, event_observedEM50 = Simu(quantAlunos, 'matrix/matrixM50.csv')
#
# times = [timeF, timeM, timeM50]
# events = [event_observedEF, event_observedEM, event_observedEM50]
# labels = ["Feminino", "Masculino - 25%", "Masculino - 50%"]
#
# sobrevivencia(times, events, labels, "Evasão")


# Simulação Trancamento
# time, event = Simu(quantAlunos, 'matrix/matrixPadrao.csv')
# time20, event_observed_20 = Simu(quantAlunos, 'matrix/matrixTrancamentoMenos20.csv')
# time40, event_observed_40 = Simu(quantAlunos, 'matrix/matrixTrancamentoMenos40.csv')
# time60, event_observed_60 = Simu(quantAlunos, 'matrix/matrixTrancamentoMenos60.csv')
#
# times = [time, time20, time40, time60]
# events = [event, event_observed_20, event_observed_40, event_observed_60]
# labels = ["Padrão", "20% menor", "40% menor", "60% menor"]
#
# sobrevivencia(times, events, labels, "Taxa de Trancamento")
#
#
# print("logrank")
# results = logrank_test(time, time20, event, event_observed_20)
# results.print_summary()
# print(results.p_value)
#
# results = logrank_test(time, time40, event, event_observed_40)
# results.print_summary()
# print(results.p_value)
#
# results = logrank_test(time, time60, event, event_observed_60)
# results.print_summary()
# print(results.p_value)


# Simulação Retenção
# time, event = Simu(quantAlunos, 'matrix/matrixPadrao.csv')
# time20, event_observed_20 = Simu(quantAlunos, 'matrix/matrixRetencaoMenos20.csv')
# time40, event_observed_40 = Simu(quantAlunos, 'matrix/matrixRetencaoMenos40.csv')
# time60, event_observed_60 = Simu(quantAlunos, 'matrix/matrixRetencaoMenos60.csv')
#
# times = [time, time20, time40, time60]
# events = [event, event_observed_20, event_observed_40, event_observed_60]
# labels = ["Padrão", "20% menor", "40% menor", "60% menor"]
#
# sobrevivencia(times, events, labels, "Taxa de Retenção")
#
#
# print("logrank")
# results = logrank_test(time, time20, event, event_observed_20)
# results.print_summary()
# print(results.p_value)
#
# results = logrank_test(time, time40, event, event_observed_40)
# results.print_summary()
# print(results.p_value)
#
# results = logrank_test(time, time60, event, event_observed_60)
# results.print_summary()
# print(results.p_value)




# Simulação Evasão A1
time, event = Simu(quantAlunos, 'matrix/matrixPadrao.csv')
time20, event_observed_20 = Simu(quantAlunos, 'matrix/matrixMenos20EvasaoA1.csv')
time40, event_observed_40 = Simu(quantAlunos, 'matrix/matrixMenos40EvasaoA1.csv')
time60, event_observed_60 = Simu(quantAlunos, 'matrix/matrixMenos60EvasaoA1.csv')


times = [time, time20, time40, time60]
events = [event, event_observed_20, event_observed_40, event_observed_60]
labels = ["Padrão", "20% menor", "40% menor", "60% menor"]

sobrevivencia(times, events, labels, "Taxa de Evasão")


print("logrank")
results = logrank_test(time, time20, event, event_observed_20)
results.print_summary()
print(results.p_value)

results = logrank_test(time, time40, event, event_observed_40)
results.print_summary()
print(results.p_value)

results = logrank_test(time, time60, event, event_observed_60)
results.print_summary()
print(results.p_value)



# Simulação Evasão A1 e A2
# time, event = Simu(quantAlunos, 'matrix/matrixPadrao.csv')
# time20, event_observed_20 = Simu(quantAlunos, 'matrix/matrixMenos20EvasaoA2.csv')
# time40, event_observed_40 = Simu(quantAlunos, 'matrix/matrixMenos40EvasaoA2.csv')
# time60, event_observed_60 = Simu(quantAlunos, 'matrix/matrixMenos60EvasaoA2.csv')
#
#
# times = [time, time20, time40, time60]
# events = [event, event_observed_20, event_observed_40, event_observed_60]
# labels = ["Padrão", "20% menor", "40% menor", "60% menor"]
#
# sobrevivencia(times, events, labels, "Taxa de Evasão")
#
#
# print("logrank")
# results = logrank_test(time, time20, event, event_observed_20)
# results.print_summary()
# print(results.p_value)
#
# results = logrank_test(time, time40, event, event_observed_40)
# results.print_summary()
# print(results.p_value)
#
# results = logrank_test(time, time60, event, event_observed_60)
# results.print_summary()
# print(results.p_value)



# Simulação Geral
# time, event = Simu(quantAlunos, 'matrix/matrixPadrao.csv')
#
# sobrevivencia([time], [event], ['Estudantes'], "Análise de Sobrevivência")





