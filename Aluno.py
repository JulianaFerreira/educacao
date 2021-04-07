import numpy as np
import pandas as pd


class Aluno:

    def __init__(self, aluno_id, matrix):
        self.aluno_id = aluno_id
        self.df_Q = pd.read_csv(matrix, index_col=0)
        self.states = self.df_Q.columns
        self.state = self.states[0]
        self.nb_state = 1
        self.gen = self.markov()
        self.history = [self.states[0]]

    def get_next_state(self):
        return next(self.gen)

    def markov(self):

        while self.state != 'G' and self.state != 'E':

            # calculate the next state
            next_state = np.random.choice(self.states, 1, p=self.df_Q.loc[f'{self.state}'])[0]

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