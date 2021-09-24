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

# Cria matriz de transição passando um array com os estados transicionando
def transition_matrix(transitions):
    n = 1 + max(transitions)  # numero de estados

    M = [[0] * n for _ in range(n)]

    # conta quantos em cada estado
    for (i, j) in zip(transitions, transitions[1:]):
        M[i][j] += 1

    print(M)

    # Conta para estudantes que ainda não evadiram ou graduaram -  não apague!
    for i in range(len(M)):
        for j in range(len(M)):
            if j == 0:
                M[i][j] = 0

    # converte para probabilidades:
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f / s for f in row]

    return M

def apagar_reintegrados(df):
    erros = [200610330, 200632094, 200632584, 200659979, 200678895, 200626145, 200632598, 200632612, 200650641,
             200650658, 200659166, 200664331, 200695510]

    for i in range(len(erros)):
        df = df[df['NU_MATR_CURSO'] != erros[i]]

    return df

# def apagar_reintegrados(df):
#     erros = []
#
#     count = 1
#     for i in range(len(df)):
#         if count == df.iloc[i].DURACAO_VINCULO_x:
#             count = count + 1
#         else:
#             if df.iloc[i-1].STATUS_x == 'EVADIDO' or df.iloc[i-1].STATUS_x == 'CONCLUIDO':
#                 count = 2
#             else:
#                 count = 1
#                 item = df.iloc[i].NU_MATR_CURSO
#                 if not item in erros:
#                     erros.append(item)
#
#     for i in range(len(erros)):
#         df = df[df['NU_MATR_CURSO'] != erros[i]]
#
#     return df


def evade_ou_conclu(df):
    df_evadidos = df[df['STATUS'] == 'EVADIDO']
    df_graduados = df[df['STATUS'] == 'CONCLUIDO']
    df_desvinculados = pd.concat([df_evadidos, df_graduados])
    df_result = df.merge(df_desvinculados, on="NU_MATR_CURSO")

    return df_result


def gerar_csv_matriz_probab(dados):
    df = pd.read_csv(dados)

    # Não precisa mais dessa parte
    # # Corrigir a coluna de retidos
    # df.loc[((df['QTD_REPROVADO_ACUM'] - df['QTD_REPROVADO']) < df['QTD_DISCIPLINAS_PERIODO']) & (
    #         df['QTD_TRANCAMENTOS_ACUM'] < 1), 'RETIDO'] = False
    #
    # # Corrigir retidos trancados no primeiro periodo
    # df.loc[df['DURACAO_VINCULO'] == 1, 'RETIDO'] = False

    # Se quise fazer apenas com estudantes que já evadiram ou concluiram
    # df = evade_ou_conclu(df)

    df = apagar_reintegrados(df)

    return df


def altera_duracao_estados(df):
    # Começa pelo 0 para criar matriz
    df['DURACAO_VINCULO'] = df['DURACAO_VINCULO'] - 1

    # Altera DURACAO_VINCULO conforme status e retido
    df.loc[df['RETIDO'] == True, 'DURACAO_VINCULO'] = df['DURACAO_VINCULO'] + 22
    df.loc[df['STATUS'] == 'EVADIDO', 'DURACAO_VINCULO'] = 44
    df.loc[df['STATUS'] == 'CONCLUIDO', 'DURACAO_VINCULO'] = 45

    return df

def alterar_prob_evasao(p):
    evasao = []
    evasaoR = []

    # pega e altera para 50% valor de E nos primeiros 4 períodos
    for i in range(4):
        evasao.append(p[i][len(p) - 2] / 2)

    for i in range(22, 26):
        evasaoR.append(p[i][len(p) - 2] / 2)

    # coloca novo valor alterado
    for i in range(4):
        p[i][len(p) - 2] = evasao[i]

    for i in range(22, 26):
        p[i][len(p) - 2] = evasaoR[i - 22]

    for i in range(len(p)-1):
        for j in range(len(p)-1):
            if i < 4:
                if j == i + 1:
                    p[i][j] = p[i][j] + evasao[i] / 2
                    p[i][j + 22] = p[i][j + 22] + evasao[i] / 2
            elif i > 21 and i < 26:
                if j == i + 1:
                    p[i][j] = p[i][j] + evasaoR[i-22]

    return p


def alterar_prob_retencao(p):
    retencao = []

    # pegar e alterar valor da retenção em 50% até o período 4
    for i in range(4):
        for j in range(len(p)-1):
            if j == i + 1:
                retencao.append(p[i][j+22]/2)
                p[i][j+22] = retencao[i]
                p[i][j] = p[i][j] + retencao[i]

    return p


df = gerar_csv_matriz_probab("docs/df_survivability_bsi-bcc.csv")

df = altera_duracao_estados(df)

# Ano
df = df.loc[df['CD_PERD_ADMIS'] < 2014]

# # Sexo
# df = df[df['NM_SEXO'] == 'F']
# df = df[df['NM_SEXO'] == 'M']
#
# # Cor
# df = df[df['NM_COR_RACA'] == 'BRANCA']
# df = df[df['NM_COR_RACA'] == 'PRETA']
# df = df[df['NM_COR_RACA'] == 'PARDA']
#
# # Curso
df = df[df['NM_PROGR_FORM'] == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO']
# df = df[df['NM_PROGR_FORM'] == 'BACHARELADO EM CIÊNCIA DA COMPUTAÇÃO']

# Com retido
states = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S21', 'S22',
          'S1R', 'S2R', 'S3R', 'S4R', 'S5R', 'S6R', 'S7R', 'S8R', 'S9R', 'S10R', 'S11R', 'S12R', 'S13R', 'S14R', 'S15R','S16R', 'S17R', 'S18R', 'S19R', 'S20R', 'S21R', 'S22R', 'E', 'G']

# Sem retido
# states = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S21', 'E', 'G']

t = df['DURACAO_VINCULO']
p = transition_matrix(t)
p[44] = np.zeros(46)
p[45] = np.zeros(46)

# Alterar probabilidades de Reter e Evadir
# p = alterar_prob_evasao(p)
# p = alterar_prob_retencao(p)

# p = np.round(p, 2)
# generate_csv_and_diagram("matrix/bsi-bcc-prob-evasao.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-prob-retencao.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-prob-evasao-retencao.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-sem-retencao.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-ate-2015-teste-aaa.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-20101.csv", states, p)
# generate_csv_and_diagram("matrix/bcc-2010.1.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-ate-2013-evasao-retencao.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-ate-2013.csv", states, p)
# generate_csv_and_diagram("matrix/bcc-ate-2013.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-ate-2013.csv", states, p)

# generate_csv_and_diagram("matrix/bsi-bcc-sexo-f.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-sexo-m.csv", states, p)
#
# generate_csv_and_diagram("matrix/bsi-bcc-cor-branca.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-cor-preta.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-cor-parda.csv", states, p)
#
# generate_csv_and_diagram("matrix/bsi-bcc-curso-bsi.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-curso-bcc.csv", states, p)
