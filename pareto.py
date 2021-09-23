import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


df = pd.read_csv("docs/df_survivability_bsi-bcc-atualizado.csv")
df = df.loc[df['CD_PERD_ADMIS'] < 2014]

# Categorias

df = df.loc[df['NM_COR_RACA'] == 'PARDA']
# df = df[df['NM_SEXO'] == 'F']
# df = df[df['NM_PROGR_FORM'] == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO']
# df = df[df['NM_PROGR_FORM'] == 'BACHARELADO EM CIÊNCIA DA COMPUTAÇÃO']


item_counts = df["DURACAO_VINCULO"].value_counts().sort_index()
print(item_counts)

df = pd.DataFrame({'estudantes': item_counts})
df.index = item_counts.index
df = df.sort_values(by='estudantes',ascending=False)
df["percentage"] = df["estudantes"].cumsum()/df["estudantes"].sum()*100


fig, ax = plt.subplots()
ax.bar(df.index, df["estudantes"], color="dimgray")
ax2 = ax.twinx()
ax2.plot(df.index, df["percentage"], color="darkgray", marker="D", ms=7)
ax2.axhline(95, color="darkgray", linestyle="dashed")
ax2.yaxis.set_major_formatter(PercentFormatter())

ax.tick_params(axis="y", colors="black")
ax2.tick_params(axis="y", colors="black")
plt.xticks(range(0, 21))
title = "Parda"
plt.title(title)
plt.savefig(f"imgs/pareto/pareto-{title}.png")
plt.show()
