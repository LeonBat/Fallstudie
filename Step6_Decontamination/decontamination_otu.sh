#!/bin/bash

# ==============================================================================
# QIIME 2 Decontamination Pipeline (Step 6)
# This script executes the three-part decontam process using the 'combined' method.
# It uses the filtered OTU table from Step 5.
# ==============================================================================

# --- Configuration Variables ---

# Input files from previous steps (adjust paths if needed)
OTU_TABLE="../Step5_Filtering/otu_table-filtered.qza"
OTU_REP_SEQS="../Step4_QCFeatureTableConstruction/rep-seqs-dn-97.qza"
METADATA_FILE="../Data/metadata.tsv"

# Output files for the contamination artifacts
OUTPUT_SCORES="otu_comb_decontam_scores.qza"
OUTPUT_VIZ="otu_decontam_score_viz.qzv"
OUTPUT_FILTERED_TABLE="otu_table-decontam.qza"
OUTPUT_FILTERED_SEQS="otu_rep_seqs-decontam.qza"

# Decontamination parameters
METHOD="combined"
CONTROL_COL="Sample_or_Control"
CONTROL_VAL="control"
CONC_COL="Concentration"
# IMPORTANT: This is the threshold to distinguish contaminants (p > 0.1)
P_THRESHOLD=0.1 

echo "Starting Decontamination Pipeline (ASV Features)..."
echo "----------------------------------------------------"

# --- Part 1: Identify Contaminant Scores (decontam-identify) ---
echo "1. Calculating Contamination Scores using the Combined method..."

qiime quality-control decontam-identify \
  --i-table "$OTU_TABLE" \
  --m-metadata-file "$METADATA_FILE" \
  --p-method "$METHOD" \
  --p-prev-control-column "$CONTROL_COL" \
  --p-prev-control-indicator "$CONTROL_VAL" \
  --p-freq-concentration-column "$CONC_COL" \
  --o-decontam-scores "$OUTPUT_SCORES"

if [ $? -ne 0 ]; then
  echo "ERROR: Decontam identification failed. Exiting."
  exit 1
fi
echo "   -> Scores saved to $OUTPUT_SCORES"

# --- Part 2: Visualize the Scores (decontam-score-viz) ---
echo ""
echo "2. Generating Score Visualization for Manual Review..."

qiime quality-control decontam-score-viz \
  --i-decontam-scores "$OUTPUT_SCORES" \
  --i-table "$OTU_TABLE" \
  --i-rep-seqs "$OTU_REP_SEQS" \
  --p-threshold "$P_THRESHOLD" \
  --p-no-weighted \
  --p-bin-size 0.05 \
  --o-visualization "$OUTPUT_VIZ"

if [ $? -ne 0 ]; then
  echo "ERROR: Score visualization failed. Exiting."
  exit 1
fi
echo "   -> Visualization saved to $OUTPUT_VIZ"
echo "   *** REVIEW $OUTPUT_VIZ in QIIME 2 View to confirm the threshold ($P_THRESHOLD) ***"

# --- Part 3: Filter Features and Sequences ---
echo ""
echo "3. Filtering Features (ASVs) based on $P_THRESHOLD..."

# Filter the Feature Table: Keep features where p-value is <= 0.1 (not contaminant) OR IS NULL (not tested)
qiime feature-table filter-features \
  --i-table "$OTU_TABLE" \
  --m-metadata-file "$OUTPUT_SCORES" \
  --p-where "[p]<=$P_THRESHOLD OR [p] IS NULL" \
  --o-filtered-table "$OUTPUT_FILTERED_TABLE"

if [ $? -ne 0 ]; then
  echo "ERROR: Feature table filtering failed. Exiting."
  exit 1
fi
echo "   -> Filtered feature table saved to $OUTPUT_FILTERED_TABLE"

echo "4. Filtering Representative Sequences (Rep-Seqs)..."

# Filter the Rep-Seqs to match the new filtered feature table
qiime feature-table filter-seqs \
  --i-data "$OTU_REP_SEQS" \
  --i-table "$OUTPUT_FILTERED_TABLE" \
  --o-filtered-data "$OUTPUT_FILTERED_SEQS"

if [ $? -ne 0 ]; then
  echo "ERROR: Representative sequence filtering failed. Exiting."
  exit 1
fi
echo "   -> Filtered representative sequences saved to $OUTPUT_FILTERED_SEQS"

echo "----------------------------------------------------"
echo "Decontamination pipeline successful. New working files:"
echo "   - Feature Table: $OUTPUT_FILTERED_TABLE"
echo "   - Rep. Sequences: $OUTPUT_FILTERED_SEQS"