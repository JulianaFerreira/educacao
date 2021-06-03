import pandas as pd
import numpy as np
from markov_diagram import Diagram


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


def aplicar_parametros(p, taxa_evasao):
    taxa_progresso = 2 - taxa_evasao

    n = len(p)

    new_value = p.iloc[:, n-1] * taxa_progresso
    p.iloc[:, n-1] = p.iloc[:, n-1] * taxa_evasao

    for i in range(n):
        for j in range(n):
            if j == i + 1:
                p.iloc[i, j] = p.iloc[i, j] - new_value[i]

    return p


# Cria matriz de transição passando um array com os estados transicionando
def transition_matrix_test(transitions):
    n = 1 + max(transitions)  # number of states

    M = [[0] * n for _ in range(n)]

    for (i, j) in zip(transitions, transitions[1:]):
        M[i][j] += 1

    print(M)

    # now convert to probabilities:
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f / s for f in row]

    return M



# # CSV Principal
df = pd.read_csv("docs/df_survivability_bsi-bcc.csv")
# # df.info()
#

# Usar alunos ingressantes apenas de ano e curso específico
df = df.loc[df['CD_PERD_ADMIS'] == 2009.1]
df = df.loc[df['NM_PROGR_FORM'] == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO']


# Usar apenas alunos evadidos e concluidos
# df_evadidos = df[df['STATUS'] == 'EVADIDO']
# df_graduados = df[df['STATUS'] == 'CONCLUIDO']
# df_desvinculados = pd.concat([df_evadidos, df_graduados])
# df_result = pd.merge(df, df_desvinculados, on="NU_MATR_CURSO")


# # # Pegar dados do csv para comparar
# # duracao_graduado = df_graduados['DURACAO_VINCULO'].mean()
# # duracao_evadido = df_evadidos['DURACAO_VINCULO'].mean()
# # retidos = df_desvinculados[df_desvinculados['RETIDO'] == True]


# Apagar aluno que evade no primeiro período
# df = df.drop(df['NU_MATR_CURSO' == 200695476].index)


# Apagar alunos reintegrados
# erros = []
#
# count = 1
# for i in range(len(df_result)):
#     if count == df_result.iloc[i].DURACAO_VINCULO_x:
#         count = count + 1
#     else:
#         if df_result.iloc[i-1].STATUS_x == 'EVADIDO' or df_result.iloc[i-1].STATUS_x == 'CONCLUIDO':
#             count = 2
#         else:
#             count = 1
#             item = df_result.iloc[i].NU_MATR_CURSO
#             if not item in erros:
#                 erros.append(item)
#
# for i in range(len(erros)):
#     df_result = df_result[df_result['NU_MATR_CURSO'] != erros[i]]


# df_result.to_csv("docs/df_survivability_bsi-bcc-20091.csv")
# df.to_csv("docs/df_survivability_bsi-bcc-20091.csv")


# TODO aqui
# Corrigir a coluna de retidos
# FL_SUSPENSO > 0 ou QTD_REPROVADO_ACUM - QTD_REPROVADO > 4


# Colocar periodo - 1
df['DURACAO_VINCULO'] = df['DURACAO_VINCULO'] - 1

# df = pd.read_csv("docs/df_survivability_bsi-bcc-selec.csv")
# df = pd.read_csv("docs/df_survivability_bsi-bcc-20091.csv")
#
# # Transforma DURACAO_VINCULO para um formato de estados com informação de retido, graduado e evadido
# df = df.drop_duplicates(subset=['NU_MATR_CURSO', 'DURACAO_VINCULO_x'], keep='last')
# df.loc[df['RETIDO_x'] == True, 'DURACAO_VINCULO_x'] = df['DURACAO_VINCULO_x'] + 10
df.loc[df['STATUS'] == 'EVADIDO', 'DURACAO_VINCULO'] = 21
df.loc[df['STATUS'] == 'CONCLUIDO', 'DURACAO_VINCULO'] = 22
#
df.to_csv("docs/df_survivability_bsi-bcc-estados-sem-retido.csv")
# df.to_csv("docs/df_survivability_bsi-bcc-estados.csv")


# Gera matriz de transição
# df = pd.read_csv("docs/df_survivability_bsi-bcc-ano-estados.csv")
# df = pd.read_csv("docs/df_survivability_bsi-bcc-ano-estados-sem-retido.csv")

# # Sexo
# df_sexo_f = df[df['NM_SEXO_x'] == 'F']
# df_sexo_m = df[df['NM_SEXO_x'] == 'M']
#
# # Cor
# df_cor_branca = df[df['NM_COR_RACA_x'] == 'BRANCA']
# df_cor_preta = df[df['NM_COR_RACA_x'] == 'PRETA']
# df_cor_parda = df[df['NM_COR_RACA_x'] == 'PARDA']
#
# # Curso
# df_curso_bsi = df[df['NM_PROGR_FORM_x'] == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO']
# df_curso_bcc = df[df['NM_PROGR_FORM_x'] == 'BACHARELADO EM CIÊNCIA DA COMPUTAÇÃO']

# states = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'A6R', 'A7R', 'A8R', 'A9R', 'A10R', 'E', 'G']
# states = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S1R', 'S2R', 'S3R', 'S4R', 'S5R', 'S6R', 'S7R', 'S8R', 'S9R', 'S10R', 'E', 'G']

# Sem retido
# states = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S21', 'E', 'G']

# t = df['DURACAO_VINCULO_x']
# p = transition_matrix_test(t)
# p[20] = np.zeros(22)
# p[21] = np.zeros(22)

# p = np.round(p, 2)
# generate_csv_and_diagram("matrix/bsi-bcc-completo.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-completo-evasao-menos-50-ano12.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-completo-retencao.csv", states, p)

# generate_csv_and_diagram("matrix/bsi-bcc-sexo-f.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-sexo-m.csv", states, p)
#
# generate_csv_and_diagram("matrix/bsi-bcc-cor-branca.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-cor-preta.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-cor-parda.csv", states, p)
#
# generate_csv_and_diagram("matrix/bsi-bcc-curso-bsi.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-curso-bcc.csv", states, p)
