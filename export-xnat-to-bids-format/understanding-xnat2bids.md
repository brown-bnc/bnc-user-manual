# Understanding XNAT2BIDS

## Understanding the inputs

Familiarize yourself with the inputs to xnat2bids For a full list of the inputs, you can run:

```text
 xnat2bids --help
```

Some key optional inputs to be aware of:

* `--bidsmap_file`: `xnat2bids` can take a json file with a dictionary of sequence names to correct/change. For instance you can pass `--bidsmap_file ./my_bidsmap.json`. The bidsmaps directory in this repository has examples of bidsmaps file
* `--seqlist`: If you only want to export some sequences from XNAT, you can pass the list \(use order in your XNAT\). e.g., `--seqlist 1 2 3 4 5 7 8 9`
* `--cleanup`: At the end on the process, the source data is avaialable in two directories `root_dir/xnat-export` and `root_dir/bids/sourcedata`. Passing the `--cleanup` flag removes `root_dir/xnat-export`

## Understanding the process

`xnat2bids` performs two main steps:

1. Export to a [Heudiconv](https://github.com/nipy/heudiconv) friendly directory structure. We follow the structure suggested by [the ReproIn guide](https://github.com/ReproNim/reproin), enabling us to use their [heuristic file](https://github.com/nipy/heudiconv/blob/master/heudiconv/heuristics/reproin.py).This step is encapsulated in `xnat_tools/dicom_export.py`
2. We run Heudiconv using ReproIn heuristic. This step is encapsulated in `xnat_tools/run_heudiconv.py`

If you'd like to run those steps separatly, you can do

```text
xnat-dicom-export --user ${xnat_user}  \
--session ${session}                   \
--bids_root_dir ${bids_root_dir}
```

Followed by:

```text
xnat-heudiconv --user ${xnat_user}  \
--session ${session}                \
--bids_root_dir ${bids_root_dir}
```

