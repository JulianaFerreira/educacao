import pandas as pd

states = ['A1', 'A2', 'A3', 'A4', 'A5', 'G', 'E']
n = [100, 90, 80, ]

#calcula o p
p = 0



q_df = pd.DataFrame(columns=states, index=states)
i = 0
for state in states:
    q_df.loc[state] = p[i]
    i += 1

q_df.to_csv("matrixtest.csv")

# Progressão dos alunos entre diferentes estados
print("\n Matriz de Transição:")
print(q_df)



#Transition probabilities matrix
p = pd.read_csv('matrix.csv', index_col=0)
print(p)

