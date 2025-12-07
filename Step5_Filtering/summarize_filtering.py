#!/usr/bin/env python3

# Filtered Table Summarization Script


# Import necessary modules

from qiime2.plugins.feature_table.actions import filter_features
from qiime2.plugins.feature_table.actions import summarize_plus
import os
from qiime2 import Artifact, Metadata


# Define file paths
TABLE = os.path.join("asv_table-filtered.qza")
METADATA = os.path.join("../", "Data", "metadata_for_q.csv")



#Loading Artifacts
try:
    table = Artifact.load(TABLE)
    metadata = Metadata.load(METADATA)
except Exception as e:
    print(f"Error loading artifacts: {e}")
    raise


# Visualize the filtering results
try:
    asv_frequencies_ms2, sample_frequencies_ms2, asv_table_ms2_viz = summarize_plus(
        table=table,
        metadata=metadata,
    )
except Exception as e:
    print(f"Error during summarization: {e}")
    raise


# Save the visualization
asv_table_ms2_viz.save("asv_table-filtered-summary.qzv")