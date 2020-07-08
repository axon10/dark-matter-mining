import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt 
import os
from time import perf_counter

SAMPLE_ID="SRR10547735"
rf = {}
index = {}
classifications = {}
unique_taxa = []
unique_samples = []

header = "/mnt/storage/grid/var/metagenomic_samples/Testing2/combined/"
i = 0
for kraken_file in os.listdir(header):
   # if i > 10:
    #   break
   # i += 1
    with open(str(header + kraken_file)) as f:
        for line in f:
            line = line.split()
            if len(line) >= 1:
                sample = line[1][0:len(SAMPLE_ID)]
                taxonomy = line[0]
                if (taxonomy != "U"):
                    taxonomy = line[3]
                if (sample, taxonomy) not in classifications.keys():
                    classifications[(sample, taxonomy)] = 1
                else:
                    classifications[(sample, taxonomy)] +=1
                unique_taxa = list(set(unique_taxa + [taxonomy]))
                unique_samples = list(set(unique_samples + [sample]))
    print('Finished reading ', kraken_file)

df = pd.DataFrame(0, index = unique_samples, columns = unique_taxa)
start = perf_counter()
for classification in classifications.keys():  
    df.loc[classification[0], classification[1]] = classifications[classification]
print('Time taken 4 DF: ', perf_counter() - start)
print('Columns: ', len(df.columns))
start = perf_counter()
df.to_csv('/mnt/storage/grid/var/metagenomic_samples/Testing2/krona_classification_test_optimized.csv',)
print('Time taken 4 csv: ', perf_counter() - start)
start = perf_counter()
df = df.loc[:, (df != 0).any(axis=0)]
print(df)
sns.set_context(rc={"axes.labelsize":10}) 
sns.set(font_scale=0.5)
picture = sns.heatmap(df, xticklabels=True,yticklabels=True,
    fmt = "d", annot = True, annot_kws={"size": 3})
plt.xlabel("Taxonomy ID")
plt.ylabel("Sample ID")
plt.figure(figsize =(40,40))
figure = picture.get_figure()
figure.savefig('/mnt/storage/grid/var/metagenomic_samples/Testing2/classification_test_optimized.png', bbox_inches='tight', dpi=300)
print('Time taken 4 map: ', perf_counter() - start)
