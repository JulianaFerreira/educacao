import numpy as np
import pandas as pd

#Transition probabilities matrix
df_Q = pd.read_csv('matriz.csv', index_col=0)

#States of Markov chain
STATES = ['A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'G', 'E']


class Aluno:

    def __init__(self, aluno_id):
        self.aluno_id = aluno_id
        self.state = 'A1'
        self.nb_state = 1
        self.gen = self.markov()
        self.history = ['A1']

    def __repr__(self):
        return f"Aluno número {self.aluno_id} no estado: {self.state}"

    def get_next_state(self):
        return next(self.gen)

    def markov(self):

        while self.state != 'G' or self.state != 'E':

            # calculate the next state
            next_state = np.random.choice(STATES, 1, p=df_Q.loc[f'{self.state}'])[0]

            if next_state == 'G':
                self.state = 'G'
                self.history.append(self.state)
                self.nb_state += 1
                yield self.state

            elif next_state == 'E':
                self.state = 'E'
                self.history.append(self.state)
                self.nb_state += 1
                yield self.state

            else:
                self.state = next_state
                self.history.append(self.state)
                self.nb_state += 1
                yield self.state