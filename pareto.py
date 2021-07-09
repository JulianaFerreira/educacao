import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


df = pd.read_csv("docs/df_survivability_bsi-bcc.csv")
df = df.loc[df['CD_PERD_ADMIS'] < 2014]

item_counts = df["DURACAO_VINCULO"].value_counts()
print(item_counts)

df = pd.DataFrame({'country': item_counts})
df.index = item_counts.index
df = df.sort_values(by='country',ascending=False)
df["cumpercentage"] = df["country"].cumsum()/df["country"].sum()*100


fig, ax = plt.subplots()
ax.bar(df.index, df["country"], color="C0")
ax2 = ax.twinx()
ax2.plot(df.index, df["cumpercentage"], color="C1", marker="D", ms=7)
ax2.axhline(95, color="orange", linestyle="dashed")
ax2.yaxis.set_major_formatter(PercentFormatter())

ax.tick_params(axis="y", colors="C0")
ax2.tick_params(axis="y", colors="C1")
plt.show()
