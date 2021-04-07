from Aluno import Aluno

a = Aluno(1)
# next = a.get_next_state()
list(a.gen)
states = a.history
time = a.nb_state
print(states)
print(time)
