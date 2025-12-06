#!/usr/bin/env python

import qiime2.plugins.feature_table.actions as feature_table_actions
from qiime2 import Artifact, Metadata

# 1. Load OTU files (from the VSEARCH step)
print("Loading OTU files...")
clustered_table = Artifact.load('table-dn-97.qza')
clustered_sequences = Artifact.load('rep-seqs-dn-97.qza')

# 2. Load Metadata 
print("Loading Metadata...")
metadata = Metadata.load('../Data/metadata_for_q.csv')

# --- Feature Table Summarize ---
print("Summarizing feature table...")
summary_results = feature_table_actions.summarize(
    table=clustered_table,
    sample_metadata=metadata
)
# Extract and save
table_viz = summary_results.visualization
table_viz.save('table-dn-97-summary.qzv')


# --- Tabulate Sequences ---
print("Tabulating sequences...")
tabulate_results = feature_table_actions.tabulate_seqs(
    data=clustered_sequences
)
# Extract and save
seq_viz = tabulate_results.visualization
seq_viz.save('rep-seqs-dn-97-summary.qzv')

print("Done! created 'table-dn-97-summary.qzv' and 'rep-seqs-dn-97-summary.qzv'")