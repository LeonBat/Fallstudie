#!/usr/bin/env python

import qiime2.plugins.vsearch.actions as vsearch_actions
from qiime2 import Artifact

# 1. Load the files from DADA2 step
print("Loading DADA2 files...")
table = Artifact.load('table.qza')
representative_sequences = Artifact.load('rep-seqs.qza')

# 2. Run VSEARCH Clustering
print("Running VSEARCH Clustering (97%)...")

results = vsearch_actions.cluster_features_de_novo(
    sequences=representative_sequences,
    table=table,
    perc_identity=0.97,  # 97 % OTUs
    strand='plus',       # Standard for Illumina
    threads=0            # Use all available cores
)

# 3. Extract the outputs
clustered_table = results.clustered_table
clustered_sequences = results.clustered_sequences

# 4. Save the new files
print("Saving OTU files...")
clustered_table.save('table-dn-97.qza')
clustered_sequences.save('rep-seqs-dn-97.qza')

print("Done! OTUs created.")