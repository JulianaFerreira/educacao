import pandas as pd

df = pd.read_csv("docs/df_survivability_bsi-bcc.csv")
df = df.loc[df['CD_PERD_ADMIS'] < 2014]
print(df.nunique())

# df = pd.read_csv("docs/df_survival.csv")
# df = df.loc[df['CD_PERD_ADMIS'] > 2015]
# df = df.loc[df['CD_PERD_ADMIS'] < 2019]
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

