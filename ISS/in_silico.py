from nltk import ngrams
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import io
genome = io.StringIO(
    """
>NZ_LN874954.1 Escherichia coli strain LM33 isolate patient, whole genome shotgun sequence
GAAACGCCGTAGCGCCGATGGTAGTGTGGGGTCTCCCCATGCGAGAGTAGGGAACTGCCAGGTATCAAAT
TAAGCAGTAAGCCGGTCATAAAACCGGTGGTTGTAAAAGAATTCGGTGGAGCGGTAGTTCAGTCGGTTAG
AATACCTGCCTGTCACGCAGGGGGTCGCGGGTTCGAGTCCCGTCCGTTCCGCCACTTACTAAGAAGCCTC
GAGTTAACGCTCGAGGTTTTTTTTCGTTTGTATTTCTATTATTGCCAAAATCGCAAAAATCCTCTGCGTT
TTACGCCATTTTTCCGCAACAGTCTGAAGCCCATAATCACCTCAGTTAACGAAAATAGCATTAAAAGAGG
CATATTATGGCTATCCCTGCATTTGGTTTAGGCACTTTCCGTCTGAAAGACGACGTTGTTATTTCATCTG
TGAAAACGGCGCTTGAACTTGATTATCGCGCAATTGATACCGCACAAATCTATGATAACGAAGCCGCAGT
AGGTCAGGCGATTGCAGAAAGTGGCGTGCCACGTCATGAACTCCACATCACCACTAAAATCTGGATTGAA
AATCTCAGCAAAGACAAATTGATCCCGAGTCTGAAAGAGAGCCTGCAAAAATTGCGTACCGATTATGTTG
ATCTGACGCTAATCCACTGGCCGTCACCAAACGATGAAGTCTCTGTTGAAGAGTTTATGCAGGCGCTGCT
"""
)

# Config
read_length = 150
insert_length = 500
genome_soup = []
# Break into ngrams/kmers
seqs = SeqIO.parse(genome, "fasta")
for seq in seqs:
    seq_id = seq.id
    all_kmers = list(ngrams(seq, insert_length))
    all_kmers = [kmer[0:read_length] + complement(kmer[read_length-insert_length:]) for kmer in all_kmers]

    # add some logic here to randomly sample k-mers, simulating in-silico dataset
    reads = ["".join(x) for x in all_kmers] # not sure if this line is needed
    # split into read tuples with forward and reverse
    all_reads = [(read[0:read_length],read[read_length, len(read)] for read in all_kmers)]
    # add some logic here so that sequence knows how many bp is between the forward and reverse, and that there are 2 records input
    records = [
        SeqRecord(
            seq=Seq(x),
            id="%s_%d" % (seq_id, i),
            letter_annotations={"phred_quality": [40] * len(x)},
        )
        for i, x in enumerate(reads)
    ]
    genome_soup.extend(records)

def complement(read):
    key = {"A":"T", "C":"G", "G":"C", "T":"A"}
    complement = str([key[base] for base in read])
    return complement
# write out the paired reads
SeqIO.write(genome_soup, "ecoli_test.fastq", "fastq")

#Steps to build an in-silico sequencer
# 1. get large genome
# 2. Get ngrams of length (insert length, which includes the actual insert as well as the front and back)
# 3. Sample certain number of ngrams (normal? idk. Have to look into this)
# 3 transform all sampled ngrams by dropping the center, retaining the foward, and reversing the back (keep as string)
# 4. for each ngram, add the forward and reverse as separate reads
