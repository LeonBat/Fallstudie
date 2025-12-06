# Libraries
from qiime2 import Artifact
from qiime2 import Metadata
import qiime2.plugins.feature_classifier.actions as feature_classifier_actions
import qiime2.plugins.taxa.actions as taxa_actions
import os
from urllib.request import urlretrieve # Used for downloading the classifier file

# --- Configuration and Path Setup ---

# paths and names
READS = os.path.join("../", "Step4_QCFeatureTableConstruction/", "rep-seqs.qza") # Corrected to rep-seqs.qza
METADATA = os.path.join("../", "Data/", "metadata_for_q.csv")
# Note: Using 'filtered-table.qza' as specified by user, assuming this is the final decontaminated table
TABLE = os.path.join("../", "Step6_Decontamination/", "filtered-table.qza") 

CLASSIFIER_FN = "gg-13-8-99-515-806-nb-classifier.qza"
CLASSIFIER_URL = "https://s3.amazonaws.com/qiime2-data/gg/gg-13-8-99-515-806-nb-classifier.qza" # Corrected URL to be standard QIIME 2 endpoint

OTUPUT_TAXONOMY = "taxonomy.qza"
OUTPUT_TAXONOMY_VIZ = "taxonomy.qzv"

# Initialize variables for global scope (FIXED)
taxonomy = None 
taxonomy_results = None

# --- 1. Getting classifier from URL ---

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


# --- 2. Running taxonomic classification and visualization ---

print("=============================================")
print("Running taxonomic classification for ASV data...")
print("=============================================")

# Input Check and Loading
files = [READS, TABLE, METADATA, CLASSIFIER_FN]
try:
    for file in files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Required file not found: {file}")
            
    print("Loading input artifacts...")
    gg_13_8_99_515_806_nb_classifier = Artifact.load(CLASSIFIER_FN)
    reads_artifact = Artifact.load(READS)
    table_artifact = Artifact.load(TABLE)
    metadata_obj = Metadata.load(METADATA)
    print("Artifacts loaded successfully.")
    
except Exception as e:
    print(f"An error occurred while loading artifacts: {e}")
    exit(1)


# 2a. Run Classification
print("Running classify sklearn...")
try:
    # taxonomy is now the variable that holds the artifact object
    taxonomy_results, = feature_classifier_actions.classify_sklearn(
        classifier=gg_13_8_99_515_806_nb_classifier,
        reads=reads_artifact, # Pass the loaded object (FIXED)
    )
    taxonomy_results.save(OTUPUT_TAXONOMY)
    print(f"Taxonomy classification completed. Artifact saved to {OTUPUT_TAXONOMY}")

except Exception as e:
    print(f"An error occurred during taxonomic classification: {e}")
    exit(1) # CRITICAL FIX: Exit here if classification fails!


# 2b. Visualizing the results
print("==============================================")
print("Visualizing taxonomic composition for ASV data...")
print("==============================================")

try:
    taxa_bar_plots_viz, = taxa_actions.barplot(
        table=table_artifact,
        taxonomy=taxonomy_results, # Use the defined variable
        metadata=metadata_obj, # Use the loaded object
    )
    taxa_bar_plots_viz.save(OUTPUT_TAXONOMY_VIZ)
    print(f"Output visualization saved to {OUTPUT_TAXONOMY_VIZ}")

except Exception as e:
    print(f"An error occurred during visualization of taxonomic composition: {e}") 
    exit(1)

print("\nTaxonomy analysis script completed successfully.")