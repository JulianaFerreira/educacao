from lifelines.statistics import logrank_test
from matplotlib import pyplot as plt
import numpy as np
from lifelines import KaplanMeierFitter
from Student import Student


def sobrevivencia(time, event_observed, label, title):
    kmf = KaplanMeierFitter()

    color = ["red", "green", "blue"]
    linestyles = ['-.', ':', '--', '-']
    markers = ['x', '*', '^', 'o']

    for i in range(len(time)):
        kmf.fit(time[i], event_observed[i], label=label[i])
        # kmf.plot_survival_function(color=color[i])
        kmf.plot_survival_function(linestyle=linestyles[i], color="black", marker=markers[i], ci_show=False)
        # kmf.event_table.to_csv(f"docs/event_table{title}.csv")

    plt.xlabel('Tempo (em anos)')
    plt.ylabel('Probabilidade')
    plt.suptitle(f"{title}", fontsize=12)
    # plt.title("IC de 95% para a Média", fontsize=10)
    # plt.savefig(f"imgs/plot{title}.png")
    plt.show()
    # kmf.plot_cumulative_density(ci_show=False)
    # plt.show()


# def sobrevivencia_densidade(time, event_observed, label, title):
#     kmf = KaplanMeierFitter()
#
#     linestyles = ['-', '--', ':', '-.']
#     for i in range(len(time)):
#         kmf.fit(time[i], event_observed[i], label=label[i])
#         # kmf.plot_survival_function(color=color[i])
#         kmf.plot_cumulative_density(linestyle=linestyles[i], color="black", ci_show=False)
#
#
#     plt.xlabel('Tempo (em anos)')
#     plt.ylabel('Probabilidade')
#     plt.suptitle(f"{title}", fontsize=18)
#     plt.savefig(f"imgs/plot{title}.png")
#     plt.show()



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
    event_evadido = []
    event_graduado = []
    event = []
    tempo_ate_retido = []
    tempo_ate_trancado = []
    tempo_ate_evadido = []
    tempo_ate_graduado = []
    tempo_A1 = []
    tempo_A2 = []
    tempo_A3 = []
    tempo_A4 = []

    for i in range(quantAlunos):
        a = Student(i, matriz)
        list(a.gen)  # não apagar!
        arr = a.history
        anos = a.size

        # Tempo por ano
        tempo_A1.append(anos)
        if anos-2 > 0:
            tempo_A2.append(anos-1)
        if anos-3 > 0:
            tempo_A3.append(anos-2)
        if anos-4 > 0:
            tempo_A4.append(anos-3)

        if arr[anos-1] == 'E':  # evadido
            e += 1
            tempo_ate_evadido.append(anos)
            time.append(anos-1)
            event.append(1)
            event_graduado.append(0)
            event_evadido.append(1)
        else:  # graduado
            g += 1
            tempo_ate_graduado.append(anos)
            time.append(anos-1)
            event.append(1)
            event_graduado.append(1)
            event_evadido.append(0)

        # Se ficou Trancado em algum dos estados
        # i = 1
        # while i < len(arr):
        #     if arr[i] == arr[i - 1]:  # se estado igual ao estado anterior
        #         t += 1
        #         tempo_ate_trancado.append(i)
        #         break
        #     i += 1

        # Se ficou Retido em algum dos estados
        count = 0
        for estado in arr:
            if 'R' in estado:
                tempo_ate_retido.append(count)
                r += 1
                break
            count += 1

    prob_and_temp("Retido", r, tempo_ate_retido, quantAlunos)
    # prob_and_temp("Trancado", t, tempo_ate_trancado, quantAlunos)
    prob_and_temp("Evadido", e, tempo_ate_evadido, quantAlunos)
    prob_and_temp("Graduado", g, tempo_ate_graduado, quantAlunos)
    prob_and_temp("Desvinculado", g+e, tempo_ate_graduado+tempo_ate_evadido, quantAlunos)

    print("\nTempos por ano")
    print(f"Tempo médio até ser desvinculado A1: {np.round(np.mean(tempo_A1), 3)} anos")
    print(f"Tempo médio até ser desvinculado A2: {np.round(np.mean(tempo_A2), 3)} anos")
    print(f"Tempo médio até ser desvinculado A3: {np.round(np.mean(tempo_A3), 3)} anos")
    print(f"Tempo médio até ser desvinculado A4: {np.round(np.mean(tempo_A4), 3)} anos")

    return time, event, event_evadido, event_graduado


