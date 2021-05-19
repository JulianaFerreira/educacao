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
    n = n + 2
    M = np.zeros((n, n))

    e = []
    c = []
    v = []

    # Fazer array para e, c e v, para não dar problemas quando tiver valor 0

    # adiciona quantidade de evadidos na tabela
    for i in range(1, n-1):
        x = df.loc[(df['DURACAO_VINCULO'] == i) & (df['STATUS'] == 'EVADIDO')]
        e.append(x.iloc[0]['QTD'])
    e.append(0)  # linha graduado
    e.append(0)  # linha evadido
    M[:, n-1] = e

    # concluido adiciona na penultima coluna e linha do duracao_vinculo
    # c = df[df['STATUS'] == 'CONCLUIDO']['QTD'].values
    # print(c)
    #M[:, n-2] = c

    # for i in range(1, n-1):
    #     y = df.loc[(df['DURACAO_VINCULO'] == i) & (df['STATUS'] == 'CONCLUIDO')]
    #     print(y)
    #     c.append(y.iloc[0]['QTD'])
    # c.append(0)  # linha graduado
    # c.append(0)  # linha evadido
    # M[:, n-2] = c

    # adiciona quantidade de vinculados na tabela
    for i in range(1, n-1):
        x = df.loc[(df['DURACAO_VINCULO'] == i) & (df['STATUS'] == 'VINCULADO')]
        v.append(x.iloc[0]['QTD'])
    v.append(0)  # linha graduado
    v.append(0)  # linha evadido
    for i in range(n):
        for j in range(n):
            if j == i + 1:
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











