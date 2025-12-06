# Libraries
from qiime2 import Artifact, Metadata
import qiime2.plugins.diversity.actions as diversity_actions
import qiime2.plugins.emperor.actions as emperor_actions
import os

# --- Configuration and Path Setup ---

# Define working directories
STEP6_DIR = os.path.join("..", "Step6_Decontamination")
DIVERSITY_OUTPUT_DIR = "core_diversity_results"

# Input files (Must use the final, decontaminated names)
PHYLOGENY_TREE = "asv_rooted_tree.qza" 
# Corrected name: This must match the output of the final decontamination step
TABLE = os.path.join(STEP6_DIR, "filtered-table.qza") 
METADATA = os.path.join("..", "Data", "metadata_for_q.csv") 

# Parameters
SAMPLING_DEPTH = 9000 #chosen rarefaction depth based on table summary
ALPHA_OUTPUT_PREFIX = os.path.join(DIVERSITY_OUTPUT_DIR, "alpha_group_significance")
BETA_OUTPUT_PREFIX = os.path.join(DIVERSITY_OUTPUT_DIR, "beta_group_significance")


# --- Utility Functions ---

def ensure_dir(path):
    """Ensures the output directory exists."""
    os.makedirs(path, exist_ok=True)

def save_artifacts(results, prefix):
    """Saves artifacts in a NamedTuple result object."""
    print(f"Saving artifacts to disk with prefix: {prefix}")
    for name, artifact in results._asdict().items():
        if isinstance(artifact, Artifact):
            artifact.save(os.path.join(prefix, f"{name}.qza"))
        elif visualization := getattr(artifact, 'visualization', None):
            visualization.save(os.path.join(prefix, f"{name}.qzv"))


# --- Execution ---
print("============================================")
print("1. Initializing Diversity Analysis for ASV Data...")
print("============================================")

# 1. Load Metadata and check inputs
try:
    ensure_dir(DIVERSITY_OUTPUT_DIR)
    
    # 1a. Load Metadata Object (Crucial Fix)
    metadata_obj = Metadata.load(METADATA)
    
    # 1b. Check and Load Artifacts
    if not all(os.path.exists(p) for p in [PHYLOGENY_TREE, TABLE]):
        raise FileNotFoundError("One or more input artifacts not found. Check Step 6 and 7 paths.")
        
    rooted_tree_art = Artifact.load(PHYLOGENY_TREE)
    table_art = Artifact.load(TABLE)

except Exception as e:
    print(f"ERROR during setup: {e}")
    exit(1)


# 2. Execute Core Metrics Phylogenetic
print(f"Executing core_metrics_phylogenetic at depth: {SAMPLING_DEPTH}...")
try:
    # Pass the loaded metadata object to the action
    action_results = diversity_actions.core_metrics_phylogenetic(
        phylogeny=rooted_tree_art,
        table=table_art,
        sampling_depth=SAMPLING_DEPTH,
        metadata=metadata_obj, # Use the loaded Metadata object
    )
    
    # Save all 14 core metrics results
    core_metrics_prefix = os.path.join(DIVERSITY_OUTPUT_DIR, "core_metrics")
    ensure_dir(core_metrics_prefix)
    save_artifacts(action_results, core_metrics_prefix)

except Exception as e:
    print(f"An error occurred during core metrics calculation: {e}")
    exit(1)
print("Finished calculating diversity metrics successfully.")


# 3. Alpha Diversity Group Significance (e.g., Kruskal-Wallis Test)
print("============================================")
print("2. Testing for associations between metadata and alpha diversity data")
print("============================================")

