#!usr/bin/env python3

### Phylogenetic Tree Construction for ASV Data


#Libraries
from qiime2 import Artifact
import qiime2.plugins.phylogeny.actions as phylogeny_actions
import os


##### ASV Phylogenetic Tree Construction
# Define file paths
rep_seqs_path = os.path.join("../", "Step6_Decontamination", "filtered-rep-seqs.qza")
if not os.path.exists(rep_seqs_path):
    raise FileNotFoundError(f"Please check again the path to the representative sequences: {rep_seqs_path}")



# Run phylogenetic tree construction
try:
    print("Constructing phylogenetic tree for ASV representative sequences...")
    rep_seqs = Artifact.load(rep_seqs_path)
    asv_aligned_rep_seqs, asv_masked_aligned_rep_seqs, asv_unrooted_tree, asv_rooted_tree = phylogeny_actions.align_to_tree_mafft_fasttree(
        sequences=rep_seqs,
    )
except Exception as e:
    print(f"An error occurred during phylogenetic tree construction: {e}")

#Saving the rooted tree
print("Saving asv_rooted_tree.qza...")
asv_rooted_tree.save(os.path.join( "asv_rooted_tree.qza"))

print("Constructing phylogenetic tree finished")



##### OTU phylogenetic Tree Construction
# Define file paths
# rep_seqs_path = os.path.join("../", "Step6_Decontamination", "otu_rep_seqs-decontam.qza")
# if not os.path.exists(rep_seqs_path):
#     raise FileNotFoundError(f"Please check again the path to the representative sequences: {rep_seqs_path}")



# # Run phylogenetic tree construction
# try:
#     print("Constructing phylogenetic tree for OTU representative sequences...")
#     rep_seqs = Artifact.load(rep_seqs_path)
#     otu_aligned_rep_seqs, otu_masked_aligned_rep_seqs, otu_unrooted_tree, otu_rooted_tree = phylogeny_actions.align_to_tree_mafft_fasttree(
#         sequences=rep_seqs,
#     )
# except Exception as e:
#     print(f"An error occurred during phylogenetic tree construction: {e}")



# print("Constructing phylogenetic tree finished")