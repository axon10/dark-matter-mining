import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 

df = pd.read_csv("krona_classification.csv")
sns.set_context(rc={"axes.labelsize":10}) 
sns.set(font_scale=0.5)
sns.heatmap(df, xticklabels=True,yticklabels=True,
    fmt = "d", annot = True, annot_kws={"size": 3})

    