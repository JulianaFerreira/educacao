import pandas as pd
from lifelines.statistics import logrank_test
from matplotlib import pyplot as plt
import numpy as np
from lifelines import KaplanMeierFitter
from scipy.stats import ttest_ind

from Student import Student


def sobrevivencia(time, event_observed, label, title):
    kmf = KaplanMeierFitter()

    color = ["red", "green", "blue"]
    linestyles = ['-.', ':', '--', '-']
    markers = ['x', '*', '^', 'o']

    for i in range(len(time)):
        kmf.fit(time[i], event_observed[i], label=label[i])
        # kmf.plot_survival_function(color=color[i])
        kmf.plot_survival_function(linestyle=linestyles[i], color="black", marker=markers[i], ci_show=True)
        # print(kmf.event_table)
        # kmf.event_table.to_csv(f"docs/event_table{title}.csv")

    plt.ylabel('Probabilidade')
    plt.yticks(np.arange(0, 1.1, step=0.1))
    plt.suptitle(f"{title}", fontsize=12)
    plt.title("IC de 95% para a Média", fontsize=10)

    # Corte pelo semestre no gráfico - BSI-BCC
    plt.xticks(range(0, 21))
    plt.xlim([-0.2, 20.2])
    # plt.xticks(range(0, 15))
    # plt.xlim([-0.2, 14.2])
    plt.xlabel('Tempo (semestres)')

    # Corte pelo semestre no gráfico - Boumi
    # plt.xticks(range(0, 10))
    # plt.xlim([-0.2, 9.2])
    # plt.xlabel('Tempo (anos)')

    plt.savefig(f"imgs/plot{title}.png")
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

def real_data():
    df = pd.read_csv("docs/df_survivability_bsi-bcc.csv")
    df = df.loc[df['CD_PERD_ADMIS'] < 2014]

    df = df.loc[df['NM_COR_RACA'] == 'PRETA']
    # df = df[df['NM_SEXO'] == 'F']
    # df = df[df['NM_PROGR_FORM'] == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO']
    # df = df[df['NM_PROGR_FORM'] == 'BACHARELADO EM CIÊNCIA DA COMPUTAÇÃO']

    df_evadidos = df.loc[df['STATUS'] == "EVADIDO"]
    df_evadidos['DURACAO_VINCULO'] = df_evadidos['DURACAO_VINCULO'] - 1
    tempo_evasao = df_evadidos["DURACAO_VINCULO"].values

    df_graduados = df.loc[df['STATUS'] == "CONCLUIDO"]
    df_graduados['DURACAO_VINCULO'] = df_graduados['DURACAO_VINCULO']
    tempo_conclusao = df_graduados["DURACAO_VINCULO"].values

    tempo_desvinculacao = np.concatenate((tempo_evasao, tempo_conclusao))

    evento_desvinculacao = np.ones(len(tempo_desvinculacao))
    evento_evasao = np.ones(len(tempo_evasao))
    evento_conclusao = np.ones(len(tempo_conclusao))

    return tempo_desvinculacao, tempo_evasao, tempo_conclusao, evento_desvinculacao, evento_evasao, evento_conclusao



def prob_and_temp(state, x, tempo, quantAlunos):
    # archive = open("docs/prob_and_temp.txt", "a")
    # archive.write(f"Probabilidade de ser {state}: {np.round(x / quantAlunos * 100, 1)} %" + "\n")
    # archive.write(f"Tempo médio até ser {state}: {np.round(np.mean(tempo), 3)} semestres" + "\n")
    print(f"\nProbabilidade de ser {state}: {np.round(x / quantAlunos * 100, 2)} %")
    print(f"Tempo médio até ser {state}: {np.round(np.mean(tempo), 3)} semestres")


def stacked_bar_plot(n, vinculados, graduados, evadidos):
    periodos = list(range(0, n))

    colors = ['darkgray', 'gray', 'dimgray', 'lightgray']
    plt.figure(figsize=(9, 7))
    plt.bar(periodos, graduados, color=colors[1], label="Concluídos")
    plt.bar(periodos, evadidos, color=colors[0], bottom=np.array(graduados), label="Evadidos")
    plt.bar(periodos, vinculados, color=colors[3], bottom=np.array(graduados) + np.array(evadidos), label="Vinculados")

    plt.xlabel('Tempo (semestres)')
    plt.ylabel('Probabilidade')
    plt.legend(loc="lower left", bbox_to_anchor=(0.8, 1.0))
    plt.xticks(range(0, n))
    plt.yticks(np.arange(0, 101, step=10))
    plt.show()


