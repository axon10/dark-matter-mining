"""
    Download refseq genomes based on abundance threshold from sorted taxonomic-based abundance profile.
    Update abundances of each taxonomy based on available refseq genomes.

"""

import os
import pandas as pd  
from pandas.api.types import is_numeric_dtype

#TODO-implement option for related taxa.

refseq_norman_PATH="/mnt/storage/grid/home/norman/16S/refseq/refseq_genomes"
taxonomies = pd.read_csv("sorted_species_abundance.csv")
#fix headers
headers=["taxid"] + [x for x in list(taxonomies.columns)[1:]]
taxonomies.columns = pd.Index(headers)
taxonomies["abundances"] = taxonomies["sum"]/ taxonomies["sum"].sum() * 100

with open("assembly_summary_refseq.txt", "r+") as f:
    file_lines=f.readlines()
assembly = pd.DataFrame([string.split("\t") for string in file_lines])
#print(len(assembly))

#fix headers
assembly.columns = assembly.iloc[0]
assembly=assembly[1:]
assembly = assembly.set_index("assembly_accession", drop=False)
#print(assembly.columns)
#drop to only revelant assemblies/taxons
desired_rows=taxonomies[taxonomies["abundances"] >= 0.0001]
desired_taxa = [str(x) for x in list(desired_rows["taxid"])]
assembly = assembly[assembly['taxid'].isin(desired_taxa)]
assembly['taxid']=assembly['taxid'].astype(int)
assembly = assembly[assembly["assembly_level"] == "Complete Genome"]

# drop duplicate genomes
# TODO: implement option for multiple strains /taxid to better capture diversity
assembly = assembly.drop_duplicates(subset=['taxid'])

# fix abundances now that dropped taxa are included
taxonomies = taxonomies[taxonomies['taxid'].isin(list(assembly['taxid']))]
taxonomies["fixed_abundances"] = taxonomies["sum"]/taxonomies["sum"].sum() * 100

assembly["filepath"]=assembly['ftp_path'].apply(lambda x: x.split("/")[-1]+"_genomic.gbff")

"""
# download the assembly
for index, row in assembly.iterrows():
    filepath=row['ftp_path']
    filename=filepath.split("/")[-1]+"_genomic.gbff.gz"

    if filename not in os.listdir(refseq_norman_PATH) and filename not in os.listdir("../refseq_genomes"):
        cmd = "wget -P ./genomes/ "+filepath+"/"+filename
        os.system("wget -P ./genomes/ "+filepath+"/"+filename)
    else:
        #copy the ref genome from norman's path to mine
        cmd = "cp " + refseq_norman_PATH + "/" + filename + " ./genomes/"
        os.system("cp " + refseq_norman_PATH + "/" + filename + " ./genomes/")
assembly.to_csv("no_duplicates_assembly_ref.csv")
taxonomies.to_csv("no_duplicates_taxonomy.csv") """

print(assembly.columns)
# keep only taxonomy ID and abundance
taxonomies = taxonomies.iloc[:,[0,-1]]
assembly = assembly.iloc[:, [5,-1]]
# Reindex using taxonomy ID and merge

taxonomies = taxonomies.set_index('taxid')
assembly = assembly.set_index('taxid')

print(taxonomies.index, len(taxonomies))
print(assembly.index, len(assembly))
# merge taxonomy ID with assemblies, and drop all rows
abundances_file = pd.merge(assembly, taxonomies, left_index=True, right_index=True).sort_values('fixed_abundances', ascending=False)
abundances_file.to_csv("refseq_abundancies.txt", sep="\t", index=False)
