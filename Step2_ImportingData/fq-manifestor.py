#!/usr/bin/env python

import glob
import os.path
import re 
import sys
import subprocess
import shlex

def fq_manifestor(input_dir,
                  output_fp,
                  fq_extensions=['fastq.gz', 'fq.gz'],
                  split_pattern='_',
                  f_read_pattern='_1.',
                  r_read_pattern='_2.',
                  filter_pattern=None,
                  verbose=True):

    input_dir = os.path.abspath(input_dir)
    if verbose: print("Searching directory: %s" % input_dir)

    fq_filepaths = []
    for fq_extension in fq_extensions:
        fq_filepaths += glob.glob('%s/**/*.%s' % (input_dir, fq_extension),
                                 recursive = True)
    if filter_pattern is not None:
        fq_filepaths = [fp for fp in fq_filepaths if filter_pattern in fp]

    n_fq_filepaths = len(fq_filepaths)
    if verbose: print('Found %d fastq files.' % n_fq_filepaths)

    sids_to_fps = {}

    for fq_filepath in fq_filepaths:
        fq_filename = os.path.basename(fq_filepath)
        sid_fields = re.split(split_pattern, fq_filename)

        if len(sid_fields) == 1:
            raise ValueError('Sample ID not found in file: %s' % fq_filepath)
        else:
            sid = sid_fields[0]

        if bool(re.search(f_read_pattern, fq_filename)):
            forward = True
            reverse = False
        elif bool(re.search(r_read_pattern, fq_filename)):
            forward = False
            reverse = True
        else:
            raise ValueError('Forward/reverse patterns not found in file: %s' % fq_filepath)

        try:
            sid_fps = sids_to_fps[sid]
        except KeyError:
            sid_fps = [None, None]

        if forward:
            sid_fps[0] = fq_filepath
        else:
            sid_fps[1] = fq_filepath
        sids_to_fps[sid] = sid_fps

    lines = ['sample-id\tforward-absolute-filepath\treverse-absolute-filepath']
    for sid, (fwd_fq_filepath, rev_fq_filepath) in sids_to_fps.items():
        if fwd_fq_filepath is None:
            raise ValueError('Missing forward read for sample: %s' % sid)

        if rev_fq_filepath is None:
            raise ValueError('Missing reverse read for sample: %s' % sid)

        lines.append('%s\t%s\t%s' % (sid, fwd_fq_filepath, rev_fq_filepath))

    if (len(lines) - 1) != (n_fq_filepaths / 2) and verbose:
        print("\n** WARNING**: "
              "The number of manifest records doesn't align with the number of "
              "fastq files that were found. It's possible that the match "
              "patterns aren't working correctly for your files. These can "
              "be customized when using the API.\n")

    with open(output_fp, 'w') as of:
        of.write('\n'.join(lines))
        of.write('\n')

# --- EXECUTION BLOCK ---
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('USAGE: python fq_manifestor.py input-directory output-filepath')
        sys.exit(1)

    input_dir = sys.argv[1]
    output_fp = sys.argv[2]
    output_fp_abs = os.path.abspath(output_fp)
    
# 1. CHECK FOR EXISTING MANIFEST FILE
    if os.path.exists(output_fp_abs):
        print(f"✅ Manifest file already exists at: {output_fp_abs}")
        print("Skipping manifest generation and proceeding directly to QIIME 2 import.")
    else:
        # 2. Generate the manifest file if it doesn't exist
        print("Manifest file not found. Starting generation...")
        try:
            fq_manifestor(input_dir, output_fp) 
            print(f"Successfully created manifest file: {output_fp_abs}")
        except Exception as e:
            print(f"❌ ERROR: Manifest generation failed. Details: {e}")
            sys.exit(1)

# 2. Define and execute the QIIME 2 import command
    print("--- Running QIIME 2 Import ---")

    qiime_command = (
        f"qiime tools import "
        f"--type 'SampleData[PairedEndSequencesWithQuality]' "
        f"--input-path {output_fp_abs} "
        f"--output-path demux.qza "
        f"--input-format PairedEndFastqManifestPhred33V2"
    )

    print(f"Executing: {qiime_command}")
    
    try:
        # Use shlex.split to correctly handle spaces and arguments
        subprocess.run(shlex.split(qiime_command), check=True)
        print("\n✅ Successfully imported data! Artifact saved as demux.qza.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERROR: QIIME 2 import failed.")
        print(f"Check your manifest file paths and QIIME 2 environment.")
        print(f"Details: {e}")
        sys.exit(1)

# in command line: python fq_manifestor.py ~/Fallstudie/20241209-raw_data fastq-manifest.tsv