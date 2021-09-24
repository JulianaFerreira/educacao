import pandas as pd
import numpy as np

df = pd.read_csv("docs/df_survivability_bsi-bcc.csv")

# Corrigir a coluna de retidos - não precisa mais desse, correção é feita no modelo
# df.loc[((df['QTD_REPROVADO_ACUM'] - df['QTD_REPROVADO']) < df['QTD_DISCIPLINAS_PERIODO']) & (df['QTD_TRANCAMENTOS_ACUM'] < 1), 'RETIDO'] = False

# Corrigir a coluna periodo curso
df['PERIODO_CURSO'] = 1 + (np.minimum((df.DURACAO_CURSO - 1),
                                       np.round((df['QTD_APROVADO_ACUM'] - df['QTD_APROVADO'])/df['QTD_DISCIPLINAS_PERIODO'])))


df.to_csv("docs/df_survivability_bsi-bcc_corrigido.csv")


test = 1 + (np.minimum(8, np.round((10-4)/5.333333)))

