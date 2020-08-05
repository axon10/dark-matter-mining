'''
    Convert Genbank flat file format (raw RefSeq genome format) to accepted FASTA format.
'''
from Bio import SeqIO
header = "/mnt/storage/grid/home/norman/16S/refseq/refseq_genomes/"
#header = ""
outheader ="/mnt/storage/grid/home/ana/dmm/ISS/"
genbank_f = "GCF_902806445.1_P4284_genomic.gbff"
#genbank_f= "SRS121011.fasta"

records= SeqIO.parse("/mnt/storage/grid/home/norman/16S/refseq/refseq_genomes/"+ genbank_f, "genbank")
print(len(list(records)))
for record in records:
   print(record.id)
   print(record.description)
   print(record) 
count = SeqIO.convert(header+genbank_f, "genbank", genbank_f.replace("gbff", "fasta"), "fasta")

print("Converted %i records" % count)
