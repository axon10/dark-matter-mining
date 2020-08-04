# filter taxids to only species level 
import pandas as pd 
bacteria = pd.read_csv("CanolaClassificationTable.csv", index_col=0) 

#drop any classifications without refseq for species-specificity
bacteria = bacteria.dropna(subset=["species"])

taxids = bacteria.index
print(taxids)
species = bacteria["species"]

print("Index\n", species.index)
sorted_classification = pd.read_csv("sorted_classification.csv", index_col = 0)
sorted_classification.insert(0,'species', species)

sorted_classification = sorted_classification[sorted_classification.index.isin(taxids)]
# drop zeros
sorted_classification = sorted_classification.loc[sorted_classification['sum'] != 0]


print(type(sorted_classification))
sorted_classification.to_csv("sorted_refseq_genomes.csv", index=True) 


