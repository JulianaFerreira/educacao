import pandas as pd
import numpy as np


df = pd.read_csv("docs/df_survivability_bsi-bcc.csv")

# alterar csv de período para ano
df_ano = df[df['NM_SEXO'] == 'F']
df_ano.to_csv("docs/df_survivability_bsi-bcc-ano.csv")



df_todos = df.groupby(['DURACAO_VINCULO', 'STATUS'])['QTD'].sum()
df_test = df.groupby(['DURACAO_VINCULO'])['QTD'].sum()

df_todos.to_csv("docs/df_survivability_bsi-bcc_todos.csv")





#categorias


# df_sexo_f = df_ano[df_ano['NM_SEXO'] == 'F']
# df_sexo_m = df_ano[df_ano['NM_SEXO'] == 'M']
#
#
# df_esclr_pais_não_analfabetos = df_ano[df_ano['NM_ESCLR_MAE'] != 'ANALFABETO']
# df_esclr_pais_analfabetos = df_ano[df_ano['NM_ESCLR_MAE'] == 'ANALFABETO']











# Cria matriz de transição passando um array com os estados transicionando
def transition_matrix(transitions):
    n = 1 + max(transitions) #number of states

    M = [[0]*n for _ in range(n)]

    for (i, j) in zip(transitions, transitions[1:]):
        M[i][j] += 1

    print(M)

    #now convert to probabilities:
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]
    return M



# estados transicionando
# t = [1,1,2,6,8,5,5,7,8,8,1,1,4,5,5,0,0,0,1,1,4,4,5,1,3,3,4,5,4,1,1]
# states = np.unique(t)
# p = transition_matrix(t)
# print(p)



