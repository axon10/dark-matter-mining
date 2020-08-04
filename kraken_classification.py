'''

Create an abundance profile in CSV format from a combination of metagenomic DNA samples.

'''
import pandas as pd
from tqdm import tqdm
from glob import glob

classifications = {}

for kraken_file in tqdm(glob("/mnt/storage/grid/var/metagenomic_samples/Testing2/combined/*")):
    # read file
    this_df = pd.read_csv(kraken_file, sep="\t", header=None)
    # split 2nd column and make a new one 
    this_df['sample_id'] = this_df[1].apply(lambda x: x.split('.')[0])
   
    for sample in this_df['sample_id'].unique():
        # select rows where sample ID matches, aka subset DF to sample
        sample_df = this_df[this_df['sample_id'] == sample]
        # if this sample is not present, then
        if classifications.get(sample) is None: 
            # add series of counts (3rd column)
            classifications[sample] = sample_df[2].value_counts()
        else:
            # add unique counts to prexisting sample
            classifications[sample].add(sample_df[2].value_counts(), fill_value=0)

classifications_df = pd.DataFrame(classifications)
classifications_df.to_csv('/mnt/storage/grid/var/metagenomic_samples/Testing2/abundance_profile_fixed.csv')
