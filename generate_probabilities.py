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
def transition_matrix(transitions):
    n = 1 + max(transitions)  # numero de estados

    M = [[0] * n for _ in range(n)]

    # conta quantos em cada estado
    for (i, j) in zip(transitions, transitions[1:]):
        M[i][j] += 1

    print(M)

    # converte para probabilidades:
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f / s for f in row]

    return M


def apagar_reintegrados(df):
    erros = []

    count = 1
    for i in range(len(df)):
        if count == df.iloc[i].DURACAO_VINCULO_x:
            count = count + 1
        else:
            if df.iloc[i-1].STATUS_x == 'EVADIDO' or df.iloc[i-1].STATUS_x == 'CONCLUIDO':
                count = 2
            else:
                count = 1
                item = df.iloc[i].NU_MATR_CURSO
                if not item in erros:
                    erros.append(item)

    for i in range(len(erros)):
        df = df[df['NU_MATR_CURSO'] != erros[i]]

    return df


def evade_ou_conclu(df):
    df_evadidos = df[df['STATUS'] == 'EVADIDO']
    df_graduados = df[df['STATUS'] == 'CONCLUIDO']
    df_desvinculados = pd.concat([df_evadidos, df_graduados])
    df_result = df.merge(df_desvinculados, on="NU_MATR_CURSO")

    return df_result


def gerar_csv_matriz_probab(dados):
    df = pd.read_csv(dados)

    # Corrigir a coluna de retidos
    df.loc[((df['QTD_REPROVADO_ACUM'] - df['QTD_REPROVADO']) < df['QTD_DISCIPLINAS_PERIODO']) & (
            df['QTD_TRANCAMENTOS_ACUM'] < 1), 'RETIDO'] = False

    df = evade_ou_conclu(df)

    df = apagar_reintegrados(df)

    return df


def altera_duracao_estados(df):
    # Começa pelo 0 para criar matriz
    df['DURACAO_VINCULO_x'] = df['DURACAO_VINCULO_x'] - 1

    # Altera DURACAO_VINCULO conforme status e retido
    df.loc[df['RETIDO_x'] == True, 'DURACAO_VINCULO_x'] = df['DURACAO_VINCULO_x'] + 22
    df.loc[df['STATUS_x'] == 'EVADIDO', 'DURACAO_VINCULO_x'] = 44
    df.loc[df['STATUS_x'] == 'CONCLUIDO', 'DURACAO_VINCULO_x'] = 45

    return df


df = gerar_csv_matriz_probab("docs/df_survivability_bsi-bcc.csv")

df = altera_duracao_estados(df)

# Ano
df = df.loc[df['CD_PERD_ADMIS_x'] < 2015]

# # Sexo
# df = df[df['NM_SEXO_x'] == 'F']
# df = df[df['NM_SEXO_x'] == 'M']
#
# # Cor
# df = df[df['NM_COR_RACA_x'] == 'BRANCA']
# df = df[df['NM_COR_RACA_x'] == 'PRETA']
# df = df[df['NM_COR_RACA_x'] == 'PARDA']
#
# # Curso
# df = df[df['NM_PROGR_FORM_x'] == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO']
# df = df[df['NM_PROGR_FORM_x'] == 'BACHARELADO EM CIÊNCIA DA COMPUTAÇÃO']

# Com retido
states = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S21', 'S22',
          'S1R', 'S2R', 'S3R', 'S4R', 'S5R', 'S6R', 'S7R', 'S8R', 'S9R', 'S10R', 'S11R', 'S12R', 'S13R', 'S14R', 'S15R','S16R', 'S17R', 'S18R', 'S19R', 'S20R', 'S21R', 'S22R', 'E', 'G']

# Sem retido
# states = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S21', 'E', 'G']

t = df['DURACAO_VINCULO_x']
p = transition_matrix(t)
p[44] = np.zeros(46)
p[45] = np.zeros(46)

#TODO aqui
# Diminuir probabilidade de evadir e reter nos primeiros dois anos



# p = np.round(p, 2)
# generate_csv_and_diagram("matrix/bsi-bcc-prob-evasao.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-prob-retencao.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-sem-retencao.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-20091.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-ate-2015.csv", states, p)

# generate_csv_and_diagram("matrix/bsi-bcc-sexo-f.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-sexo-m.csv", states, p)
#
# generate_csv_and_diagram("matrix/bsi-bcc-cor-branca.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-cor-preta.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-cor-parda.csv", states, p)
#
# generate_csv_and_diagram("matrix/bsi-bcc-curso-bsi.csv", states, p)
# generate_csv_and_diagram("matrix/bsi-bcc-curso-bcc.csv", states, p)

