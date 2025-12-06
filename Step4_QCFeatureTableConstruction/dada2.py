#!/usr/bin/env python

import qiime2.plugins.dada2.actions as dada2_actions
from qiime2 import Artifact

# 1. Load data 
print("Loading data...")
demux_paired = Artifact.load('../Step2_ImportingData/demux.qza')

# 2. Run DADA2
print("Running DADA2...")
results = dada2_actions.denoise_paired(
    demultiplexed_seqs=demux_paired,
    trim_left_f=15,     # Cut the first 20 bases (removes the "dip" at pos 11-14) 
    trunc_len_f=280,    # Truncate forward reads at 250 bases  
    trim_left_r=0,      # No trimming for reverse reads
    trunc_len_r=240,    # Truncate reverse reads at 200 bases
    n_threads=0         # Use all available cores
)

# 3. Extract the parts we need using their specific names
table = results.table
representative_sequences = results.representative_sequences
denoising_stats = results.denoising_stats

# 4. Saving the files 
print("Saving output files...")
table.save('table.qza')
representative_sequences.save('rep-seqs.qza')
denoising_stats.save('denoising-stats.qza')

print("Done!")