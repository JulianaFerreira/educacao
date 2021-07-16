import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


df = pd.read_csv("docs/df_survivability_bsi-bcc-atualizado1.csv")
df = df.loc[df['CD_PERD_ADMIS'] < 2014]

# Categorias

# df = df.loc[df['NM_COR_RACA'] == 'BRANCA']
# df = df[df['NM_SEXO'] == 'M']
# df = df[df['NM_PROGR_FORM'] == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO']
# df = df[df['NM_PROGR_FORM'] == 'BACHARELADO EM CIÊNCIA DA COMPUTAÇÃO']


item_counts = df["DURACAO_VINCULO"].value_counts()
print(item_counts)

df = pd.DataFrame({'estudantes': item_counts})
df.index = item_counts.index
df = df.sort_values(by='estudantes',ascending=False)
df["percentage"] = df["estudantes"].cumsum()/df["estudantes"].sum()*100


fig, ax = plt.subplots()
ax.bar(df.index, df["estudantes"], color="C0")
ax2 = ax.twinx()
ax2.plot(df.index, df["percentage"], color="C1", marker="D", ms=7)
ax2.axhline(95, color="orange", linestyle="dashed")
ax2.yaxis.set_major_formatter(PercentFormatter())

ax.tick_params(axis="y", colors="C0")
ax2.tick_params(axis="y", colors="C1")
plt.title("BCC")
plt.show()
