import seaborn as sns
import pandas as pd
import matplotlib as plt 

SAMPLE_ID="SRR10547735"
rf = {}
index = {}
classifications = []
unique_taxa = []
unique_samples = []
with open("/mnt/storage/grid/var/metagenomic_samples/Testing2/combined.kraken") as f:
    for line in f.readlines():
        line = line.split()
        sample = line[1][0:len(SAMPLE_ID)]
        taxonomy = line[0]
        if (taxonomy != "U"):
            taxonomy = line[3]
        classifications.append((sample, taxonomy))
        unique_taxa = list(set(unique_taxa + [taxonomy]))
        unique_samples = list(set(unique_samples + [sample]))

df = pd.DataFrame(0, index = unique_samples, columns = unique_taxa)
for classification in classifications:
    df.loc[classification[0], classification[1]] +=1
print(df)
df.to_csv('/mnt/storage/grid/var/metagenomic_samples/Testing2/krona_classification.csv')

picture = sns.heatmap(df)
figure = picture.get_figure()
figure.savefig('/mnt/storage/grid/var/metagenomic_samples/Testing2/classification.png')

