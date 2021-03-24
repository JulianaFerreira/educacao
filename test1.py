import numpy as np
import pandas as pd
from random import seed
from random import random
import matplotlib.pyplot as plt
P = np.array([[0.057, 0.31, 0.0, 0.0, 0.603, 0.0, 0.03],
      [0.0, 0.187, 0.528, 0.0, 0.285, 0.0, 0.0],
      [0.0, 0.0, 0.012, 0.563, 0.097, 0.328, 0.0],
      [0.0, 0.0, 0.0, 0.039, 0.094, 0.814, 0.053],
      [0.001, 0.036, 0.02, 0.0, 0.0, 0.003, 0.94],
      [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])

stateChangeHist= np.array([[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0],
[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0],
[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0],
[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0],
[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0],
[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0],
[0.0,  0.0,  0.0, 0.0, 0.0, 0.0, 0.0]])

state=np.array([[1, 0, 0, 0, 0, 0, 0]])
currentState=0
stateHist=state
dfStateHist=pd.DataFrame(state)
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
for x in range(10):
  currentRow=np.ma.masked_values((P[currentState]), 0.0)
  nextState=simulate_multinomial(currentRow)
  # Keep track of state changes
  stateChangeHist[currentState,nextState]+=1
  # Keep track of the state vector itself
  state=np.array([[0,0,0,0,0,0,0]])
  state[0,nextState]=1.0
  # Keep track of state history
  stateHist=np.append(stateHist,state,axis=0)
  currentState=nextState
  # calculate the actual distribution over the 3 states so far
  totals=np.sum(stateHist,axis=0)
  gt=np.sum(totals)
  distrib=totals/gt
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