try:
    # Use the Faith PD and Evenness artifacts generated in action_results
    faith_pd_vector = Artifact.load(os.path.join(core_metrics_prefix, "faith_pd_vector.qza"))
    evenness_vector = Artifact.load(os.path.join(core_metrics_prefix, "evenness_vector.qza"))
    
    # Test Faith's PD
    faith_pd_significance = diversity_actions.alpha_group_significance(
        alpha_diversity=faith_pd_vector,
        metadata=metadata_obj,
    )
    faith_pd_significance.visualization.save(f"{ALPHA_OUTPUT_PREFIX}_faith_pd.qzv")
    
    # Test Evenness
    evenness_significance = diversity_actions.alpha_group_significance(
        alpha_diversity=evenness_vector,
        metadata=metadata_obj,
    )
    evenness_significance.visualization.save(f"{ALPHA_OUTPUT_PREFIX}_evenness.qzv")

except Exception as e:
    print(f"An error occurred during alpha diversity group significance testing: {e}")
    # Continue execution even if alpha testing fails, as beta and ordination may still be fine

print("Finished testing for associations with categorical metadata columns")

# 4. Beta Diversity Group Significance (PERMANOVA)
print("============================================")
print("3. Analyzing beta diversity differences with PERMANOVA")
print("============================================")

try:
    # Use the Unweighted UniFrac distance matrix generated in action_results
    unweighted_unifrac_dm = Artifact.load(os.path.join(core_metrics_prefix, "unweighted_unifrac_distance_matrix.qza"))
    
    # --- Test 1: disease_state (Categorical) ---
    print("Running PERMANOVA on Unweighted UniFrac for 'disease_state'...")
    unweighted_unifrac_disease_state_viz, = diversity_actions.beta_group_significance(
        distance_matrix=unweighted_unifrac_dm,
        # FIX: Correct API usage to get the metadata column object
        metadata=metadata_obj.get_column('disease_state'), 
        pairwise=True,
    )
    unweighted_unifrac_disease_state_viz.save(f"{BETA_OUTPUT_PREFIX}_unweighted_unifrac_disease_state.qzv")

    # --- Test 2: Horse (Categorical) ---
    print("Running PERMANOVA on Unweighted UniFrac for 'Horse'...")
    unweighted_unifrac_horse_viz, = diversity_actions.beta_group_significance(
        distance_matrix=unweighted_unifrac_dm,
        # FIX: Correct API usage to get the metadata column object
        metadata=metadata_obj.get_column('Horse'), 
        pairwise=True,
    )
    unweighted_unifrac_horse_viz.save(f"{BETA_OUTPUT_PREFIX}_unweighted_unifrac_horse.qzv")

except Exception as e:
    print(f"An error occurred during beta diversity group significance testing: {e}")
    exit(1)
print("Finished PERMANOVA analysis on beta diversity metrics")


# 5. Ordination for exploring microbial community composition (Emperor)
print("=============================================")
print("4. Ordination for exploring microbial community composition")
print("=============================================")

try:
    # Use the PCoA results generated in action_results
    unweighted_unifrac_pcoa = Artifact.load(os.path.join(core_metrics_prefix, "unweighted_unifrac_pcoa_results.qza"))
    bray_curtis_pcoa = Artifact.load(os.path.join(core_metrics_prefix, "bray_curtis_pcoa_results.qza"))

    # Generate Emperor plots (which use the full metadata object)
    print("Generating Emperor plot for Unweighted UniFrac...")
    unweighted_unifrac_emperor_viz, = emperor_actions.plot(
        pcoa=unweighted_unifrac_pcoa,
        metadata=metadata_obj, # Pass the full metadata object
    )
    unweighted_unifrac_emperor_viz.save(os.path.join(DIVERSITY_OUTPUT_DIR, "emperor_unweighted_unifrac.qzv"))

    print("Generating Emperor plot for Bray-Curtis...")
    bray_curtis_emperor_viz, = emperor_actions.plot(
        pcoa=bray_curtis_pcoa,
        metadata=metadata_obj, # Pass the full metadata object
    )
    bray_curtis_emperor_viz.save(os.path.join(DIVERSITY_OUTPUT_DIR, "emperor_bray_curtis.qzv"))

except Exception as e:
    print(f"An error occurred during Emperor plot generation: {e}")
    exit(1)
print("Finished generating Emperor plots for ordination analysis")


print("\nDiversity analysis script completed successfully.")