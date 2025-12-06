#### Alpha Rarefactioning Script

#Libraries
from qiime2 import Artifact
import qiime2.plugins.diversity.actions as diversity_actions
from qiime2 import Metadata
import os

# paths and names
TABLE = os.path.join("../", "Step6_Decontamination", "filtered-table.qza")
TREE = os.path.join("../", "Step7_PhylogeneticTree", "asv_rooted_tree.qza")
METADATA = os.path.join("../", "Data", "metadata_for_q.csv")

OUTPUT_VIZ_FILE = "asv_alpha_rarefaction.qzv"
# Execution of Alpha Rarefactioning
# Creation of function between alpha diversity and sampling depth
# using the qimme diversity alpha-rarefaction visualizer


print("============================================== ")
print("  Starting Alpha Rarefactioning Process...   ")
print("============================================== ")

files = [TABLE, TREE, METADATA]
for file in files:
    if not os.path.exists(file):
        raise FileNotFoundError(f"Required file not found: {file}")


#Loading artifacts
try:    
    print("Loading input artifacts...")
    table_artifact = Artifact.load(TABLE)
    tree_artifact = Artifact.load(TREE)
    metadata_obj = Metadata.load(METADATA)
    print("Artifacts loaded successfully.")
except Exception as e:
    print(f"An error occurred while loading artifacts: {e}")
    exit(1)

try:
    alpha_rarefaction_viz, = diversity_actions.alpha_rarefaction(
    table=table_artifact,
    phylogeny=tree_artifact,
    max_depth=13000, #choosing value close to median (recommended in tutorial)
    metadata=metadata_obj,
)
except Exception as e:
    print(f"An error occurred during alpha rarefactioning: {e}")

print("Alpha rarefactioning completed successfully.")

# Saving the output visualization
alpha_rarefaction_viz.save(OUTPUT_VIZ_FILE)
print(f"Output visualization saved to {OUTPUT_VIZ_FILE}")


print("Finished calculating diversity metrics successfulley.")
print(f"Interactive visualization saved to: {OUTPUT_VIZ_FILE}")
print("Review this file to select the final sampling depth for Step 7.1 (Core Metrics).")