quantAlunos = 10000


# Simulação Retenção
# time, event, event_evadido, event_graduado = Simu(quantAlunos, 'matrix/matrixPadrao.csv')
# time20, event_20, event_evadido20, event_graduado20 = Simu(quantAlunos, 'matrix/matrixRetencaoMenos20.csv')
# time40, event_40, event_evadido40, event_graduado40 = Simu(quantAlunos, 'matrix/matrixRetencaoMenos40.csv')
# time60, event_60, event_evadido60, event_graduado60 = Simu(quantAlunos, 'matrix/matrixRetencaoMenos60.csv')


# Simulação Evasão A1
# time, event, event_evadido, event_graduado = Simu(quantAlunos, 'matrix/matrixPadrao.csv')
# time20, event_20, event_evadido20, event_graduado20 = Simu(quantAlunos, 'matrix/matrixMenos20EvasaoA1.csv')
# time40, event_40, event_evadido40, event_graduado40 = Simu(quantAlunos, 'matrix/matrixMenos40EvasaoA1.csv')
# time60, event_60, event_evadido60, event_graduado60 = Simu(quantAlunos, 'matrix/matrixMenos60EvasaoA1.csv')


# Simulação Evasão A1 e A2
# time, event, event_evadido, event_graduado = Simu(quantAlunos, 'matrix/matrixPadrao.csv')
# time20, event_20, event_evadido20, event_graduado20 = Simu(quantAlunos, 'matrix/matrixMenos20EvasaoA2.csv')
# time40, event_40, event_evadido40, event_graduado40 = Simu(quantAlunos, 'matrix/matrixMenos40EvasaoA2.csv')
# time60, event_60, event_evadido60, event_graduado60 = Simu(quantAlunos, 'matrix/matrixMenos60EvasaoA2.csv')


# times = [time, time20, time40, time60]
# events = [event, event_20, event_40, event_60]
# labels = ["Padrão", "80%", "60%", "40%"]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência do Vínculo")
#
# events = [event_evadido, event_evadido20, event_evadido40, event_evadido60]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão")
#
# events = [event_graduado, event_graduado20, event_graduado40, event_graduado60]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Graduação")
#
# print("logrank")
# results = logrank_test(time, time20, event, event_20)
# results.print_summary()
# print(results.p_value)
#
# results = logrank_test(time, time40, event, event_40)
# results.print_summary()
# print(results.p_value)
#
# results = logrank_test(time, time60, event, event_60)
# results.print_summary()
# print(results.p_value)


# Simulação Boumi
# time, event, event_evadido, event_graduado = Simu(10000, 'matrix/matrixBoumi.csv')
# sobrevivencia([time, time, time], [event_evadido, event_graduado, event], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência")
#
# timeA, eventA, event_evadidoA, event_graduadoA = Simu(10000, 'matrix/matrixBoumiAlterado.csv')
# sobrevivencia([timeA, timeA, timeA], [event_evadidoA, event_graduadoA, eventA], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência")
#
# times = [time, timeA]
# events = [event, eventA]
# labels = ["Versão do Artigo Original", "Versão Adaptada"]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação")
#
# events = [event_evadido, event_evadidoA]
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão")
#
# events = [event_graduado, event_graduadoA]
# sobrevivencia(times, events, labels, "Análise de Sobrevivência do Graduação")
#
# print("Graduado")
# results = logrank_test(time, timeA, event_graduado, event_graduadoA)
# results.print_summary()
# print(results.p_value)
#
# print("Vinculado")
# results = logrank_test(time, timeA, event, eventA)
# results.print_summary()
# print(results.p_value)
#
# print("Evadido")
# results = logrank_test(time, timeA, event_evadido, event_evadidoA)
# results.print_summary()
# print(results.p_value)


