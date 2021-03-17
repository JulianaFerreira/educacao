import numpy as np
import pandas as pd
from random import seed
from random import random
import matplotlib.pyplot as plt
# P = np.array([[0.2, 0.7, 0.1],
#               [0.9, 0.0, 0.1],
#               [0.2, 0.8, 0.0]])
#
# stateChangeHist= np.array([[0.0,  0.0,  0.0],
#                           [0.0, 0.0,  0.0],
#                           [0.0, 0.0,  0.0]])
# state=np.array([[1.0, 0.0, 0.0]])

P = np.array([[0.0, 0.89, 0.09, 0.02, 0.0, 0.0, 0.0], [0.0, 0.17, 0.64, 0.06, 0.0, 0.0, 0.13],
     [0.0, 0.0, 0.1, 0.75, 0.08, 0.0, 0.07], [0.0, 0.0, 0.0, 0.08, 0.84, 0.04, 0.04],
     [0.0, 0.0, 0.0, 0.0, 0.37, 0.61, 0.02], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])

stateChangeHist= np.array([[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0],[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0],
[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0],[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0],
[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0],[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0],
[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0]])

state=np.array([[1, 0, 0, 0, 0, 0, 0]])



currentState=0
stateHist=state
dfStateHist=pd.DataFrame(state)
#distr_hist = [[0,0,0]]
distr_hist = [[0,0,0,0,0,0,0]]
seed(4)

# Simulate from multinomial distribution
def simulate_multinomial(vmultinomial):
  r=np.random.uniform(0.0, 1.0)
  CS=np.cumsum(vmultinomial)
  CS=np.insert(CS,0,0)
  m=(np.where(CS<r))[0]
  nextState=m[len(m)-1]
  return nextState

for x in range(1000):
  currentRow=np.ma.masked_values((P[currentState]), 0.0)
  nextState=simulate_multinomial(currentRow)
  # Keep track of state changes
  stateChangeHist[currentState,nextState]+=1
  # Keep track of the state vector itself
  #state=np.array([[0,0,0]])
  state=np.array([[0,0,0,0,0,0,0]])
  state[0,nextState]=1.0
  # Keep track of state history
  stateHist=np.append(stateHist,state,axis=0)
  currentState=nextState
  # calculate the actual distribution over the 3 states so far
  totals=np.sum(stateHist,axis=0)
  gt=np.sum(totals)
  distrib=totals/gt
  #distrib=np.reshape(distrib,(1,3))
  distrib=np.reshape(distrib,(1,7))
  distr_hist=np.append(distr_hist,distrib,axis=0)

print(distrib)
P_hat=stateChangeHist/stateChangeHist.sum(axis=1)[:,None]
# Check estimated state transition probabilities based on history so far:
print(P_hat)
dfDistrHist = pd.DataFrame(distr_hist)
# Plot the distribution as the simulation progresses over time
dfDistrHist.plot(title="Simulation History")
plt.show()