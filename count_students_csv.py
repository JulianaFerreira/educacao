import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
#
# df = pd.read_csv("docs/df_survivability_bsi-bcc.csv")
# df = df.loc[df['CD_PERD_ADMIS'] < 2014]
# df_retidos = df.loc[df['RETIDO'] == True]
# print(df.nunique())
# print(df_retidos.nunique())


# df = pd.read_csv("docs/df_survival_att.csv")
# df = df.loc[df['NM_PROGR_FORM'] != 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO']
# df = df.loc[df['CD_PERD_ADMIS'] > 2015]
# df = df.loc[df['CD_PERD_ADMIS'] < 2019]
# print(df.nunique())

# df = pd.read_csv("docs/df_survival_att.csv")
# df = df.loc[df['NM_PROGR_FORM'] != 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO']
# df = df.loc[df['CD_PERD_ADMIS'] > 2009]
# df = df.loc[df['CD_PERD_ADMIS'] < 2014]
# print(df.nunique())

# df_evadidos = df[df['STATUS'] == 'EVADIDO']
# print(df_evadidos.nunique())
#
# df_graduados = df[df['STATUS'] == 'CONCLUIDO']
# print(df_graduados.nunique())

# df_f = df[df['NM_SEXO'] == 'F']
# print(df_f.nunique())
#
# df_m = df[df['NM_SEXO'] == 'M']
# print(df_m.nunique())

# df_branca = df[df['NM_COR_RACA'] == 'PARDA']
# print(df_branca.nunique())




df = pd.read_csv("docs/df_survival_att.csv")
df = df.loc[df['CD_PERD_ADMIS'] > 2009]
df = df.loc[df['CD_PERD_ADMIS'] < 2014]
df = df.loc[df['STATUS'] == 'EVADIDO']

df_agrarias = df.loc[df['NM_PROGR_FORM'] == 'AGRONOMIA']
df_computacao = df.loc[df['NM_PROGR_FORM'] == 'BACHARELADO EM CIÊNCIA DA COMPUTAÇÃO']
df_saude = df.loc[df['NM_PROGR_FORM'] == 'MEDICINA VETERINÁRIA']

# Boxplot
sns.set_theme(style="whitegrid")
data1 = {'Cursos': 'Agrárias', 'Tempo(semestres)': df_agrarias['DURACAO_VINCULO'].values}
df1 = pd.DataFrame(data1)
data2 = {'Cursos': 'Computação', 'Tempo(semestres)': df_computacao['DURACAO_VINCULO'].values}
df2 = pd.DataFrame(data2)
# data3 = {'Curso': 'Curso 3', 'Tempo(semestres)': time_evadido2}
# df3 = pd.DataFrame(data3)
data4 = {'Cursos': 'Saúde', 'Tempo(semestres)': df_saude['DURACAO_VINCULO'].values}
df4 = pd.DataFrame(data4)
#df = df1.append(df2).append(df3).append(df4)
df = df1.append(df2).append(df4)
ax = sns.boxplot(x='Cursos', y='Tempo(semestres)', color='grey', data=df)
plt.show()