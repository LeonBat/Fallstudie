#!usr/bin/env python3

### Script for Differential Abundance testing with ANCOM-BC

# Library
import os
from qiime2 import Artifact, Metadata
import qiime2.plugins.composition.actions as composition_actions
import qiime2.plugins.taxa.actions as taxa_actions

# paths and names
METADATA = os.path.join("../", "Data/", "metadata_for_q.csv")
TABLE = os.path.join("../", "Step6_Decontamination/", "filtered-table.qza")
TAXONOMY = os.path.join("../", "Step9_TaxonomicAnalysis/", "taxonomy.qza")

OUTOUT_ANCOMBC = "ancombc_results.qza"
OUTPUT_ANCOMBC_DISEASE_VIZ = "ancombc_disease_barplot.qzv"
OUTPUT_ANCOMBC_TOOTH_VIZ = "ancombc_tooth_barplot.qzv"

# Running ANCOM-BC

print("=============================================")
print("1.Running ANCOM-BC for Differential Abundance Testing")
print("=============================================")

#Loading  artifact
print("Loading artifacts...")
try:
    table = Artifact.load(TABLE)
    metadata = Metadata.load(METADATA)
except Exception as e:
    print(f"An error occurred while loading artifacts: {e}")
    exit(1)

try:
    ancombc_subject, = composition_actions.ancombc(
        table=table,
        metadata=metadata,
        formula='disease_state',
    )
    da_barplot_subject_viz, = composition_actions.da_barplot(
        data=ancombc_subject,
        significance_threshold=0.001,
    )


except Exception as e:
    print("ANCOM-BC failed:", e)
    exit(1)

#saving results
ancombc_subject.save(OUTOUT_ANCOMBC)
print("ANCOM-BC completed successfully without collapsing.")

# Collapsing test at specific taxonomic level

print("=============================================")
print("2.Collapsing ANCOM-BC results at Genus level")
print("=============================================")

print("Collapsing to Genus level...")

print("Loading taxonomy artifact...")
try:
    taxonomy = Artifact.load(TAXONOMY)
except Exception as e:
    print(f"An error occurred while loading taxonomy artifact: {e}")
    exit(1)


print("Collapsing table to Genus level and running ANCOM-BC with disease state...")
try:
    table_genus, = taxa_actions.collapse(
    table=table,
    taxonomy=taxonomy,
    level=6,
    )
    l6_ancombc_subject, = composition_actions.ancombc(
        table=table_genus,
        metadata=metadata,
        formula='disease_state',
        reference_levels=['disease_state::healthy'],
    )
    l6_da_barplot_subject_viz, = composition_actions.da_barplot(
        data=l6_ancombc_subject,
        significance_threshold=0.05,
        
    )
except Exception as e:
    print("Collapsing to Genus level failed:", e)
    exit(1)

#saving visualization
l6_da_barplot_subject_viz.save(OUTPUT_ANCOMBC_DISEASE_VIZ)
print("Collapsing to Genus level completed successfully.")



print("Collapsing table to Genus level and running ANCOM-BC with tooth site...")
try:
    table_genus, = taxa_actions.collapse(
    table=table,
    taxonomy=taxonomy,
    level=6,
    )
    l6_ancombc_subject, = composition_actions.ancombc(
        table=table_genus,
        metadata=metadata,
        formula='Type',
    )
    l6_da_barplot_subject_viz, = composition_actions.da_barplot(
        data=l6_ancombc_subject,
        significance_threshold=0.05,
    )
except Exception as e:
    print("Collapsing to Genus level failed:", e)
    exit(1)


#saving visualization
l6_da_barplot_subject_viz.save(OUTPUT_ANCOMBC_TOOTH_VIZ)
print("Collapsing to Genus level completed successfully.")