# Simulação Geral
# time, event, event_evadido, event_graduado = Simu(quantAlunos, 'matrix/matrixPadrao.csv')
#
# sobrevivencia([time, time, time], [event_evadido, event_graduado, event], ['evasão', 'graduação', 'vínculo'], "Análise de Sobrevivência")
# sobrevivencia_densidade([time, time], [event_evadido, event_graduado], ['Evadido', 'Graduado'], "Teste")



# Simulação BSI-BCC
time, event, event_evadido, event_graduado = Simu(10000, 'matrix/bsi-bcc-completo.csv')

sobrevivencia([time, time, time], [event_evadido, event_graduado, event], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência")


# Simulação BSI-BCC - Sexo

# time_f, event_f, event_evadido_f, event_graduado_f = Simu(10000, 'matrix/bsi-bcc-sexo-f.csv')
# sobrevivencia([time_f, time_f, time_f], [event_evadido_f, event_graduado_f, event_f], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência do Sexo Feminino")
#
# time_m, event_m, event_evadido_m, event_graduado_m = Simu(10000, 'matrix/bsi-bcc-sexo-m.csv')
# sobrevivencia([time_m, time_m, time_m], [event_evadido_m, event_graduado_m, event_m], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência do Sexo Masculino")
#
# times = [time_f, time_m]
# events = [event_f, event_m]
# labels = ["Feminino", "Masculino"]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação para Sexo")
#
# events = [event_evadido_f, event_evadido_m]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão para Sexo")
#
# events = [event_graduado_f, event_graduado_m]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Graduação para Sexo")
#
# results = logrank_test(time_f, time_m, event_evadido_f, event_evadido_m)
# results.print_summary()
# print("\nEvasão")
# print(results.p_value)
#
# results = logrank_test(time_f, time_m, event_graduado_f, event_graduado_m)
# results.print_summary()
# print("\nGraduação")
# print(results.p_value)
#
# results = logrank_test(time_f, time_m, event_f, event_m)
# results.print_summary()
# print("\nDesvinculação")
# print(results.p_value)


# Simulação BSI-BCC - Cor/Raça

# print("Branca")
# time_branca, event_branca, event_evadido_branca, event_graduado_branca = Simu(10000, 'matrix/bsi-bcc-cor-branca.csv')
# sobrevivencia([time_branca, time_branca, time_branca], [event_evadido_branca, event_graduado_branca, event_branca], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência para Cor Branca")
#
# print("Preta")
# time_preta, event_preta, event_evadido_preta, event_graduado_preta = Simu(10000, 'matrix/bsi-bcc-cor-preta.csv')
# sobrevivencia([time_preta, time_preta, time_preta], [event_evadido_preta, event_graduado_preta, event_preta], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência para Cor Preta")
#
# print("Parda")
# time_parda, event_parda, event_evadido_parda, event_graduado_parda = Simu(10000, 'matrix/bsi-bcc-cor-parda.csv')
# sobrevivencia([time_parda, time_parda, time_parda], [event_evadido_parda, event_graduado_parda, event_parda], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência para Cor Parda")
#
#
# times = [time_branca, time_preta, time_parda]
# events = [event_branca, event_preta, event_parda]
# labels = ["Branca", "Preta", "Parda"]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação para Cor")
#
# events = [event_evadido_branca, event_evadido_preta, event_evadido_parda]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão para Cor")
#
# events = [event_graduado_branca, event_graduado_preta, event_graduado_parda]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Graduação para Cor")


# Simulação BSI-BCC - Curso
