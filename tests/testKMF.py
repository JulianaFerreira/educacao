from lifelines.datasets import load_waltons
from lifelines import KaplanMeierFitter
df = load_waltons() # returns a Pandas DataFrame

from matplotlib import pyplot as plt

durations = [5,6,6,2.5,4,4]
event_observed = [1, 0, 0, 1, 1, 1]
label='Kaplan Meier Estimate'

print(df)
"""
    T  E    group
0   6  1  miR-137
1  13  1  miR-137
2  13  1  miR-137
3  13  1  miR-137
4  19  1  miR-137
"""

T = df['T']
E = df['E']
#print(E)

kmf = KaplanMeierFitter()
kmf.fit(T, event_observed=E)

#Colocar no print
kmf.event_table
kmf.predict([0,10])
kmf.survival_function_
kmf.cumulative_density_
kmf.median_survival_time_
kmf.confidence_interval_
kmf.conditional_time_to_event_

kmf.plot_survival_function()
plt.show()
kmf.plot_cumulative_density()
plt.show()