from lifelines.datasets import load_waltons
from lifelines import KaplanMeierFitter
df = load_waltons() # returns a Pandas DataFrame

from matplotlib import pyplot as plt

plt.ion()

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

kmf.survival_function_
kmf.cumulative_density_
kmf.plot_survival_function()
#kmf.plot_cumulative_density()