import pandas as pd
from scipy.stats import norm, ttest_rel, ttest_ind, chisquare
from lifelines.statistics import logrank_test
import numpy as np

tempos_evasao_bsi = [2, 3, 4, 2, 1, 9, 12, 7, 4, 4,
                     1, 1, 2, 23, 1, 1, 4, 1, 2, 4,
                     3, 3, 7, 2, 11, 3, 7, 4, 14, 6,
                     3, 3, 9, 5, 10, 26, 5, 18, 2, 2,
                     6, 2, 3, 9, 2, 4, 2, 9, 1, 8]

tempos_evasao_bcc = [2, 4, 4, 6, 1, 14, 2, 4, 2, 3,
                     4, 5, 2, 5, 1, 10, 1, 3, 4, 2,
                     1, 5, 1, 24, 6, 6, 2, 7, 4, 2,
                     13, 2, 3, 1, 3, 2, 17, 16, 2, 4,
                     23, 1, 4, 5, 13, 7, 1, 10, 1, 10]


# Student’s t-test
t, p_valor = ttest_ind(tempos_evasao_bsi, tempos_evasao_bcc)
print(p_valor)

# Paired Student’s t-test
t, p_valor = ttest_rel(tempos_evasao_bsi, tempos_evasao_bcc)
print(p_valor)

# Chi-square - The chi-square test tests the null hypothesis that the categorical data has the given frequencies.
t, p_valor = chisquare(tempos_evasao_bsi, tempos_evasao_bcc)
print(p_valor)
