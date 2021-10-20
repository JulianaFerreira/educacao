import pandas as pd
from scipy.stats import norm, ttest_rel, ttest_ind, chisquare, pearsonr, f_oneway, mannwhitneyu
from lifelines.statistics import logrank_test
import numpy as np

# tempos_evasao_bsi = [2, 3, 4, 2, 1, 9, 12, 7, 4, 4,
#                      1, 1, 2, 23, 1, 1, 4, 1, 2, 4,
#                      3, 3, 7, 2, 11, 3, 7, 4, 14, 6,
#                      3, 3, 9, 5, 10, 26, 5, 18, 2, 2,
#                      6, 2, 3, 9, 2, 4, 2, 9, 1, 8]
#
# tempos_evasao_bcc = [2, 4, 4, 6, 1, 14, 2, 4, 2, 3,
#                      4, 5, 2, 5, 1, 10, 1, 3, 4, 2,
#                      1, 5, 1, 24, 6, 6, 2, 7, 4, 2,
#                      13, 2, 3, 1, 3, 2, 17, 16, 2, 4,
#                      23, 1, 4, 5, 13, 7, 1, 10, 1, 10]

tempos_evasao_bsi = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
tempos_evasao_bcc = [2, 2, 3, 4, 7, 6, 5, 8, 10, 9]

# Student’s t-test
t, p_valor = ttest_ind(tempos_evasao_bsi, tempos_evasao_bcc)
print(p_valor)

# Paired Student’s t-test
t, p_valor = ttest_rel(tempos_evasao_bsi, tempos_evasao_bcc)
print(p_valor)

# Analysis of Variance Test (ANOVA)
# t, p_valor = f_oneway(tempos_evasao_bsi, tempos_evasao_bcc)
# print(p_valor)

# Chi-square - The chi-square test tests the null hypothesis that the categorical data has the given frequencies.
t, p_valor = chisquare(tempos_evasao_bsi, tempos_evasao_bcc)
print(p_valor)

results = logrank_test(tempos_evasao_bsi, tempos_evasao_bcc)
results.print_summary()
print(results.p_value)

# Mann-Whitney Correlation Coefficient
stat, p_valor = mannwhitneyu(tempos_evasao_bsi, tempos_evasao_bcc)
print(p_valor)

# Pearson’s Correlation Coefficient
stat, p_valor = pearsonr(tempos_evasao_bsi, tempos_evasao_bcc)
print(p_valor)


# print("Student’s t-test para Desvinculação:")
# t, p = ttest_ind(time, time1)
# print(p)
#
# print("Paired Student’s t-test para Desvinculação:")
# #t, p = ttest_rel(time_dados_pareado[:300], time_dados_pareado1[:300])
# t, p = ttest_rel(time[:9000], time1[:9000])
# print(p)
#
# print("Chi-square para Desvinculação:")
# #t, p = chisquare(time_dados_pareado[:300], f_exp=time_dados_pareado1[:300])
# t, p = chisquare(time[:9000], f_exp=time1[:9000])
# print(p)
#
# print("Logrank test para Desvinculação:")
# results = logrank_test(time, time1)
# results.print_summary()
# print(results.p_value)
#
# print("Mann-Whitney para Desvinculação:")
# t, p = mannwhitneyu(time, time1)
# print(p)
#
# print("Pearsonr para Desvinculação:")
# #t, p = pearsonr(time_dados_pareado[:300], time_dados_pareado1[:300])
# t, p = pearsonr(time[:9000], time1[:9000])
# print(p)


# Kolmogorov Smirnov Test

# def d_crit_two_way(arr1, arr2):
#     return 1.36*np.sqrt(len(arr1)**-1 + len(arr2)**-1)
#
# def kolmogorov_smirnov_test(samp_a, samp_b, label1, label2):
#     # Apenas para teste com +1 nos 100 primeiros e últimos do modelo
#     # samp_a.sort()
#     # for i in range(len(samp_a)/2):
#     #     samp_a[i] = samp_a[i] * 1.1
#     #
#     # for i in range(len(samp_a)/2, len(samp_a)):
#     #     samp_a[i] = samp_a[i] * 0.9
#
#     # concatenate and sort
#     samp_conc = np.sort(np.concatenate((samp_a, samp_b)))
#
#     # cdf of sample a
#     samp_a_cdf = [np.round(st.percentileofscore(samp_a, value) / 100, 1) for value in samp_conc]
#
#     # cdf of sample b
#     samp_b_cdf = [np.round(st.percentileofscore(samp_b, value) / 100, 1) for value in samp_conc]
#
#     # compute absolute difference
#     samp_diff = np.abs(np.subtract(samp_a_cdf, samp_b_cdf))
#
#     # get max difference
#     dn_ks = max(samp_diff)
#     print("dn_ks:", dn_ks)
#
#     print("dn_crit:", d_crit_two_way(samp_a, samp_b))
#
#     plt.figure(figsize=(10, 5))
#     plt.plot(samp_conc, samp_a_cdf, label=label1)
#     plt.plot(samp_conc, samp_b_cdf, label=label2)
#
#     for val, p1, p2 in zip(samp_conc, samp_a_cdf, samp_b_cdf):
#         plt.plot([val, val], [p1, p2], color='green', alpha=0.2)
#
#     plt.legend()
#     plt.ylabel("F(x)")
#     plt.xlabel('x')
#     plt.title("KS Test - Dados x Modelo(pareto) [BCC] - Teste com +1 no tempo")
#
#     plt.show()
#
#     #t, p = stats.kstest(samp_conc, 'norm', args=(mean(samp_conc), std(samp_conc)), N=len(samp_conc))
#     t, p = ks_2samp(np.sort(samp_a), np.sort(samp_b))
#     print("p-valor:", p)
#
#     t, p = ttest_ind(samp_a, samp_b)
#     print(p)
#
#     t, p = ttest_rel(samp_a, samp_b)
#     print(p)