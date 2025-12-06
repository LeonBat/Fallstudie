#usr/bin/env python3

####Filtering Script

#Libraries
from qiime2 import Artifact
import qiime2.plugins.feature_table.actions as feature_table_actions
import os


# Declaring paths and names
unfiltered_otu_table_path = "../Step4_QCFeatureTableConstruction/table-dn-97.qza"
filtered_otu_table_path = "otu_table-filtered.qza"

if not os.path.exists(unfiltered_otu_table_path):
    raise FileNotFoundError(f"Please check again the path to the unfiltered OTU table: {unfiltered_otu_table_path}")

unfiltered_asv_table_path = "../Step4_QCFeatureTableConstruction/table.qza"
filtered_asv_table_path = "asv_table-filtered.qza"

if not os.path.exists(unfiltered_asv_table_path):
    raise FileNotFoundError(f"Please check again the path to the unfiltered ASV table: {unfiltered_asv_table_path}")


#Filtering the tables 


#ASV
print("Filtering ASV table to retain features present in at least 2 samples...")
try:
    unfiltered_table = Artifact.load(unfiltered_asv_table_path)
    filtered_artifact, = feature_table_actions.filter_features(
    table=unfiltered_table,
    min_samples=2
    )
except Exception as e:
    print(f"Something went wrong while filtering the table: {e}")
    
filtered_artifact.save(filtered_asv_table_path)
print(f"Filtered ASV table saved to {filtered_asv_table_path}")


#OTU
print("Filtering OTU table to retain features present in at least 2 samples...")
try:
    unfiltered_table = Artifact.load(unfiltered_otu_table_path)
    filtered_artifact, = feature_table_actions.filter_features(
    table=unfiltered_table,
    min_samples=2
    )
except Exception as e:
    print(f"Something went wrong while filtering the table: {e}")

filtered_artifact.save(filtered_otu_table_path)
print(f"Filtered OTU table saved to {filtered_otu_table_path}")




print("All filtering tasks are complete.")
