import pandas as pd
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns

prob_evadidos = []
prob_graduados = []
prob_retidos = []
tempo_evasao = []
tempo_graduacao = []
tempo_retencao = []

dist_graduacao = []
dist_evasao = []
dist_retencao = []

periodos = [2009.1, 2009.2, 2010.1, 2010.2, 2011.1, 2011.2, 2012.1, 2012.2, 2013.1, 2013.2]

for i in range(len(periodos)):
    df = pd.read_csv("docs/df_survivability_bsi-bcc-atualizado1.csv")
    df = df.loc[df['CD_PERD_ADMIS'] == periodos[i]]

    # df_cor = df.loc[df['NM_COR_RACA'] == 'PRETA']

    df_evadidos = df.loc[df['STATUS'] == "EVADIDO"]
    df_graduados = df.loc[df['STATUS'] == "CONCLUIDO"]
    df_retidos = df[df['STATUS'] != "EVADIDO"]
    df_retidos = df_retidos.loc[df_retidos['RETIDO'] == True]

    quant_todos = len(df.NU_MATR_CURSO.unique())
    quant_evadidos = len(df_evadidos.NU_MATR_CURSO.unique())
    quant_graduados = len(df_graduados.NU_MATR_CURSO.unique())
    quant_retidos = len(df_retidos.NU_MATR_CURSO.unique())


    prob_evadir = quant_evadidos / quant_todos
    prob_evadidos.append(prob_evadir)

    tempo_evadidos = df_evadidos["DURACAO_VINCULO"].mean()
    tempo_evasao.append(tempo_evadidos)


    prob_graduar = quant_graduados / quant_todos
    prob_graduados.append(prob_graduar)

    tempo_graduados = df_graduados["DURACAO_VINCULO"].mean()
    tempo_graduacao.append(tempo_graduados)


    prob_reter = quant_retidos / quant_todos
    prob_retidos.append(prob_reter)

    df_retidos_tempo = df_retidos.drop_duplicates(subset=['NU_MATR_CURSO'])
    tempo_retidos = df_retidos_tempo["DURACAO_VINCULO"].mean()
    tempo_retencao.append(tempo_retidos)


df = pd.read_csv("docs/df_survivability_bsi-bcc-atualizado1.csv")
df = df.loc[df['CD_PERD_ADMIS'] < 2014]

df_retidos = df[df['STATUS'] != "EVADIDO"]
df_retidos = df_retidos.loc[df['RETIDO'] == True]
df_retidos_tempo = df_retidos.drop_duplicates(subset=['NU_MATR_CURSO'])
dist_retencao = df_retidos_tempo["DURACAO_VINCULO"]

df_evadidos = df.loc[df['STATUS'] == "EVADIDO"]
dist_evasao = df_evadidos["DURACAO_VINCULO"]

df_graduados = df.loc[df['STATUS'] == "CONCLUIDO"]
dist_graduacao = df_graduados["DURACAO_VINCULO"]

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


prob_g_mean, prob_g_min, prob_g_max = mean_confidence_interval(prob_graduados)
prob_e_mean, prob_e_min, prob_e_max = mean_confidence_interval(prob_evadidos)
prob_r_mean, prob_r_min, prob_r_max = mean_confidence_interval(prob_retidos)

tempo_g_mean, tempo_g_min, tempo_g_max = mean_confidence_interval(tempo_graduacao)
tempo_e_mean, tempo_e_min, tempo_e_max = mean_confidence_interval(tempo_evasao)
tempo_r_mean, tempo_r_min, tempo_r_max = mean_confidence_interval(tempo_retencao)

#x = [10,12,14,11,11]
x = [3,3,11,7,2,5,13,5,6,2]
tempo_x_mean, tempo_x_min, tempo_x_max = mean_confidence_interval(x)


# Fit a normal distribution to
# the data:
# mean and standard deviation
mu, std = norm.fit(dist_retencao)

# Plot the histogram
plt.hist(dist_retencao, bins=len(dist_retencao.unique()), density=True, alpha=0.6, color='b')
print(dist_retencao.unique())

# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)

plt.plot(x, p, 'k', linewidth=2)
title = "Distribuição da Retenção".format(mu, std)
plt.xticks(range(0, 22))
plt.title(title)

plt.show()




