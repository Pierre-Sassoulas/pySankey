import matplotlib.pyplot as plt
import pandas as pd
from pysankey import sankey

df = pd.read_csv("../pysankey/fruits.txt", sep=" ", names=["true", "predicted"])

colorDict = {
    "apple": "#f71b1b",
    "blueberry": "#1b7ef7",
    "banana": "#f3f71b",
    "lime": "#12e23f",
    "orange": "#f78c1b",
    "kiwi": "#9BD937",
}

labels = list(colorDict.keys())
leftLabels = [label for label in labels if label in df["true"].values]
rightLabels = [label for label in labels if label in df["predicted"].values]

ax = sankey(
    left=df["true"],
    right=df["predicted"],
    leftLabels=leftLabels,
    rightLabels=rightLabels,
    colorDict=colorDict,
    aspect=20,
    fontsize=12,
)

plt.savefig("img/fruits.png")
plt.close()


# This calculates how often the different combinations of "true" and
# "predicted" co-occure
df = df.groupby(["true", "predicted"]).size().reset_index()
weights = df[0].astype(float)


ax = sankey(
    left=df["true"],
    right=df["predicted"],
    rightWeight=weights,
    leftWeight=weights,
    leftLabels=leftLabels,
    rightLabels=rightLabels,
    colorDict=colorDict,
    aspect=20,
    fontsize=12,
)


plt.savefig("img/fruits_weighted.png")
