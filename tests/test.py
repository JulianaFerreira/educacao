import pandas as pd

#
df = pd.read_csv("docs/df_survivability_bsi-bcc-atualizado1.csv")


#df_survivability_final['PERIODO_CURSO'] = 1 + (np.minimum(df_survivability_final.DURACAO_CURSO,
#                                       np.round((df_survivability_final['QTD_APROVADO_ACUM'] - df['QTD_APROVADO'])/df_survivability_final['QTD_DISCIPLINAS_PERIODO'])))

import numpy as np

test = 1 + (np.minimum(8, np.round((10-4)/5.333333)))