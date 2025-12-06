#! usr/bin/env python3


### Script for Taxonomic Analysis

# Libraries
from qiime2 import Artifact
from qiime2 import Metadata
import qiime2.plugins.feature_classifier.actions as feature_classifier_actions
import qiime2.plugins.taxa.actions as taxa_actions

import os
from urllib.request import urlretrieve # Used for downloading the classifier file


# Paths and Names
READS = os.path.join("../", "Step4_QCFeatureTableConstruction/", "rep-seqs.qza")
METADATA = os.path.join("../", "Data/", "metadata_for_q.csv")
TABLE = os.path.join("../", "Step6_Decontamination/", "filtered-table.qza")

CLASSIFIER_FN = "2024.09.backbone.v4.nb.sklearn-1.4.2.qza"
CLASSIFIER_URL = "https://data.qiime2.org/classifiers/sklearn-1.4.2/greengenes2/2024.09.backbone.v4.nb.sklearn-1.4.2.qza"


OUTPUT_TAXONOMY = "taxonomy.qza"
OUTPUT_TAXONOMY_VIZ = "taxonomy_barplot.qzv"
# Getting classifier from URL

print("Downloading Greengenes classifier...")
try:
    # Check if the classifier already exists to skip download time
    if not os.path.exists(CLASSIFIER_FN):
        urlretrieve(CLASSIFIER_URL, CLASSIFIER_FN)
        print("Greengenes classifier downloaded successfully.")
    else:
        print("Classifier already exists locally. Skipping download.")
except Exception as e:
    print(f"An error occurred while downloading the classifier. Error: {e}")
    exit(1)
print("Greengenes classifier downloaded successfully.")


# Running taxonomic classification for ASV data

print("=============================================")
print("Running taxonomic classification for ASV data...")
print("=============================================")



print("Loading artifacts...")
try:
    classifier = Artifact.load("2024.09.backbone.v4.nb.sklearn-1.4.2.qza")
    reads_artifact = Artifact.load(READS)
    table_artifact = Artifact.load(TABLE)
    metadata = Metadata.load(METADATA)
    
except Exception as e:
    print(f"An error occurred while loading artifacts: {e}")
    exit(1)


print("Running classify sklearn...")
try:
    taxonomy, = feature_classifier_actions.classify_sklearn(
        classifier=classifier,
        reads=reads_artifact,
    )
    taxonomy.save(OUTPUT_TAXONOMY)

except Exception as e:
    print(f"An error occurred during taxonomic classification: {e}")

print("Taxonomic classification for ASV data finished.")



# Visualizing the results

print("==============================================")
print("Visualizing taxonomic composition for ASV data...")
print("==============================================")

try:
    taxa_bar_plots_viz, = taxa_actions.barplot(
        table=table_artifact,
        taxonomy=taxonomy,
        metadata=metadata,
    )
    taxa_bar_plots_viz.save(OUTPUT_TAXONOMY_VIZ)

except Exception as e:
    print(f"An error occurred during visualization of taxonomic composition: {e}") 
exit(1)
print("Visualization of taxonomic composition for ASV data finished.")