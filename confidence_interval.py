import pandas as pd
import scipy.stats
import numpy as np

prob_evadidos = []
prob_graduados = []
prob_retidos = []

periodos = [2009.1, 2009.2, 2010.1, 2010.2, 2011.1, 2011.2, 2012.1, 2012.2, 2013.1, 2013.2, 2014.1, 2014.2]

for i in range(len(periodos)):
    df = pd.read_csv("docs/df_survivability_bsi-bcc.csv")

    df = df.loc[df['CD_PERD_ADMIS'] == periodos[i]]

    df_evadidos = df.loc[df['STATUS'] == "EVADIDO"]
    df_graduados = df.loc[df['STATUS'] == "CONCLUIDO"]
    df_retidos = df.loc[df['RETIDO'] == True]

    quant_todos = len(df.NU_MATR_CURSO.unique())
    quant_evadidos = len(df_evadidos.NU_MATR_CURSO.unique())
    quant_graduados = len(df_graduados.NU_MATR_CURSO.unique())
    quant_retidos = len(df_retidos.NU_MATR_CURSO.unique())

    prob_evadir = quant_evadidos / quant_todos
    prob_evadidos.append(prob_evadir)
    prob_graduar = quant_graduados / quant_todos
    prob_graduados.append(prob_graduar)
    prob_reter = quant_retidos / quant_todos
    prob_retidos.append(prob_reter)


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


g1, g2, g3 = mean_confidence_interval(prob_graduados)
e1, e2, e3 = mean_confidence_interval(prob_evadidos)
r1, r2, r3 = mean_confidence_interval(prob_retidos)



