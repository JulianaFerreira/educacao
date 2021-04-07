from Student import Student

a = Student(1)
# next = a.get_next_state()
list(a.gen)
states = a.history
time = a.nb_state
print(states)
print(time)
