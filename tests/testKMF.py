from lifelines.datasets import load_waltons
from lifelines import KaplanMeierFitter
from matplotlib import pyplot as plt


times = [5, 6, 7, 2, 4, 4, 3, 6, 4, 7]
event_g = [1, 1, 1, 0, 0, 0, 0, 1, 0, 1]
event_e = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0]

# durations = [5, 6, 7, 2, 4, 4, 3, 6, 4, 7, 4, 4]
# event_g = [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1]
# event_e = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0]
#
# durations = [5, 6, 7, 2, 4, 4, 3, 6, 4, 7, 8, 10]
# event_g = [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1]
# event_e = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0]
#
# durations = [5, 6, 7, 2, 4, 4, 3, 6, 4, 7, 8, 10]
# event_g = [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0]
# event_e = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1]


kmf = KaplanMeierFitter()
kmf.fit(times, event_g)
kmf.plot_survival_function(ci_show=False)
plt.show()
kmf.fit(times, event_e)
kmf.plot_survival_function(ci_show=False)
plt.show()
kmf.plot_cumulative_density(ci_show=False)
plt.show()








# df = load_waltons()
# print(df)

# T = df['T']
# E = df['E']
# print(E)


# kmf.plot_cumulative_density()
# plt.show()

# Colocar no print
# kmf.event_table
# kmf.predict([0,10])
# kmf.survival_function_
# kmf.cumulative_density_
# kmf.median_survival_time_
# kmf.confidence_interval_
# kmf.conditional_time_to_event_

