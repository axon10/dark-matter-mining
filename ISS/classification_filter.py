'''
    Sort abundance profile by decreasing taxonomic frequency/abundance and drop taxa with no species annotation, via 
    filtering out taxonomies from combined samples to those with 'species' field available, aka those with possible
    refseq genomes from NCBI.

'''
 
import pandas as pd 
import numpy as np

#drop any classifications lacking species annotation
species_only = pd.read_csv("canola_taxonomy_classification.csv", index_col=0).dropna(subset=["species"])
taxids = species_only.index

# drop irrelevant taxIDs, sort by abundance, drop NaNs
abundance_profile = pd.read_csv("abundance_profile.csv", index_col=0)
abundance_profile = abundance_profile[abundance_profile.index.isin(taxids)]

abundace_profile = abundance_profile.replace(np.nan, 0)
abundance_profile['sum'] = abundance_profile.sum(axis=1)
abundance_profile = abundance_profile.sort_values(by='sum', ascending = False)

# add species annotations
abundance_profile.insert(0,'species', species_only["species"])


abundance_profile.to_csv("sorted_species_abundance.csv", index=True) 


