#! usr/bin/env python3

#### Diversity Analysis Script

from qiime2 import Artifact
import qiime2.plugins.diversity.actions as diversity_actions
import qiime2.plugins.emperor.actions as emperor_actions

import os


#### ASV Diversity Analysis

# Define files and names
PHYLOGENY_TREE = os.path.join("asv_rooted_tree.qza")
TABLE = os.path.join("../", "Step6_Decontamination", "filtered-table.qza")
SAMPLING_DEPTH = 9000 # according to table summary we exclude not many samples (<25%) by this threshold
METADATA = os.path.join("../", "Data", "metadata_for_q.csv")
DIVERSITY_OUTPUT_DIR = "core_diversity_results"


ALPHA_OUTPUT_PREFIX = os.path.join(DIVERSITY_OUTPUT_DIR, "alpha_group_significance")
BETA_OUTPUT_PREFIX = os.path.join(DIVERSITY_OUTPUT_DIR, "beta_group_significance")

#checking if files exist or are found
files = [PHYLOGENY_TREE, TABLE, METADATA]
try:
    missing_files = [path for path in files if not os.path.exists(path)]
    if missing_files:
        raise FileNotFoundError(f"Missing files: {missing_files}")
except FileNotFoundError as e:
    print(e)


#defining saving function
def save_artifact(results, prefix):
    '''
    This function saves the artifacts from diversity analysis to specified output directory.
    '''
    print(f"Saving artifacts to disk with prefix: {prefix}")
    for name, artifact in results._asdict().items():
        if isinstance(artifact, Artifact):
            artifact.save(os.path.join(prefix, f"{name}.qza"))
        elif visualization := getattr(artifact, 'visualization', None):
            visualization.save(os.path.join(prefix, f"{name}.qzv"))

# executing diversity analysis
print("============================================")
print("1.Starting diversity analysis for ASV data...")
print("============================================")

try:
    action_results = diversity_actions.core_metrics_phylogenetic(
        phylogeny=Artifact.load(PHYLOGENY_TREE),
        table=Artifact.load(TABLE),
        sampling_depth=SAMPLING_DEPTH,
        metadata = METADATA,
    )

    rarefied_table = action_results.rarefied_table
    faith_pd_vector = action_results.faith_pd_vector
    observed_features_vector = action_results.observed_features_vector
    shannon_vector = action_results.shannon_vector
    evenness_vector = action_results.evenness_vector
    unweighted_unifrac_distance_matrix = action_results.unweighted_unifrac_distance_matrix
    weighted_unifrac_distance_matrix = action_results.weighted_unifrac_distance_matrix
    jaccard_distance_matrix = action_results.jaccard_distance_matrix
    bray_curtis_distance_matrix = action_results.bray_curtis_distance_matrix
    unweighted_unifrac_pcoa_results = action_results.unweighted_unifrac_pcoa_results
    weighted_unifrac_pcoa_results = action_results.weighted_unifrac_pcoa_results
    jaccard_pcoa_results = action_results.jaccard_pcoa_results
    bray_curtis_pcoa_results = action_results.bray_curtis_pcoa_results
    unweighted_unifrac_emperor_viz = action_results.unweighted_unifrac_emperor
    weighted_unifrac_emperor_viz = action_results.weighted_unifrac_emperor
    jaccard_emperor_viz = action_results.jaccard_emperor
    bray_curtis_emperor_viz = action_results.bray_curtis_emperor

except Exception as e:
    print(f"An error occurred during diversity analysis: {e}")

print("Finished  calculating diverstiy metrics succesfulley")


print("============================================")
print("2.Testing for associations between categorical metadata columns and alpha diversity data")
print("============================================")

print("Testing Faith's PD...")

try:
    faith_pd_group_significance_viz, = diversity_actions.alpha_group_significance(
        alpha_diversity = faith_pd_vector,
        metadata = METADATA,
    )

    eveness_group_significance_viz, = diversity_actions.alpha_group_significance(
        alpha_diversity = evenness_vector,
        metadata = METADATA,
    )

except Exception as e:
    print(f"An error occurred during alpha diversity group significance testing: {e}")

print("Finished testing for associations with categorical metadata columns")


print("============================================")
print("3.Analyzing beta diversity differences with PERMANOVA")
print("============================================")

print("Running PERMANOVA on Unweighted UniFrac...")

try:
    disease_state_mdc = sample_metadata_md.get_column('disease_state')
    unweighted_unifrac_disease_state_group_significance_viz, = diversity_actions.beta_group_significance(
    distance_matrix=unweighted_unifrac_distance_matrix,
    metadata=disease_state_mdc,
    pairwise=True,
    )
    horse_mdc = sample_metadata_md.get_column('Horse')
    unweighted_unifrac_horse_group_significance_viz, = diversity_actions.beta_group_significance(
        distance_matrix=unweighted_unifrac_distance_matrix,
        metadata=horse_mdc,
        pairwise=True,
    )
except Exception as e:
    print(f"An error occurred during beta diversity group significance testing: {e}")

print("Finished PERMANOVA analysis on beta diversity metrics")



print("=============================================")
print("4.Ordination for exploring microbial community composition")
print("=============================================")

print("Generating Emperor plots for Unweighted UniFrac...")

try:
    unweighted_unifrac_emperor_days_since_experiment_start_viz, = emperor_actions.plot(
        pcoa=unweighted_unifrac_pcoa_results,
        metadata= METADATA,
    )
    bray_curtis_emperor_days_since_experiment_start_viz, = emperor_actions.plot(
        pcoa=bray_curtis_pcoa_results,
        metadata= METADATA,
    )

except Exception as e:
    print(f"An error occurred during Emperor plot generation: {e}")
print("Finished generating Emperor plots for ordination analysis")


print("Diversity analysis script completed.")
