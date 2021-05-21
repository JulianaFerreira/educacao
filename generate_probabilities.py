import pandas as pd
import numpy as np
from markov_diagram import Diagram

# # Gera os CSVs

# CSV Principal
# df = pd.read_csv("docs/df_survivability_bsi-bcc.csv")
# df.info()

# CSV duracao_vinculo por ano
# df['DURACAO_VINCULO'] = round((df['DURACAO_VINCULO']/2)+0.4)
# df.to_csv("docs/df_survivability_bsi-bcc-ano.csv")

# CSV para todos os estudantes
# df = pd.read_csv("docs/df_survivability_bsi-bcc-ano.csv")
# df_todos = df.groupby(['DURACAO_VINCULO', 'STATUS'])['QTD'].sum()
# df_todos.to_csv("docs/df_survivability_bsi-bcc-ano-todos.csv")

# # Categorias

# Sexo
# df = pd.read_csv("docs/df_survivability_bsi-bcc-ano.csv")
# df_sexo_f = df[df['NM_SEXO'] == 'F']
# df_sexo_f = df_sexo_f.groupby(['DURACAO_VINCULO', 'STATUS'])['QTD'].sum()
# df_sexo_f.to_csv("docs/df_survivability_bsi-bcc-ano-sexo_f.csv")
#
# df_sexo_m = df[df['NM_SEXO'] == 'M']
# df_sexo_m = df_sexo_m.groupby(['DURACAO_VINCULO', 'STATUS'])['QTD'].sum()
# df_sexo_m.to_csv("docs/df_survivability_bsi-bcc-ano-sexo_m.csv")

# Escolaridade Pais
# df = pd.read_csv("docs/df_survivability_bsi-bcc-ano.csv")
# df_esclr_pais_nao_analfabetos = df[df['NM_ESCLR_MAE'] != 'ANALFABETO']
# df_esclr_pais_nao_analfabetos = df_esclr_pais_nao_analfabetos.groupby(['DURACAO_VINCULO', 'STATUS'])['QTD'].sum()
# df_esclr_pais_nao_analfabetos.to_csv("docs/df_survivability_bsi-bcc-ano-esclr_pais_nao_analfabetos.csv")
#
# df_esclr_pais_analfabetos = df[df['NM_ESCLR_MAE'] == 'ANALFABETO']
# df_esclr_pais_alfabetos = df_esclr_pais_analfabetos.groupby(['DURACAO_VINCULO', 'STATUS'])['QTD'].sum()
# df_esclr_pais_analfabetos.to_csv("docs/df_survivability_bsi-bcc-ano-esclr_pais_analfabetos.csv")

# Cor/Raça [AMARELA, BRANCA, PARDA, PRETA, INDIGENA, -] - desconsiderados indigenas e amarelos
# df = pd.read_csv("docs/df_survivability_bsi-bcc-ano.csv")
# df_cor_raca_amarela = df[df['NM_COR_RACA'] != 'AMARELA']
# df_cor_raca_amarela = df_cor_raca_amarela.groupby(['DURACAO_VINCULO', 'STATUS'])['QTD'].sum()
# df_cor_raca_amarela.to_csv("docs/df_survivability_bsi-bcc-ano-cor_raca_amarela.csv")
#
# df_cor_raca_branca = df[df['NM_COR_RACA'] != 'BRANCA']
# df_cor_raca_branca = df_cor_raca_branca.groupby(['DURACAO_VINCULO', 'STATUS'])['QTD'].sum()
# df_cor_raca_branca.to_csv("docs/df_survivability_bsi-bcc-ano-cor_raca_branca.csv")
#
# df_cor_raca_parda = df[df['NM_COR_RACA'] != 'PARDA']
# df_cor_raca_parda = df_cor_raca_parda.groupby(['DURACAO_VINCULO', 'STATUS'])['QTD'].sum()
# df_cor_raca_parda.to_csv("docs/df_survivability_bsi-bcc-ano-cor_raca_parda.csv")
#
# df_cor_raca_preta = df[df['NM_COR_RACA'] != 'PRETA']
# df_cor_raca_preta = df_cor_raca_preta.groupby(['DURACAO_VINCULO', 'STATUS'])['QTD'].sum()
# df_cor_raca_preta.to_csv("docs/df_survivability_bsi-bcc-ano-cor_raca_preta.csv")
#
# df_cor_raca_indigena = df[df['NM_COR_RACA'] != 'INDIGENA']
# df_cor_raca_indigena = df_cor_raca_indigena.groupby(['DURACAO_VINCULO', 'STATUS'])['QTD'].sum()
# df_cor_raca_indigena.to_csv("docs/df_survivability_bsi-bcc-ano-cor_raca_indigena.csv")
#
# df_cor_raca_ni = df[df['NM_COR_RACA'] != '-']
# df_cor_raca_ni = df_cor_raca_ni.groupby(['DURACAO_VINCULO', 'STATUS'])['QTD'].sum()
# df_cor_raca_ni.to_csv("docs/df_survivability_bsi-bcc-ano-cor_raca_ni.csv")



# Gerar csv com matriz de transicao e desenho da cadeia de markov
def generate_csv_and_diagram(arquivo, states, p):
    q_df = pd.DataFrame(columns=states, index=states)
    i = 0
    for state in states:
        q_df.loc[state] = p[i]
        i += 1

    q_df.to_csv(arquivo)

    # Desenha Cadeia de Markov
    d = Diagram(arquivo)
    d.make_markov_diagram()

