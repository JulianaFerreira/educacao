from Aluno import Aluno

statenames = ['A1', 'A2', 'A3', 'A4', 'A5', 'A1R', 'A2R', 'A3R', 'A4R', 'A5R', 'A6R', 'A7R', 'G', 'E']

#teste
# for i in range(10):
#     a = Aluno(i, statenames)
#     list(a.gen)
#     states = a.history
#     print(states)
    #print(a.get_quant_trans())

# for i in range(10):
#     a = Aluno(i, statenames)
#     #next = a.get_next_state()
#     list(a.gen)
#     states = a.history
#     print()

a = Aluno(1)
list(a.gen)
states = a.history
time = a.nb_state
print(states)
print(time)
