'''
    Download refseq genomes based on abundance threshold from sorted taxonomic-based abundance profile.
    Update abundances of each taxonomy based on available refseq genomes.

'''
import os
import pandas as pd  
from pandas.api.types import is_numeric_dtype

#TODO-implement option for related taxa.

refseq_norman_PATH="/mnt/storage/grid/home/norman/16S/refseq/refseq_genomes"
taxonomies = pd.read_csv("/mnt/storage/grid/var/metagenomic_samples/Testing2/sorted_bacteria.csv")
#fix headers
headers=["taxid"] + [x for x in list(taxonomies.columns)[1:]]
taxonomies.columns = pd.Index(headers)
taxonomies["abundances"] = taxonomies["sum"]/ taxonomies["sum"].sum() * 100

with open("assembly_summary_refseq.txt", "r+") as f:
    file_lines=f.readlines()
assembly = pd.DataFrame([string.split("\t") for string in file_lines])
print(len(assembly))

#fix headers
assembly.columns = assembly.iloc[0]
assembly=assembly[1:]
assembly = assembly.set_index("assembly_accession", drop=False)
print(assembly.columns)
#drop to only revelant assemblies/taxons
desired_rows=taxonomies[taxonomies["abundances"] >= 0.0001]
desired_taxa = [str(x) for x in list(desired_rows["taxid"])]
assembly = assembly[assembly['taxid'].isin(desired_taxa)]
assembly = assembly[assembly["assembly_level"] == "Complete Genome"]

# drop duplicate genomes
# TODO: implement option for multiple strains /taxid to better capture diversity
assembly = assembly.drop_duplicates(subset=['taxid'])

# fix abundances now that dropped taxa are included
taxonomies = taxonomies[taxonomies['taxid'].isin(list(assembly['taxid']))]
taxonomies["fixed_abundances"] = taxonomies["sum"]/taxonomies["sum"].sum() * 100


# download the assembly
for index, row in assembly.iterrows():
    filepath=row['ftp_path']
    filename=filepath.split("/")[-1]+"_genomic.gbff.gz"

    if filename not in os.listdir(refseq_norman_PATH):
        cmd = "wget -P ./genomes/ "+filepath+"/"+filename
        os.system("wget -P ./genomes/ "+filepath+"/"+filename)
        print(cmd)
    else:
        #copy the ref genome from norman's path to mine
        cmd = "cp " + refseq_norman_PATH + "/" + filename + " ./genomes/"
        os.system("cp " + refseq_norman_PATH + "/" + filename + " ./genomes/")
        print(cmd)
assembly.to_csv("no_duplicates_assembly_ref.csv")
taxonomies.to_csv("no_duplicates_taxonomy.csv")

#TODO-execute this part tomorrow when all files downloaded
assembly.set_index(["taxid"])
# merge assembly and taxonomies
# keep only the taxonomy ID and the abundance
x = taxonomies.iloc[:,[0,-1]]
# merge taxonomy ID with assemblies, and drop all rows
final = merge(x, assembly).loc[:, ["fixed_abundancy", "assembly_accession"]]
final.to_csv("abundancy.txt", sep="\t", index=False)
