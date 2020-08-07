import numpy as np
import pandas as pd
import os

abundance_percentage_PATH="refseq_genomeID_abundancies.txt"

abundance_fraction = pd.read_csv(abundance_percentage_PATH, delim_whitespace=True)
abundance_fraction.insert(0, 'abundance_percentage', abundance_fraction['fixed_abundances']/100)
abundance_fraction.iloc[:,0].to_csv(abundance_percentage_PATH.replace("abundancies", "abundancies_percentage"), index=False, sep="\t")
