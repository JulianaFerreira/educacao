import pandas as pd

df = pd.read_csv("docs/df_survivability_bsi-bcc.csv")
df = df.loc[df['CD_PERD_ADMIS'] < 2014]
print(df.nunique())

# df_evadidos = df[df['STATUS'] == 'EVADIDO']
# print(df_evadidos.nunique())
#
# df_graduados = df[df['STATUS'] == 'CONCLUIDO']
# print(df_graduados.nunique())