def quant_semester(quant_alunos, tempo_evadidos, tempo_graduados):
    n = 21
    quant_vinculados = np.zeros(n)
    quant_evadidos = np.zeros(n)
    quant_graduados = np.zeros(n)

    for i in range(len(tempo_evadidos)):
        tempo = tempo_evadidos[i]
        quant_evadidos[tempo] = quant_evadidos[tempo] + 1

    for i in range(len(tempo_graduados)):
        tempo = tempo_graduados[i]
        quant_graduados[tempo] = quant_graduados[tempo] + 1

    for i in range(n-1):
        quant_evadidos[i+1] = quant_evadidos[i+1] + quant_evadidos[i]

    for i in range(n-1):
        quant_graduados[i+1] = quant_graduados[i+1] + quant_graduados[i]

    for i in range(n):
        quant_vinculados[i] = quant_alunos - quant_graduados[i] - quant_evadidos[i]

    # Converte para probabilidades
    for i in range(n):
        quant_vinculados[i] = quant_vinculados[i]/quant_alunos * 100
        quant_evadidos[i] = quant_evadidos[i]/quant_alunos * 100
        quant_graduados[i] = quant_graduados[i]/quant_alunos * 100

    stacked_bar_plot(n, quant_vinculados, quant_graduados, quant_evadidos)



def Simu(quantAlunos, matriz):
    e = 0
    g = 0
    r = 0
    v = 0
    time = []
    time_evadido = []
    time_graduado = []
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
        # semestres - 1 na evasão pq conta apenas no inicio do semestre seguinte
        # graduação conta no final do semestre
        # retenção é no inicio do semestre seguinte por isso o count começa no 0
        # probabilidade de retenção está certa, já que não pode contar quem iria ficar retido no ano que evadiu
        # lembrar dessas informações quando for validar os dados!
        if arr[semestres-1] == 'E':  # evadido
            e += 1
            semestres = semestres - 1
            tempo_ate_evadido.append(semestres)
            time.append(semestres)
            time_evadido.append(semestres)
            event.append(1)
            event_evadido.append(1)
        elif arr[semestres-1] == 'G':  # graduado
            g += 1
            tempo_ate_graduado.append(semestres)
            time.append(semestres)
            time_graduado.append(semestres)
            event.append(1)
            event_graduado.append(1)
        else:  # ainda vinculado
            v += 1
            # event.append(0)
            # time.append(semestres)

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

    # quant_semester(quantAlunos, tempo_ate_evadido, tempo_ate_graduado)

    #return time, event, event_evadido, event_graduado
    return time, time_evadido, time_graduado, event, event_evadido, event_graduado


# Simulação Boumi
# time, time_evadido, time_graduado, event, event_evadido, event_graduado = Simu(10000, 'matrix/matrixBoumi1.csv')
# sobrevivencia([time_evadido, time_graduado, time], [event_evadido, event_graduado, event], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência")
#
# timeA, time_evadidoA, time_graduadoA, eventA, event_evadidoA, event_graduadoA = Simu(10000, 'matrix/matrixBoumiAlterado1.csv')
# sobrevivencia([time_evadidoA, time_graduadoA, timeA], [event_evadidoA, event_graduadoA, eventA], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência")
#
# times = [time, timeA]
# events = [event, eventA]
# labels = ["Boumi and Vela 2020", "Este estudo"]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação")
#
# times = [time_evadido, time_evadidoA]
# events = [event_evadido, event_evadidoA]
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão")
#
# times = [time_graduado, time_graduadoA]
# events = [event_graduado, event_graduadoA]
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Conclusão")
#
# results = logrank_test(time_graduado, time_graduadoA, event_graduado, event_graduadoA)
# results.print_summary()
# print("Graduado")
# print(results.p_value)
#
# results = logrank_test(time, timeA, event, eventA)
# results.print_summary()
# print("Desvinculado")
# print(results.p_value)
#
# results = logrank_test(time_evadido, time_evadidoA, event_evadido, event_evadidoA)
# results.print_summary()
# print("Evadido")
# print(results.p_value)


# Simulação BSI-BCC - Geral
# time, event, event_evadido, event_graduado = Simu(10000, 'matrix/bsi-bcc-ate-2013.csv')

# Com dados reais
time, time_evadido, time_graduado, event, event_evadido, event_graduado = real_data()

