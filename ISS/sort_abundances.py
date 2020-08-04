import pandas as pd

df = pd.read_csv("abundance_profile_fixed.csv", index_col=0)
df = df.replace(np.nan, 0)
df['sum'] = df.sum(axis=1)
df = df.sort_values(by='sum', ascending = False)
print(df.head())
df.to_csv("sorted_classification.csv", index=True)
