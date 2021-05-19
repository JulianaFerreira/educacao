import pandas as pd
import numpy as np


# df = pd.read_csv("docs/df_survivability_bsi-bcc.csv")
# df.info()
#
# # duracao_vinculo por ano
# df['DURACAO_VINCULO'] = round((df['DURACAO_VINCULO']/2)+0.4)
# df.to_csv("docs/df_survivability_bsi-bcc-ano.csv")

df = pd.read_csv("docs/df_survivability_bsi-bcc-ano.csv")

# Para todos os estudantes
# df_todos = df.groupby(['DURACAO_VINCULO', 'STATUS'])['QTD'].sum()
# df_todos.to_csv("docs/df_survivability_bsi-bcc-ano_todos.csv")
df_todos = pd.read_csv("docs/df_survivability_bsi-bcc-ano_todos.csv")


def transition_matrix(M):
    #convert to probabilities:
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]
    return M


#criar tabela com as quantidades
def quantity_matrix(df, n):
    M = np.zeros((n,n))

    # Fazer array para e, c e v, para não dar problemas quando tiver valor 0
    # evadido adiciona na ultima coluna e linha do duracao_vinculo
    e = df[df['STATUS'] == 'EVADIDO']['QTD'].values
    M[:, n-1] = e

    # concluido adiciona na penultima coluna e linha do duracao_vinculo
    c = df[df['STATUS'] == 'CONCLUIDO']['QTD'].values
    print(c)
    #M[:, n-2] = c

    # vinculado adiciona coluna do duracao_vinculo
    v = df[df['STATUS'] == 'VINCULADO']['QTD'].values
    print(v)
    for i in range(n):
        for j in range(n):
            if j == i+1:
                M[i, j] = v[i]

    print(M)
    return M

m = quantity_matrix(df_todos, 11)
# p = transition_matrix(m)
# print(p)



#categorias


# df_sexo_f = df_ano[df_ano['NM_SEXO'] == 'F']
# df_sexo_m = df_ano[df_ano['NM_SEXO'] == 'M']
#
#
# df_esclr_pais_não_analfabetos = df_ano[df_ano['NM_ESCLR_MAE'] != 'ANALFABETO']
# df_esclr_pais_analfabetos = df_ano[df_ano['NM_ESCLR_MAE'] == 'ANALFABETO']











