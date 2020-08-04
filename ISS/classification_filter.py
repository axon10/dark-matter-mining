'''
    Sort abundance profile by decreasing taxonomic frequency/abundance and drop taxa with no species annotation, via 
    filtering out taxonomies from combined samples to those with 'species' field available, aka those with possible
    refseq genomes from NCBI.

'''
 
import pandas as pd 

#drop any classifications without refseq for species-specificity
species_only = pd.read_csv("CanolaClassificationTable.csv", index_col=0).dropna(subset=["species"])

taxids = species_only.index
species = species_only["species"]


abundance_profile = pd.read_csv("abundance_profile_fixed.csv", index_col=0)
abundace_profile = abundance_profile.replace(np.nan, 0)
abundance_profile['sum'] = abundance_profile.sum(axis=1)

sorted_abundance_profile = abundance_profile.sort_values(by='sum', ascending = False)

# add species annotations and select for certain taxIDs
sorted_abundance_profile.insert(0,'species', species)
sorted_abundance_profile = sorted_abundance_profile[sorted_abundance_profile.index.isin(taxids)]

sorted_abundance_profile.to_csv("sorted_species_abundance.csv", index=True) 


