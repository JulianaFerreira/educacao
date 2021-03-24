# Function that implements the Markov model
def getNewState(states, transitionMatrix, currentState):
    i = 0
    newState = ""
    for x in states:
        if currentState == x:
            newState = np.random.choice(states, replace=True, p=transitionMatrix[i])
        i+=1

    return newState