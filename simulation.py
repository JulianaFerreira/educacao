import pandas as pd
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

    plt.xlabel('Tempo (semestres)')
    plt.ylabel('Probabilidade')
    plt.suptitle(f"{title}", fontsize=12)
    plt.xticks(range(0, 21))
    plt.yticks(np.arange(0, 1.1, step=0.1))
    # plt.title("IC de 95% para a Média", fontsize=10)
    plt.savefig(f"imgs/plot{title}.png")

    # Corte pelo semestre no gráfico
    plt.xlim(xmax=20.2)

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
    # archive = open("docs/prob_and_temp.txt", "a")
    # archive.write(f"Probabilidade de ser {state}: {np.round(x / quantAlunos * 100, 1)} %" + "\n")
    # archive.write(f"Tempo médio até ser {state}: {np.round(np.mean(tempo), 3)} semestres" + "\n")
    print(f"\nProbabilidade de ser {state}: {np.round(x / quantAlunos * 100, 1)} %")
    print(f"Tempo médio até ser {state}: {np.round(np.mean(tempo), 3)} semestres")


def Simu(quantAlunos, matriz):
    e = 0
    g = 0
    r = 0
    t = 0
    v = 0
    time = []
    event_evadido = []
    event_graduado = []
    event = []
    tempo_ate_retido = []
    tempo_ate_evadido = []
    tempo_ate_graduado = []
    tempo_A1 = []
    tempo_A2 = []
    tempo_A3 = []
    tempo_A4 = []
    tempo_A5 = []
    tempo_A6 = []

    for i in range(quantAlunos):
        a = Student(i, matriz)
        list(a.gen)  # gera a cadeia de markov
        arr = a.history
        semestres = a.size

        # Colocar o semestre de corte aqui ou na linha 31 para fazer pelo gráfico
        # if semestres > 20:
        #     semestres = 20

        ###### Regras de Tempo ########
        # Não esquecer que são quantos semestres passaram até chegar naquele estado (quanto tempo está no curso) e não o período atual do curso!
        # semestres - 1 na evasão pq conta no siga apenas no inicio do semestre seguinte
        # graduação conta no final do semestre, então considera o último semestre do aluno
        # retenção é no inicio do semestre seguinte por isso o count começa no 0
        # probabilidade de retenção está certa, já que não pode contar quem ficou retido no ano que evadiu
        # lembrar dessas informações quando for validar os dados!
        if arr[semestres-1] == 'E':  # evadido
            e += 1
            semestres = semestres - 1
            tempo_ate_evadido.append(semestres)
            time.append(semestres)
            event.append(1)
            event_graduado.append(0)
            event_evadido.append(1)
        elif arr[semestres-1] == 'G':  # graduado
            g += 1
            tempo_ate_graduado.append(semestres)
            time.append(semestres)
            event.append(1)
            event_graduado.append(1)
            event_evadido.append(0)
        else:  # ainda vinculado
            v += 1
            event.append(0)
            event_graduado.append(0)
            event_evadido.append(0)
            time.append(semestres)

        # Se ficou Retido em algum dos estados
        count = 0
        for estado in arr:
            if 'R' in estado:
                tempo_ate_retido.append(count)
                r += 1
                break
            count += 1

        # Tempo por ano
        tempo_A1.append(semestres)
        if semestres - 2 > 0:
            tempo_A2.append(semestres - 1)
        if semestres - 3 > 0:
            tempo_A3.append(semestres - 2)
        if semestres - 4 > 0:
            tempo_A4.append(semestres - 3)
        if semestres - 5 > 0:
            tempo_A5.append(semestres - 4)
        if semestres - 6 > 0:
            tempo_A6.append(semestres - 5)

    prob_and_temp("Retido", r, tempo_ate_retido, quantAlunos)
    prob_and_temp("Evadido", e, tempo_ate_evadido, quantAlunos)
    prob_and_temp("Graduado", g, tempo_ate_graduado, quantAlunos)
    prob_and_temp("Desvinculado", g+e, tempo_ate_graduado+tempo_ate_evadido, quantAlunos)

    print("\nTempos por Semestres")
    print(f"Tempo médio até ser desvinculado S1: {np.round(np.mean(tempo_A1), 3)} semestres")
    print(f"Tempo médio até ser desvinculado S2: {np.round(np.mean(tempo_A2), 3)} semestres")
    print(f"Tempo médio até ser desvinculado S3: {np.round(np.mean(tempo_A3), 3)} semestres")
    print(f"Tempo médio até ser desvinculado S4: {np.round(np.mean(tempo_A4), 3)} semestres")
    print(f"Tempo médio até ser desvinculado S5: {np.round(np.mean(tempo_A5), 3)} semestres")
    print(f"Tempo médio até ser desvinculado S6: {np.round(np.mean(tempo_A6), 3)} semestres")


    return time, event, event_evadido, event_graduado


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
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Graduação")
#
# results = logrank_test(time, timeA, event_graduado, event_graduadoA)
# results.print_summary()
# print("Graduado")
# print(results.p_value)
#
# results = logrank_test(time, timeA, event, eventA)
# results.print_summary()
# print("Desvinculado")
# print(results.p_value)
#
# results = logrank_test(time, timeA, event_evadido, event_evadidoA)
# results.print_summary()
# print("Evadido")
# print(results.p_value)


