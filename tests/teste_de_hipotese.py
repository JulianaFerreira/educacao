import pandas as pd
from scipy.stats import norm
import numpy as np

amostra = [509, 505, 495, 510, 496, 509, 497, 502, 503, 505,
           501, 505, 510, 505, 504, 497, 506, 506, 508, 505,
           497, 504, 500, 498, 506, 496, 508, 497, 503, 501,
           503, 506, 499, 498, 509, 507, 503, 499, 509, 495,
           502, 505, 504, 509, 508, 501, 505, 497, 508, 507]

amostra = pd.DataFrame(amostra, columns=['Amostra'])
amostra.head()
media_amostra = amostra.mean()[0]
media_amostra
# 503.24
desvio_padrao_amostra = amostra.std()[0]
desvio_padrao_amostra
# 4.48
media = 500 # A média que estamos testando
significancia = 0.05
confianca = 1 - significancia
n = 50 # Amostra de tamanho 50


probabilidade = (0.5 + (confianca/2))
probabilidade
# 0.975 é o 95% de nível de confiança + 2.5 (significância/2)
z_alpha_2 = norm.ppf(probabilidade)
z_alpha_2
# 1.96

z = (media_amostra - media) / (desvio_padrao_amostra / np.sqrt(n))
# 5.10

p_valor = 1 - norm.cdf(z)
# e

p_valor = norm.sf(z)
# 0,99998