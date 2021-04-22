from lifelines.datasets import load_waltons
from lifelines import KaplanMeierFitter, CoxPHFitter, NelsonAalenFitter
from lifelines.statistics import logrank_test
from matplotlib import pyplot as plt


times = [5, 6, 7, 2, 4, 4, 3, 6, 4, 7]
event_g = [1, 1, 1, 0, 0, 0, 0, 1, 0, 1]
event_e = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0]

# times = [5, 6, 7, 2, 4, 4, 3, 6, 4, 7, 4, 4]
# event_g = [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1]
# event_e = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0]
#
# times = [5, 6, 7, 2, 4, 4, 3, 6, 4, 7, 8, 10]
# event_g = [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1]
# event_e = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0]
#
# times = [5, 6, 7, 2, 4, 4, 3, 6, 4, 7, 8, 10]
# event_g = [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0]
# event_e = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1]


# kmf = KaplanMeierFitter()
# kmf.fit(times, event_g)
# kmf.plot_survival_function(ci_show=False)
# plt.show()
# kmf.fit(times, event_e)
# kmf.plot_survival_function(ci_show=False)
# plt.show()
# kmf.plot_cumulative_density(ci_show=False)
# plt.show()




times = [5, 6, 7, 2, 4, 4, 3, 6, 4, 7]
event_e = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0]
times1 = [1, 6, 5, 6, 1, 4, 3, 5, 2, 7]
event_e1 = [1, 0, 1, 0, 1, 1, 1, 0, 1, 0]

kmf = KaplanMeierFitter()
kmf.fit(times, event_e)
kmf.plot_survival_function(ci_show=False)
# kmf.fit(times1, event_e1)
# kmf.plot_survival_function(ci_show=False)

plt.show()

print(kmf.event_table)
print("Quantidade de estudantes por ano")
print(kmf.event_table.at_risk)
print("Tempo médio de sobrevivencia")
print(kmf.median_survival_time_)
print(kmf.survival_function_)
print("Probabilidade de evadir pelo tempo")
print(kmf.cumulative_density_)
print(kmf.predict([0, 4, 7]))
print(kmf.confidence_interval_)
print(kmf.conditional_time_to_event_)




# print("cox")
# # Using Cox Proportional Hazards model
# cph = CoxPHFitter()   ## Instantiate the class to create a cph object
# cph.fit(times, event_e)
# cph.fit(times, event_e1)
# cph.print_summary()    ## HAve a look at the significance of the features





# HAZARD
naf = NelsonAalenFitter()

naf.fit(times, event_e)

print(naf.cumulative_hazard_)
naf.plot_cumulative_hazard()
plt.show()









# LOGRANK
print("logrank")
results = logrank_test(times, times1, event_e, event_e1)
results.print_summary()
print(results.p_value)



















# df = load_waltons()
# print(df)

# T = df['T']
# E = df['E']
# print(E)


# kmf.plot_cumulative_density()
# plt.show()