def transition_matrix(P):
    #convert to probabilities:
    for row in P:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]
    return P


#criar tabela com as quantidades
def quantity_matrix(df, n):
    n = n + 2
    M = np.zeros((n, n))

    e = []
    c = []
    v = []

    # adiciona quantidade de evadidos na tabela
    for i in range(1, n-1):
        x = df.loc[(df['DURACAO_VINCULO'] == i) & (df['STATUS'] == 'EVADIDO')]
        if x.QTD.empty:
            e.append(0)
        else:
            e.append(x.iloc[0]['QTD'])
    e.append(0)  # linha graduado
    e.append(0)  # linha evadido
    M[:, n-1] = e

    # adiciona quantidade de vinculados na tabela
    for i in range(1, n-1):
        x = df.loc[(df['DURACAO_VINCULO'] == i) & (df['STATUS'] == 'CONCLUIDO')]
        if x.QTD.empty:
            c.append(0)
        else:
            c.append(x.iloc[0]['QTD'])
    c.append(0)  # linha graduado
    c.append(0)  # linha evadido
    M[:, n-2] = c

    # adiciona quantidade de vinculados na tabela
    for i in range(1, n-1):
        x = df.loc[(df['DURACAO_VINCULO'] == i) & (df['STATUS'] == 'VINCULADO')]
        if x.QTD.empty:
            v.append(0)
        else:
            v.append(x.iloc[0]['QTD'])
    v.append(0)  # linha graduado
    v.append(0)  # linha evadido
    for i in range(n):
        for j in range(n):
            if j == i + 1:
                M[i, j] = v[i]

    return M


# TODO Falta corrigir o valor do progresso entre anos
def aplicar_parametros(p, taxa_evasao):

    print(p)
    n = len(p)

    p.iloc[:, n-1] = p.iloc[:, n-1] * taxa_evasao

    print(p)

    return p

states = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'G', 'E']

# p = pd.read_csv("matrix/bsi-bcc.csv", index_col=0)
# taxa_evasao = 1.5
# new_p = aplicar_parametros(p, taxa_evasao)
# print(new_p)
# generate_csv_and_diagram("matrix/bsi-bcc.csv", states, new_p)


# Todos Estudantes
# df_todos = pd.read_csv("docs/df_survivability_bsi-bcc-ano-todos.csv")
# m = quantity_matrix(df_todos, 11)
# p = transition_matrix(m)
# # p = np.round(p, 4)
# generate_csv_and_diagram("matrix/bsi-bcc.csv", states, p)


# Categoria Sexo
# df_sexo_f = pd.read_csv("docs/df_survivability_bsi-bcc-ano-sexo_f.csv")
# m = quantity_matrix(df_sexo_f, 11)
# p = transition_matrix(m)
# generate_csv_and_diagram("matrix/bsi-bcc-sexo_f.csv", states, p)
#
# df_sexo_m = pd.read_csv("docs/df_survivability_bsi-bcc-ano-sexo_m.csv")
# m = quantity_matrix(df_sexo_m, 11)
# p = transition_matrix(m)
# generate_csv_and_diagram("matrix/bsi-bcc-sexo_m.csv", states, p)


# Categoria Escolaridade dos Pais
# df_esclr_pais_nao_analfabetos = pd.read_csv("docs/df_survivability_bsi-bcc-ano-esclr_pais_nao_analfabetos.csv")
# m = quantity_matrix(df_esclr_pais_nao_analfabetos, 11)
# p = transition_matrix(m)
# generate_csv_and_diagram("matrix/bsi-bcc-df_esclr_pais_nao_analf.csv", states, p)
#
# df_esclr_pais_analfabetos = pd.read_csv("docs/df_survivability_bsi-bcc-ano-esclr_pais_analfabetos.csv")
# m = quantity_matrix(df_esclr_pais_analfabetos, 11)
# p = transition_matrix(m)
# generate_csv_and_diagram("matrix/bsi-bcc-df_esclr_pais_analf.csv", states, p)


# Categoria Cor/Raça - desconsiderar indigena e amarela
# df_cor_raca_branca = pd.read_csv("docs/df_survivability_bsi-bcc-ano-cor_raca_branca.csv")
# m = quantity_matrix(df_cor_raca_branca, 11)
# p = transition_matrix(m)
# generate_csv_and_diagram("matrix/bsi-bcc-df_cor_raca_branca.csv", states, p)
#
# df_cor_raca_preta = pd.read_csv("docs/df_survivability_bsi-bcc-ano-cor_raca_preta.csv")
# m = quantity_matrix(df_cor_raca_preta, 11)
# p = transition_matrix(m)
# generate_csv_and_diagram("matrix/bsi-bcc-df_cor_raca_preta.csv", states, p)
#
# df_cor_raca_parda = pd.read_csv("docs/df_survivability_bsi-bcc-ano-cor_raca_parda.csv")
# m = quantity_matrix(df_cor_raca_parda, 11)
# p = transition_matrix(m)
# generate_csv_and_diagram("matrix/bsi-bcc-df_cor_raca_parda.csv", states, p)
#
# df_cor_raca_ni = pd.read_csv("docs/df_survivability_bsi-bcc-ano-cor_raca_ni.csv")
# m = quantity_matrix(df_cor_raca_ni, 11)
# p = transition_matrix(m)
# generate_csv_and_diagram("matrix/bsi-bcc-df_cor_raca_ni.csv", states, p)