#time, time_evadido, time_graduado, event, event_evadido, event_graduado = Simu(20000, 'matrix/bsi-bcc-ate-2013.csv')
sobrevivencia([time_evadido, time_graduado, time], [event_evadido, event_graduado, event], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência")

time1, time_evadido1, time_graduado1, event1, event_evadido1, event_graduado1 = Simu(20000, 'matrix/corte_pareto_95/bsi-bcc-cor-preta.csv')
#time1, time_evadido1, time_graduado1, event1, event_evadido1, event_graduado1 = Simu(20000, 'matrix/corte_pareto_95/bsi-bcc-ate-2013.csv')
sobrevivencia([time_evadido1, time_graduado1, time1], [event_evadido1, event_graduado1, event1], ['evasão', 'conclusão','desvinculação'], "Análise de Sobrevivência")

times = [time, time1]
events = [event, event1]
labels = ["Dados", "Modelo"]

sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação")

times = [time_evadido, time_evadido1]
events = [event_evadido, event_evadido1]

sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão")

times = [time_graduado, time_graduado1]
events = [event_graduado, event_graduado1]

sobrevivencia(times, events, labels, "Análise de Sobrevivência da Conclusão")

# print("Desvinculação:")
# t, p = ttest_ind(time, time1)
# print(p)
#
# print("Evasão:")
# t, p = ttest_ind(time_evadido, time_evadido1)
# print(p)
#
# print("Conclusão:")
# t, p = ttest_ind(time_graduado, time_graduado1)
# print(p)


# Simulação BSI-BCC - Evasão
# time, time_evadido, time_graduado, event, event_evadido, event_graduado = Simu(10000, 'matrix/bsi-bcc-ate-2013.csv')
# sobrevivencia([time_evadido, time_graduado, time], [event_evadido, event_graduado, event], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência")
#
# time_taxa_evasao, time_evadido_taxa_evasao, time_graduado_taxa_evasao, event_taxa_evasao, event_evadido_taxa_evasao, event_graduado_taxa_evasao = Simu(10000, 'matrix/bsi-bcc-ate-2013-evasao.csv')
# sobrevivencia([time_evadido_taxa_evasao, time_graduado_taxa_evasao, time_taxa_evasao], [event_evadido_taxa_evasao, event_graduado_taxa_evasao, event_taxa_evasao], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência")
#
# times = [time, time_taxa_evasao]
# events = [event, event_taxa_evasao]
# labels = ["Referência", "50% menor"]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação")
#
# times = [time_evadido, time_evadido_taxa_evasao]
# events = [event_evadido, event_evadido_taxa_evasao]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão")
#
# times = [time_graduado, time_graduado_taxa_evasao]
# events = [event_graduado, event_graduado_taxa_evasao]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Conclusão")


# Simulação BSI-BCC - Retenção
# time, time_evadido, time_graduado, event, event_evadido, event_graduado = Simu(10000, 'matrix/bsi-bcc-ate-2013.csv')
# sobrevivencia([time_evadido, time_graduado, time], [event_evadido, event_graduado, event], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência")
#
# time_taxa_evasao, time_evadido_taxa_evasao, time_graduado_taxa_evasao, event_taxa_evasao, event_evadido_taxa_evasao, event_graduado_taxa_evasao = Simu(10000, 'matrix/bsi-bcc-ate-2013-retencao.csv')
# sobrevivencia([time_evadido_taxa_evasao, time_graduado_taxa_evasao, time_taxa_evasao], [event_evadido_taxa_evasao, event_graduado_taxa_evasao, event_taxa_evasao], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência")

# times = [time, time_taxa_evasao]
# events = [event, event_taxa_evasao]
# labels = ["Referência", "50% menor"]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação")
#
# events = [event_evadido, event_evadido_taxa_evasao]
# times = [time_evadido, time_evadido_taxa_evasao]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão")
#
# events = [event_graduado, event_graduado_taxa_evasao]
# times = [time_graduado, time_graduado_taxa_evasao]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Conclusão")


# Simulação BSI-BCC - Evasão e Retenção
# time, time_evadido, time_graduado, event, event_evadido, event_graduado = Simu(10000, 'matrix/bsi-bcc-ate-2013.csv')
# sobrevivencia([time_evadido, time_graduado, time], [event_evadido, event_graduado, event], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência")
#
# time_taxa_evasao, time_evadido_taxa_evasao, time_graduado_taxa_evasao, event_taxa_evasao, event_evadido_taxa_evasao, event_graduado_taxa_evasao = Simu(10000, 'matrix/bsi-bcc-ate-2013-evasao-retencao.csv')
# sobrevivencia([time_evadido_taxa_evasao, time_graduado_taxa_evasao, time_taxa_evasao], [event_evadido_taxa_evasao, event_graduado_taxa_evasao, event_taxa_evasao], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência")
#
# times = [time, time_taxa_evasao]
# events = [event, event_taxa_evasao]
# labels = ["Referência", "50% menor"]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação")
#
# events = [event_evadido, event_evadido_taxa_evasao]
# times = [time_evadido, time_evadido_taxa_evasao]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão")
#
# events = [event_graduado, event_graduado_taxa_evasao]
# times = [time_graduado, time_graduado_taxa_evasao]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Cnclusão")


# Simulação BSI-BCC - Sexo

# time_f, time_evadido_f, time_graduado_f, event_f, event_evadido_f, event_graduado_f = Simu(10000, 'matrix/corte_pareto_95/bsi-bcc-sexo-f.csv')
# sobrevivencia([time_evadido_f, time_graduado_f, time_f], [event_evadido_f, event_graduado_f, event_f], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência do Sexo Feminino")
#
# time_m, time_evadido_m, time_graduado_m, event_m, event_evadido_m, event_graduado_m = Simu(10000, 'matrix/corte_pareto_95/bsi-bcc-sexo-m.csv')
# sobrevivencia([time_evadido_m, time_graduado_m, time_m], [event_evadido_m, event_graduado_m, event_m], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência do Sexo Masculino")
#
# times = [time_f, time_m]
# events = [event_f, event_m]
# labels = ["Feminino", "Masculino"]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação para Sexo")
#
# times = [time_evadido_f, time_evadido_m]
# events = [event_evadido_f, event_evadido_m]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão para Sexo")
#
# times = [time_graduado_f, time_graduado_m]
# events = [event_graduado_f, event_graduado_m]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Conclusão para Sexo")
#
# print("Desvinculação:")
# t, p = ttest_ind(time_f, time_m)
# print(p)
#
# print("Evasão:")
# t, p = ttest_ind(time_evadido_f, time_evadido_m)
# print(p)
#
# print("Conclusão:")
# t, p = ttest_ind(time_graduado_f, time_graduado_m)
# print(p)



# Simulação BSI-BCC - Cor/Raça

# print("Branca")
# time_branca, time_evadido_branca, time_graduado_branca, event_branca, event_evadido_branca, event_graduado_branca = Simu(10000, 'matrix/corte_pareto_80/bsi-bcc-cor-branca.csv')
# sobrevivencia([time_evadido_branca, time_graduado_branca, time_branca], [event_evadido_branca, event_graduado_branca, event_branca], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência para Cor Branca")
#
# print("Preta")
# time_preta, time_evadido_preta, time_graduado_preta, event_preta, event_evadido_preta, event_graduado_preta = Simu(10000, 'matrix/corte_pareto_80/bsi-bcc-cor-preta.csv')
# sobrevivencia([time_evadido_preta, time_graduado_preta, time_preta], [event_evadido_preta, event_graduado_preta, event_preta], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência para Cor Preta")
#
# print("Parda")
# time_parda, time_evadido_parda, time_graduado_parda, event_parda, event_evadido_parda, event_graduado_parda = Simu(10000, 'matrix/corte_pareto_80/bsi-bcc-cor-parda.csv')
# sobrevivencia([time_evadido_parda, time_graduado_parda, time_parda], [event_evadido_parda, event_graduado_parda, event_parda], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência para Cor Parda")
#
#
# times = [time_branca, time_preta, time_parda]
# events = [event_branca, event_preta, event_parda]
# labels = ["Branca", "Preta", "Parda"]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação para Cor")
#
# times = [time_evadido_branca, time_evadido_preta, time_evadido_parda]
# events = [event_evadido_branca, event_evadido_preta, event_evadido_parda]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão para Cor")
#
# times = [time_graduado_branca, time_graduado_preta, time_graduado_parda]
# events = [event_graduado_branca, event_graduado_preta, event_graduado_parda]
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Conclusão para Cor")


# Simulação BSI-BCC - Curso

# time, time_evadido, time_graduado, event, event_evadido, event_graduado = Simu(10000, 'matrix/corte_pareto_95/bsi-ate-2013.csv')
# sobrevivencia([time_evadido, time_graduado, time], [event_evadido, event_graduado, event], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência - BSI")
#
# time1, time_evadido1, time_graduado1, event1, event_evadido1, event_graduado1 = Simu(10000, 'matrix/corte_pareto_95/bcc-ate-2013.csv')
# sobrevivencia([time_evadido1, time_graduado1, time1], [event_evadido1, event_graduado1, event1], ['evasão', 'conclusão', 'desvinculação'], "Análise de Sobrevivência - BCC")
#
# times = [time, time1]
# events = [event, event1]
# labels = ["BSI", "BCC"]
#
# print("Desvinculação:")
# t, p = ttest_ind(time, time1)
# print(p)
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Desvinculação para Categoria Curso")
#
# times = [time_evadido, time_evadido1]
# events = [event_evadido, event_evadido1]
#
# print("Evasão:")
# t, p = ttest_ind(time_evadido, time_evadido1)
# print(p)
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Evasão para Categoria Curso")
#
# times = [time_graduado, time_graduado1]
# events = [event_graduado, event_graduado1]
#
# print("Conclusão:")
# t, p = ttest_ind(time_graduado, time_graduado1)
# print(p)
#
# sobrevivencia(times, events, labels, "Análise de Sobrevivência da Conclusão para Categoria Curso")
