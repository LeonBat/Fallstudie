# Case Study: 16S Microbiome Analysis (EOTRH)

This repository documents the bioinformatic pipeline used for the analysis of 16S rRNA amplicon data (V3-V4 region) within the scope of a case study on EOTRH (Equine Odontoclastic Tooth Resorption and Hypercementosis). The analysis was conducted using **QIIME 2** (Version 2025.10) via the Python Artifact API and Bash scripting.

## Project Overview

The objective of this workflow is the reproducible processing of paired-end sequencing data, ranging from metadata preparation to differential abundance testing.

---

## Workflow & Scripts

The analysis is divided into 10 distinct steps. The Python (`.py`) and Bash (`.sh`) scripts corresponding to each step are located in the corresponding step folders.

### 1. Metadata Preparation
* **Script:** `metadata_tabulate.py`
* **Description:** Formats and tabulates the sample metadata into a QIIME 2 visualization (`tabulated_metadata.qzv`) for inspection.

### 2. Data Import
* **Script:** `fq_manifestor.py`
* **Description:** Generates a manifest file from the raw data directory and imports the FASTQ files into a QIIME 2 artifact (`demux.qza`) using the `PairedEndFastqManifestPhred33V2` format.

### 3. Demultiplexing
* **Script:** `demultiplexing.py`
* **Description:** Demultiplexes sequences (if applicable/required) using `emp_single` based on barcode sequences defined in the metadata.

### 4. QC Feature Table Construction (DADA2 & VSEARCH)
* **Scripts:**  `dada2.py`: Performs denoising, quality filtering, and merging (Trim: 15 bp; Truncate: 280/240 bp).
    * `vsearch.py`: Clusters ASVs into OTUs at 97% identity.
    * `featuretable_summary_asv.py` & `featuretable_summary_otu.py`: Generates summary visualizations for both ASV and OTU tables.

### 5. Feature Filtering
* **Script:** `filtering.py`
* **Description:** Filters the ASV and OTU tables to retain only features present in at least 2 samples, removing singleton/rare noise.

### 6. Decontamination
* **Scripts:** `decontamination_asv.sh` & `decontamination_otu.sh`
* **Description:** Identifies and removes contaminants using the `q2-quality-control` plugin.
    * **ASV:** Uses the "prevalence" method (comparing to H2O controls).
    * **OTU:** Uses the "combined" method (prevalence + concentration).

### 7. Phylogenetic Tree & Diversity Analysis
* **Scripts:**  `phylogenetic_tree.py`: Constructs a rooted phylogenetic tree using MAFFT alignment and FastTree.
    * `diversity_analysis.py` & `alphabetaanalysis.py`: Calculates core diversity metrics (Faith's PD, Shannon, UniFrac, Bray-Curtis) and generates PCoA plots (Emperor) and group significance tests (PERMANOVA).

### 8. Alpha Rarefaction
* **Script:** `alpha_rarefactioning.py`
* **Description:** Generates alpha rarefaction curves to determine the optimal sampling depth for diversity analysis (retaining maximum diversity while normalizing library sizes).

### 9. Taxonomic Analysis
* **Scripts:** `taxonomy.py` & `taxonomy_refined.py`
* **Description:** Classifies representative sequences using a Naive Bayes classifier trained on reference databases (e.g., Greengenes). Includes visualization of taxonomic bar plots.

### 10. Abundance Analysis (ANCOM-BC)
* **Script:** `abundance.py`
* **Description:** Performs differential abundance testing using **ANCOM-BC** to identify taxa significantly associated with disease states. Includes collapsing features to the Genus level (L6) before testing.

---