# Simulação Geral
# time, event, event_evadido, event_graduado = Simu(1000, 'matrix/bsi-bcc-2010.2.csv')
# time, event, event_evadido, event_graduado = Simu(10000, 'matrix/bsi-bcc-ate-2013.csv')
#
# sobrevivencia([time, time, time], [event_evadido, event_graduado, event], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência")


# Simulação BSI-BCC - Evasão
time, event, event_evadido, event_graduado = Simu(10000, 'matrix/bsi-bcc-ate-2013.csv')
sobrevivencia([time, time, time], [event_evadido, event_graduado, event], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência")

time_taxa_evasao, event_taxa_evasao, event_evadido_taxa_evasao, event_graduado_taxa_evasao = Simu(10000, 'matrix/bsi-bcc-ate-2013-evasao.csv')
sobrevivencia([time_taxa_evasao, time_taxa_evasao, time_taxa_evasao], [event_evadido_taxa_evasao, event_graduado_taxa_evasao, event_taxa_evasao], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência")

times = [time, time_taxa_evasao]
events = [event, event_taxa_evasao]
labels = ["Referência", "50% menor"]

sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação")

events = [event_evadido, event_evadido_taxa_evasao]

sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão")

events = [event_graduado, event_graduado_taxa_evasao]

sobrevivencia(times, events, labels, "Análise de Sobrevivência da Graduação")


# Simulação BSI-BCC - Retenção
# time, event, event_evadido, event_graduado = Simu(10000, 'matrix/bsi-bcc-ate-2013.csv')
# sobrevivencia([time, time, time], [event_evadido, event_graduado, event], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência")
#
# time_taxa_evasao, event_taxa_evasao, event_evadido_taxa_evasao, event_graduado_taxa_evasao = Simu(10000, 'matrix/bsi-bcc-ate-2013-retencao.csv')
# sobrevivencia([time_taxa_evasao, time_taxa_evasao, time_taxa_evasao], [event_evadido_taxa_evasao, event_graduado_taxa_evasao, event_taxa_evasao], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência")
#
# times = [time, time_taxa_evasao]
# events = [event, event_taxa_evasao]
# labels = ["Referência", "50% menor"]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação")
#
# events = [event_evadido, event_evadido_taxa_evasao]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão")
#
# events = [event_graduado, event_graduado_taxa_evasao]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Graduação")


# Simulação BSI-BCC - Evasão e Retenção
# time, event, event_evadido, event_graduado = Simu(10000, 'matrix/bsi-bcc-ate-2013.csv')
# sobrevivencia([time, time, time], [event_evadido, event_graduado, event], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência")
#
# time_taxa_evasao, event_taxa_evasao, event_evadido_taxa_evasao, event_graduado_taxa_evasao = Simu(10000, 'matrix/bsi-bcc-ate-2013-evasao-retencao.csv')
# sobrevivencia([time_taxa_evasao, time_taxa_evasao, time_taxa_evasao], [event_evadido_taxa_evasao, event_graduado_taxa_evasao, event_taxa_evasao], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência")
#
# times = [time, time_taxa_evasao]
# events = [event, event_taxa_evasao]
# labels = ["Referência", "50% menor"]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação")
#
# events = [event_evadido, event_evadido_taxa_evasao]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão")
#
# events = [event_graduado, event_graduado_taxa_evasao]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Graduação")


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

# time, event, event_evadido, event_graduado = Simu(10000, 'matrix/bsi-bcc-curso-bsi.csv')
# sobrevivencia([time, time, time], [event_evadido, event_graduado, event], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência - BSI")
#
# time_taxa_evasao, event_taxa_evasao, event_evadido_taxa_evasao, event_graduado_taxa_evasao = Simu(10000, 'matrix/bsi-bcc-curso-bcc.csv')
# sobrevivencia([time_taxa_evasao, time_taxa_evasao, time_taxa_evasao], [event_evadido_taxa_evasao, event_graduado_taxa_evasao, event_taxa_evasao], ['evasão', 'graduação', 'desvinculação'], "Análise de Sobrevivência - BCC")
#
# times = [time, time_taxa_evasao]
# events = [event, event_taxa_evasao]
# labels = ["BSI", "BCC"]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação para Categoria Curso")
#
# events = [event_evadido, event_evadido_taxa_evasao]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão para Categoria Curso")
#
# events = [event_graduado, event_graduado_taxa_evasao]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Graduação para Categoria Curso")
