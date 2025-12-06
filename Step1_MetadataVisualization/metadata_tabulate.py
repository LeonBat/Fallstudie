#!/usr/bin/env python

# Metadata tabulation

#This script reads a metadata file and generates a QIIME 2 visualization by 
#tabulating the metadata using tabulate from the qiime2.plugins

import qiime2
from qiime2.plugins.metadata.actions import tabulate
import os

# Setting up paths and filenames
METADATA_FILE = '../Data/metadata_for_q.csv' 

# Output visualization file name
OUTPUT_VIS_FILE = 'tabulated_metadata.qzv'

# --- Script Logic ---

# Check if the metadata file exists
if not os.path.exists(METADATA_FILE):
    print(f"Error: Metadata file not found at '{METADATA_FILE}'")
    print("Please ensure your metadata file is in the same directory and named correctly.")
    exit(1)

print(f"Reading metadata from: {METADATA_FILE}")

# The tabulate action requires the metadata to be passed as a QIIME 2 Metadata object.
# We read the file directly into this object.
try:
    metadata_obj = qiime2.Metadata.load(METADATA_FILE)
except Exception as e:
    print(f"Error loading metadata file. Check formatting (TSV/CSV dialect).")
    print(f"Details: {e}")
    exit(1)

# Run the 'metadata tabulate' action
print("Running qiime2.plugins.metadata.actions.tabulate...")
visualization, = tabulate(
    input=metadata_obj
)

# Save the resulting visualization artifact (.qzv)
visualization.save(OUTPUT_VIS_FILE)

print(f"\nSuccessfully created and saved visualization: {OUTPUT_VIS_FILE}")
print("You can view this file using 'qiime tools view metadata_tabulation.qzv'")
