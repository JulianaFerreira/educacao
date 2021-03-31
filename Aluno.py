import numpy as np
import pandas as pd

#Transition probabilities matrix
df_Q = pd.read_csv('matrix.csv', index_col=0)

class Aluno:

    def __init__(self, aluno_id, states):
        self.aluno_id = aluno_id
        self.state = states[0]
        self.states = states
        self.nb_state = 1
        self.gen = self.markov()
        self.history = [states[0]]

    def __repr__(self):
        return f"Aluno número {self.aluno_id} no estado: {self.state}"

    def get_next_state(self):
        return next(self.gen)

    def get_quant_trans(self):
        return self.nb_state

    def get_history(self):
        return self.history

    def markov(self):

        while self.state != 'G' and self.state != 'E':

            # calculate the next state
            next_state = np.random.choice(self.states, 1, p=df_Q.loc[f'{self.state}'])[0]

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