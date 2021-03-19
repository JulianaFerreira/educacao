import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class Plot:

    def barplot(self, title, height, bars):
        # Make a random dataset:
        y_pos = np.arange(len(bars))

        # Create bars
        plt.bar(y_pos, height)
        plt.title(title)

        # Create names on the x-axis
        plt.xticks(y_pos, bars)

        # Show graphic
        plt.show()

    def groupedbarplot(self):
        # set plot style: grey grid in the background:
        sns.set(style="darkgrid")

        # load dataset
        tips = sns.load_dataset("tips")

        # Set the figure size
        plt.figure(figsize=(8, 8))

        # grouped barplot
        sns.barplot(x="day", y="total_bill", hue="retido", data=tips, ci=None)
        plt.show()







