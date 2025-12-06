#Libraries

from qiime2 import Artifact
from qiime2 import Metadata
import qiime2.plugins.demux.actions as demux_actions

#Fetching data
fn = '../Step2_ImporingData/demux.qza'
sequences = Artifact.load(fn)

fn = '../Data/metadata.tsv'
sample_metadata_md = Metadata.load(fn)

metadata_column_mdc = sample_metadata_md.get_column('barcode-sequence')
demux, demux_details = demux_actions.emp_single(
    seqs=sequences,
    barcodes=metadata_column_mdc,
)