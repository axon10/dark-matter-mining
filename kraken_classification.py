import seaborn as sns
import pandas as pd
SAMPLE_ID="SRR10547735"
rf = {}
index = {}
with open("/home/ana/combined.kraken") as f:
    # read each line
    # taxonomy = y,
   
    for line in f.readlines():
        line = line.split()
        sample = line[1][0:len(SAMPLE_ID)]
        taxonomy = line[0]
        if (taxonomy != "U"):
            taxonomy = line[3]
        # if the sample is new 
        index[taxonomy] = 1
        if sample not in rf.keys():
            # add the sample ID
            rf[sample] = {taxonomy: 1}
        else:
            if taxonomy not in rf[sample].keys():
                # add new taxonomy
                rf[sample][taxonomy] = 1
            else:
                rf[sample][taxonomy] +=1
for sample in rf.keys():
    rf[sample] = list(rf[sample].values())
index = list(index.keys())

print(index, rf.keys())

sampleIDS = rf.keys()

df = pd.DataFrame.from_dict(rf, orient="index", columns=index)
print(df)
sns.clustermap(df.corr())