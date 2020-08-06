'''
    Convert Genbank flat file format (raw RefSeq genome format) to accepted FASTA format.
'''
from Bio import SeqIO
import os
import pandas as pd

other = "/mnt/storage/grid/home/norman/16S/refseq/refseq_genomes/"
local = "/mnt/storage/grid/home/ana/dark-matter-mining/ISS/refseq_genomes/"
abundance_PATH = "/mnt/storage/grid/home/ana/dark-matter-mining/ISS/refseq_abundancies.txt"

#index by filepath
abundancy_file = pd.read_csv(abundance_PATH, index_col= 0, delim_whitespace=True)
print(abundancy_file.columns)
print(abundancy_file.index)

genome_ID = []
for filename in abundancy_file.index:
    genbank_f = filename
    genome_PATH=''
    if genbank_f in os.listdir(other):
        genome_PATH=other
    else:
        genome_PATH=local
    out_PATH = "/".join(local.split('/')[0:-2]) + "/refseq_fasta/"
    records= SeqIO.parse(genome_PATH + genbank_f, "genbank")
    print(records)
    # only get first record in fasta file due to 1 taxon/abundance
    genome_ID.append(next(records).id)
    """
	
    TODO: implement all records, sharing equal abundance
    for record in records:
        print(record.id)
        genome_ID+=record.id
    """
    count = SeqIO.convert(genome_PATH + genbank_f, "genbank", out_PATH+genbank_f.replace("gbff", "fasta"), "fasta")
    print("Converted %i records" % count)
print(genome_ID)
abundancy_file.insert(0, 'genome_ID', pd.Series(genome_ID, index=abundancy_file.index))
abundancy_file.to_csv("/".join(abundance_PATH.split("/")[0:-1])+"/refseq_genomeID_abundancies.txt", index=False, sep="\t")

