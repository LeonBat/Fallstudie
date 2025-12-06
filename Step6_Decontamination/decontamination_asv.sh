#!/bin/bash

set -e
# ==============================================================================
# QIIME 2 Decontamination Pipeline (Step 6)
# This script executes the three-part decontam process using the 'combined' method.
# It uses the filtered ASV table from Step 5.
# ==============================================================================

# --- Configuration Variables ---

TABLE="../Step5_Filtering/asv_table-filtered.qza"
METADATA="../Data/metadata_for_q.csv"
METHOD="prevalence"
PREV_CONTROL_COLUMN="Horse"
PREV_CONTROL_INDICATOR="H2O"
DECONTAM_SCORES="asv_decontam_scores.qza"


# --- Step 1: Identify Contaminants ---

echo "==========================================================================="
echo "1. Identifying contaminants using prevalence method.."
echo "==========================================================================="

qiime quality-control decontam-identify \
  --i-table $TABLE \
  --m-metadata-file $METADATA \
  --p-method $METHOD \
  --p-prev-control-column $PREV_CONTROL_COLUMN \
  --p-prev-control-indicator $PREV_CONTROL_INDICATOR \
  --o-decontam-scores $DECONTAM_SCORES
echo "Decontamination Step 1 complete: Contaminants identified."



# --- Step 2: Decontam Score Viz

echo "==========================================================================="
echo "2. Generating decontam score visualization.."
echo "==========================================================================="


# --- Decontamination Variables ---
REP_SEQS="../Step4_QCFeatureTableConstruction/rep-seqs.qza"
TRESHOLD=0.1
BINSIZE=0.05
VISUALIZATION="asv_decontam_score_viz.qzv"

qiime quality-control decontam-score-viz \
  --i-decontam-scores "$DECONTAM_SCORES" \
  --i-table "$TABLE" \
  --i-rep-seqs "$REP_SEQS" \
  --p-threshold "$TRESHOLD" \
  --p-bin-size "$BINSIZE" \
  --o-visualization "$VISUALIZATION"
echo "Decontamination Step 2 complete: Decontam score visualization generated."


# --- Step 3: Filter Contaminants ---
echo "==========================================================================="
echo "3. Filtering contaminants from ASV table.."
echo "==========================================================================="


#--- Filtering Variables ---
FILTERED_REP_SEQS="filtered-rep-seqs.qza"
FILTERED_TABLE="filtered-table.qza"

qiime feature-table filter-features \
  --i-table "$TABLE" \
  --m-metadata-file "$DECONTAM_SCORES" \
  --p-where '[p]>0.1 OR [p] IS NULL' \
  --o-filtered-table "$FILTERED_TABLE"

qiime feature-table filter-seqs \
  --i-data "$REP_SEQS" \
  --i-table "$FILTERED_TABLE" \
  --o-filtered-data "$FILTERED_REP_SEQS"
echo "Decontamination Step 3 complete: Contaminants filtered from ASV table."


echo "==========================================================================="
echo "Decontamination process completed successfully."
echo "==========================================================================="