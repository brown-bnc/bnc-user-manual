# Running xnat2bids with a custom configuration

Open a new file in your favorite text editor, and save it as something ending in **.toml** like x2b\_my\_first\_config.toml.

{% hint style="info" %}
To open VSCode in an interactive desktop, open a terminal with a right click followed by selecting 'Open Terminal Here".  Next, run the command: **`module load vscode`**

To launch VSCode, run **`code`** on the command line.
{% endhint %}

### 1. Configure slurm parameters

First, let's configure a couple of slurm arguments; paste the following into your .toml file:

```toml
[slurm-args]
mail-user = "example-user@brown.edu"
mail-type = "ALL"
```

Update the value of `example-user` to be your e-mail. This will allow you to receive notifications on the status of your jobs!

For further details on all available slurm parameter options, see Slurm's documentation here: [https://slurm.schedmd.com/sbatch.html](https://slurm.schedmd.com/sbatch.html)

{% hint style="info" %}
**NOTE:** By default, SBATCH output logs will be located at: `~/scratch/logs/`

If you would like your logs to live somewhere else, update your configuration as follows:

```toml
[slurm-args]
output="/path/to/logs/dir/%x-%J.txt"
```
{% endhint %}

### 2. Configure xnat2bids parameters

Next, you'll need to configure what arguments to pass to `xnat2bids`, such as the session (or comma-separated list of sessions) you would like to process, as well as any other arguments.

<details>

<summary>💡Click here for a comprehensive list of all available options</summary>

{% code overflow="wrap" %}
```
project TEXT: Project ID from XNAT

subjects LIST[TEXT]: List of one or more subjects. Corresponds with the "last name" provided when registering the participant on the scanner, which becomes the "subject" ID on XNAT. If subjects parameter is specified, project must also be specified.

sessions LIST[TEXT]: List of one or more Accession #s found on XNAT

bids_root TEXT: Root output directory for exporting the files [default: ~/bids-export/]

version TEXT: Version of xnat-tools [default: latest]

host TEXT: XNAT's URL [default: https://xnat.bnc.brown.edu]

bidsmap-file TEXT: Bidsmap JSON file to correct sequence names

dicomfix-config TEXT: JSON file listing DICOM fields to correct for each specified sequence. USE WITH CAUTION

includeseq LIST[INTEGERS or STRINGS]: Include this sequence(s) only

skipseq LIST[INTEGERS or STRINGS]: Exclude this sequence(s) from processing

log-id TEXT: ID or suffix to append to logfile. If empty, current date is used [default: current date - MM-DD-YYYY-HH-MM-SS]

verbose INTEGER: Verbose level, from 0 (quiet) to 2 (most verbose) [default: 0]

overwrite BOOLEAN: Remove directories where prior results for this session/participant [default: false]

export-only BOOLEAN: Export DICOM data from XNAT without BIDS conversion [default: false]

skip-export BOOLEAN: Skip DICOM export and initiate BIDS conversion [default: false]

validate_frames BOOLEAN: Use if you manually terminate your fMRI runs. If the final volume does not contain the expected number of slices, the associated DICOM file(s) will be deleted.
```
{% endcode %}



</details>

For this demo, paste the following text into your config file:

```toml
[xnat2bids-args]
sessions = ["XNAT_E00080", "XNAT_E00114", "XNAT_E00152"]
skipseq=["anat-t1w_acq-memprage"]
```

Here, we are setting the sessions to be processed as [`XNAT_E00080`](#user-content-fn-1)[^1], `XNAT_E00114`, and `XNAT_E00152` , which are the XNAT Accession numbers for subject 004 and subject 005 (sessions 1 and 2) in our [BNC demo dataset](https://xnat.bnc.brown.edu/app/action/DisplayItemAction/search_element/xnat%3AprojectData/search_field/xnat%3AprojectData.ID/search_value/BNC_DEMODAT). Notice that by defining `skipseq`, we are choosing to  process everything except the scan with a "series description" on XNAT of "anat-t1w\_acq-memprage". You can skip or include particular scans either by their series description like this, or by their scan number on XNAT (i.e. `includeseq = [7,10]`).

#### 2.1 (Optional) Specify sessions to process with Project ID and Subject IDs rather than Accession numbers

To process all sessions from a given project, you only need to add the Project ID to your config file's `project` field.  If you only would like to process sessions from a subset of a project's subjects, add the `subjects` field with a list of one or more Subject IDs. _If you specify a project and subject(s) this way, you do not need to include a "sessions" list of Accession numbers._

<pre class="language-toml"><code class="lang-toml"><strong>[xnat2bids-args]
</strong>project="BNC_DEMODAT"
subjects=["004", "005"]
skipseq=["anat-t1w_acq-memprage"]
overwrite=true
verbose=0
</code></pre>

**NOTE:**  If exporting sessions by Subject IDs, the subjects field must be accompanied by a valid Project ID in the project field.&#x20;

**NOTE:**  Here, `overwrite=true` will tell `xnat2bids` to reprocess any existing session exports specified in your config file.  Enabling the `verbose=1` flag will turn on DEBUG logging for your script and signal `xnat2bids` to output more detailed printing to your logs.

#### 2.2 (Optional) Define Custom Parameters for Each Session

There may be the case in which you would like to add new arguments or override default parameters for processing a given session—for instance, defining logging verbosity levels or including or excluding certain sequences.&#x20;

Add the following to the bottom of your config file:

```toml
[XNAT_E00080]
includeseq=[19, 21]

[XNAT_E00114]
includeseq=[7,8,11,14]

[XNAT_E00152]
verbose=1
```

**NOTE:** The section name must match an entry in your `sessions` list.  Each session will inherit all default parameters and those specified under `[xnat2bids-args]`, overriding when necessary. _At the moment, you need to provide a sessions list of Accession numbers (rather than Project/Subject IDs) if you want to define custom parameters for each session._

#### 2.3 (Optional) Executing Pipeline Components Separately: Export Only or Skip Export Flags

If you're only interested in exporting your data from XNAT without converting your DICOM data into BIDS, you can add the following entry to your user config:

```
export-only=true
```

Similarly, if you would like to BIDS-convert data already exported to Oscar, you can add the following entry to your user config:

```
skip-export=true
```

{% hint style="info" %}
**NOTE:** When working with multi-value parameters like `includeseq` and `skipseq`, you also have the option to specify a range of values instead of individually listing them. To achieve this, utilize a string format rather than a list format, as demonstrated in the example below:

`includeseq="1-4,6,10"`
{% endhint %}

{% hint style="info" %}
**NOTE:** By default, the root output directory for DICOM exports and converted BIDS files will be `/users/<your-user-name>/bids-export/`.  If you prefer a different path to your data, you can define BIDS\_ROOT in your `[xnat2bids-args]`list as following: **`bids_root="/path/to/bids-export"`**
{% endhint %}

{% hint style="info" %}
**NOTE:**  By default, `run_xnat2bids` uses the latest version of `xnat-tools xnat2bids`, unless specified under `[xnat2bids-args]` with the following format: `version="vX.X.X"`
{% endhint %}

### 3.  Running XNAT2BIDS

Now that you have a complete configuration file like this, you are ready to run the pipeline!

```toml
[slurm-args]
mail-user = "example-user@brown.edu"
mail-type = "ALL"

[xnat2bids-args]
sessions = ["XNAT_E00080", "XNAT_E00114", "XNAT_E00152"]
skipseq=["anat-t1w_acq-memprage"]
overwrite=true

[XNAT_E00080]
includeseq=[19, 21]

[XNAT_E00114]
includeseq=[7,8,11,14]

[XNAT_E00152]
verbose=1
```

First, we need to load a module that will give us access to python and a few basic packages. From the command line, run the following:

```
module load anaconda
```

Then we can launch the script, using `--config` to specify your custom configuration file.

```
python /oscar/data/bnc/scripts/run_xnat2bids.py --config <example_user_config.toml> 
```

***

In your terminal, you should immediately see the following print statements:

```
DEBUG: {'message': 'Argument List', 'session': 'XNAT_E00152', 'slurm_param_list': ['--time 04:00:00', '--mem 16000', '--nodes 1', '--cpus-per-task 2', '--job-name xnat2bids', '--mail-user elizabeth_lorenc@brown.edu', '--mail-type ALL', '--output /gpfs/scratch/elorenc1/logs/%x-XNAT_E00152-%J.txt'], 'x2b_param_list': ['XNAT_E00152', '/users/elorenc1/bids-export/', '--host https://xnat.bnc.brown.edu', '--user elorenc1', '--skipseq anat-t1w_acq-memprage', '--overwrite', '--verbose']}
DEBUG: {'message': 'Executing xnat2bids', 'session': 'XNAT_E00152', 'command': ['sbatch', '--time', '04:00:00', '--mem', '16000', '--nodes', '1', '--cpus-per-task', '2', '--job-name', 'xnat2bids', '--mail-user', 'elizabeth_lorenc@brown.edu', '--mail-type', 'ALL', '--output', '/gpfs/scratch/elorenc1/logs/%x-XNAT_E00152-%J.txt', '--wrap', 'apptainer', 'exec', '--no-home', '-B', '/users/elorenc1/bids-export/', '/gpfs/data/bnc/simgs/brownbnc/xnat-tools-v1.6.0.sif', 'xnat2bids', '[XNAT_E00152,', '/users/elorenc1/bids-export/,', '--host,', 'https://xnat.bnc.brown.edu,', '--user,', 'elorenc1,', '--skipseq,', 'anat-t1w_acq-memprage,', '--overwrite,', '--verbose]']}
INFO: Launched 3 xnat2bids jobs
INFO: Job IDs: 11801791 11801792 11801793
INFO: Launched 1 bids-validator job to check BIDS compliance
INFO: Job ID: 11801794
INFO: Processed Scans Located At: /users/<your-username>/bids-export/
```

Check `/oscar/scratch/<your-username>/logs/` for four new log files

* `xnat2bids-XNAT_E00114-<JOB-ID>.txt`&#x20;
* `xnat2bids-XNAT_E00080-<JOB-ID>.txt`
* `xnat2bids-XNAT_E00152-<JOB-ID>.txt`&#x20;
* `bids-validator-<JOB-ID>.txt`

<details>

<summary>Click here for an example <code>xnat2bids</code> output log</summary>

```
## SLURM PROLOG ###############################################################
##    Job ID : 11801792
##  Job Name : xnat2bids
##  Nodelist : node1745
##      CPUs : 2
##  Mem/Node : 16000 MB
## Directory : /oscar/home/elorenc1/scripts
##   Job Started : Tue Oct 24 16:24:55 EDT 2023
###############################################################################
2023-10-24 16:24:57 node1745.oscar.ccv.brown.edu xnat_tools.bids_utils[243735] INFO Removing existing xnat-export session directory /users/elorenc1/bids-export/bnc/study-demodat/xnat-export/sub-005/ses-session1
2023-10-24 16:25:02 node1745.oscar.ccv.brown.edu xnat_tools.bids_utils[243735] INFO Making output xnat-export session directory /users/elorenc1/bids-export/bnc/study-demodat/xnat-export/sub-005/ses-session1
2023-10-24 16:25:02 node1745.oscar.ccv.brown.edu xnat_tools.xnat_utils[243735] INFO ------------------------------------------------
2023-10-24 16:25:02 node1745.oscar.ccv.brown.edu xnat_tools.xnat_utils[243735] INFO Get scans.
2023-10-24 16:25:02 node1745.oscar.ccv.brown.edu xnat_tools.xnat_utils[243735] INFO ------------------------------------------------
2023-10-24 16:25:02 node1745.oscar.ccv.brown.edu xnat_tools.bids_utils[243735] INFO bids_session_dir: /users/elorenc1/bids-export/bnc/study-demodat/xnat-export/sub-005/ses-session1
2023-10-24 16:25:02 node1745.oscar.ccv.brown.edu xnat_tools.bids_utils[243735] INFO BIDSNAME: anat-T1w_acq-memprageRMS
2023-10-24 16:25:02 node1745.oscar.ccv.brown.edu xnat_tools.bids_utils[243735] INFO Making scan DICOM directory /users/elorenc1/bids-export/bnc/study-demodat/xnat-export/sub-005/ses-session1/anat-T1w_acq-memprageRMS.
2023-10-24 16:25:02 node1745.oscar.ccv.brown.edu xnat_tools.bids_utils[243735] INFO Downloading files
2023-10-24 16:25:03 node1745.oscar.ccv.brown.edu py.warnings[243735] WARNING /usr/local/lib/python3.10/site-packages/xnat_tools/bids_utils.py:351: UserWarning: Changed DICOM HEADER[ProtocolName and SeriesDescription]:             anat-t1w_acq-memprage -> anat-T1w_acq-memprageRMS             anat-t1w_acq-memprage RMS -> anat-T1w_acq-memprageRMS
  warnings.warn(
.
.
.

------------------------------------------------
Get project and subject information
Project: BNC_DEMODAT
Subject ID: XNAT_S00111
Session Suffix:  SESSION1
Subject label: 005
------------------------------------------------
************************
Overwrite - Removing heudi session directory /users/elorenc1/bids-export/bnc/study-demodat/bids/sub-005/ses-session1
Overwrite - Removing sourcedata session directory /users/elorenc1/bids-export/bnc/study-demodat/bids/sourcedata/sub-005/ses-session1
Overwrite - Removing hidden session directory /users/elorenc1/bids-export/bnc/study-demodat/bids/.heudiconv/005/ses-session1
Executing Heudiconv command: heudiconv -f reproin --bids     -o /users/elorenc1/bids-export/bnc/study-demodat/bids     --dicom_dir_template /users/elorenc1/bids-export//bnc/study-demodat/xnat-export/sub-{subject}/ses-{session}/*/*.dcm     --subjects 005 --ses session1 --overwrite
INFO: Running heudiconv version 0.13.1 latest 1.0.0
INFO: Need to process 1 study sessions
INFO: PROCESSING STARTS: {'subject': '005', 'outdir': '/users/elorenc1/bids-export/bnc/study-demodat/bids/', 'session': 'session1'}
INFO: Processing 369 dicoms
INFO: Analyzing 369 dicoms
INFO: Filtering out 0 dicoms based on their filename
INFO: Generated sequence info for 4 studies with 369 entries total
INFO: Processing 4 seqinfo entries
.
.
.
INFO: Post-treating /users/elorenc1/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/dwi/sub-005_ses-session1_acq-b1500_dir-ap_sbref.json file
INFO: Adding "IntendedFor" to the fieldmaps in /users/elorenc1/bids-export/bnc/study-demodat/bids/sub-005/ses-session1.
INFO: Populating template files under /users/elorenc1/bids-export/bnc/study-demodat/bids/
INFO: PROCESSING DONE: {'subject': '005', 'outdir': '/users/elorenc1/bids-export/bnc/study-demodat/bids/', 'session': 'session1'}
Done with Heudiconv BIDS Convesion.
```



</details>

<details>

<summary>Click here for an example <code>bids-validator</code> output log</summary>

```
## SLURM PROLOG ###############################################################
##    Job ID : 11801794
##  Job Name : bids-validator
##  Nodelist : node1742
##      CPUs : 2
##  Mem/Node : 16000 MB
## Directory : /oscar/home/elorenc1/scripts
##   Job Started : Tue Oct 24 16:34:02 EDT 2023
###############################################################################
bids-validator@1.13.1
(node:148510) Warning: Closing directory handle on garbage collection
(Use `node --trace-warnings ...` to show where the warning was created)
	[33m1: [WARN] Tabular file contains custom columns not described in a data dictionary (code: 82 - CUSTOM_COLUMN_WITHOUT_DESCRIPTION)[39m
		./sub-005/ses-session1/func/sub-005_ses-session1_task-checks_run-01_events.tsv
			Evidence: Columns: TODO -- fill in rows and add more tab-separated columns if desired not defined, please define in: /events.json, /task-checks_events.json,/run-01_events.json,/task-checks_run-01_events.json,/sub-005/sub-005_events.json,/sub-005/sub-005_task-checks_events.json,/sub-005/sub-005_run-01_events.json,/sub-005/sub-005_task-checks_run-01_events.json,/sub-005/ses-session1/sub-005_ses-session1_events.json,/sub-005/ses-session1/sub-005_ses-session1_task-checks_events.json,/sub-005/ses-session1/sub-005_ses-session1_run-01_events.json,/sub-005/ses-session1/sub-005_ses-session1_task-checks_run-01_events.json,/sub-005/ses-session1/func/sub-005_ses-session1_events.json,/sub-005/ses-session1/func/sub-005_ses-session1_task-checks_events.json,/sub-005/ses-session1/func/sub-005_ses-session1_run-01_events.json,/sub-005/ses-session1/func/sub-005_ses-session1_task-checks_run-01_events.json
		./sub-005/ses-session2/func/sub-005_ses-session2_task-checks_run-01_events.tsv
			Evidence: Columns: TODO -- fill in rows and add more tab-separated columns if desired not defined, please define in: /events.json, /task-checks_events.json,/run-01_events.json,/task-checks_run-01_events.json,/sub-005/sub-005_events.json,/sub-005/sub-005_task-checks_events.json,/sub-005/sub-005_run-01_events.json,/sub-005/sub-005_task-checks_run-01_events.json,/sub-005/ses-session2/sub-005_ses-session2_events.json,/sub-005/ses-session2/sub-005_ses-session2_task-checks_events.json,/sub-005/ses-session2/sub-005_ses-session2_run-01_events.json,/sub-005/ses-session2/sub-005_ses-session2_task-checks_run-01_events.json,/sub-005/ses-session2/func/sub-005_ses-session2_events.json,/sub-005/ses-session2/func/sub-005_ses-session2_task-checks_events.json,/sub-005/ses-session2/func/sub-005_ses-session2_run-01_events.json,/sub-005/ses-session2/func/sub-005_ses-session2_task-checks_run-01_events.json
		./sub-005/ses-session2/func/sub-005_ses-session2_task-checks_run-02_events.tsv
			Evidence: Columns: TODO -- fill in rows and add more tab-separated columns if desired not defined, please define in: /events.json, /task-checks_events.json,/run-02_events.json,/task-checks_run-02_events.json,/sub-005/sub-005_events.json,/sub-005/sub-005_task-checks_events.json,/sub-005/sub-005_run-02_events.json,/sub-005/sub-005_task-checks_run-02_events.json,/sub-005/ses-session2/sub-005_ses-session2_events.json,/sub-005/ses-session2/sub-005_ses-session2_task-checks_events.json,/sub-005/ses-session2/sub-005_ses-session2_run-02_events.json,/sub-005/ses-session2/sub-005_ses-session2_task-checks_run-02_events.json,/sub-005/ses-session2/func/sub-005_ses-session2_events.json,/sub-005/ses-session2/func/sub-005_ses-session2_task-checks_events.json,/sub-005/ses-session2/func/sub-005_ses-session2_run-02_events.json,/sub-005/ses-session2/func/sub-005_ses-session2_task-checks_run-02_events.json
		./sub-005/ses-session2/func/sub-005_ses-session2_task-motionloc_events.tsv
			Evidence: Columns: TODO -- fill in rows and add more tab-separated columns if desired not defined, please define in: /events.json, /task-motionloc_events.json,/sub-005/sub-005_events.json,/sub-005/sub-005_task-motionloc_events.json,/sub-005/ses-session2/sub-005_ses-session2_events.json,/sub-005/ses-session2/sub-005_ses-session2_task-motionloc_events.json,/sub-005/ses-session2/func/sub-005_ses-session2_events.json,/sub-005/ses-session2/func/sub-005_ses-session2_task-motionloc_events.json
		./sub-005/ses-session2/func/sub-005_ses-session2_task-resting_events.tsv
			Evidence: Columns: TODO -- fill in rows and add more tab-separated columns if desired not defined, please define in: /events.json, /task-resting_events.json,/sub-005/sub-005_events.json,/sub-005/sub-005_task-resting_events.json,/sub-005/ses-session2/sub-005_ses-session2_events.json,/sub-005/ses-session2/sub-005_ses-session2_task-resting_events.json,/sub-005/ses-session2/func/sub-005_ses-session2_events.json,/sub-005/ses-session2/func/sub-005_ses-session2_task-resting_events.json

[36m	Please visit https://neurostars.org/search?q=CUSTOM_COLUMN_WITHOUT_DESCRIPTION for existing conversations about this issue.[39m

	[33m2: [WARN] Not all subjects contain the same sessions. (code: 97 - MISSING_SESSION)[39m
		./sub-004/ses-session1
			Evidence: Subject: sub-004; Missing session: ses-session1
		./sub-004/ses-session2
			Evidence: Subject: sub-004; Missing session: ses-session2
		./sub-005/ses-01
			Evidence: Subject: sub-005; Missing session: ses-01

[36m	Please visit https://neurostars.org/search?q=MISSING_SESSION for existing conversations about this issue.[39m

	[33m3: [WARN] The recommended file /README is very small. Please consider expanding it with additional information about the dataset. (code: 213 - README_FILE_SMALL)[39m
		./README

[36m	Please visit https://neurostars.org/search?q=README_FILE_SMALL for existing conversations about this issue.[39m

        [34m[4mSummary:[24m[39m                [34m[4mAvailable Tasks:[24m[39m                          [34m[4mAvailable Modalities:[39m[24m 
        65 Files, 1.21GB        checks                                    MRI                   
        2 - Subjects            motionloc                                                       
        3 - Sessions            TODO: full task name for checks                                 
                                TODO: full task name for motionloc                              
                                TODO: full task name for resting                                
                                resting                                                         


[36m	If you have any questions, please post on https://neurostars.org/tags/bids.[39m

```



</details>

Finally, go to your \~/bids-export directory to check your exported DICOM data and processed BIDS directory structure! 🎉

<details>

<summary>Click here to see how it should look</summary>

```
bnc/study-demodat/bids/
|-- CHANGES
|-- README
|-- dataset_description.json
|-- participants.json
|-- participants.tsv
|-- scans.json
|-- sourcedata
|   |-- README
|   |-- sub-004
|   |   `-- ses-01
|   |       |-- dwi
|   |       |   `-- sub-004_ses-01_acq-b1500_dir-pa_dwi.dicom.tgz
|   |       `-- fmap
|   |           `-- sub-004_ses-01_acq-diffSE_dir-pa_epi.dicom.tgz
|   `-- sub-005
|       |-- ses-session1
|       |   |-- anat
|       |   |   `-- sub-005_ses-session1_acq-memprageRMS_T1w.dicom.tgz
|       |   |-- dwi
|       |   |   `-- sub-005_ses-session1_acq-b1500_dir-ap_sbref.dicom.tgz
|       |   |-- fmap
|       |   |   `-- sub-005_ses-session1_acq-boldGRE_magnitude.dicom.tgz
|       |   `-- func
|       |       `-- sub-005_ses-session1_task-checks_run-01_bold.dicom.tgz
|       `-- ses-session2
|           |-- anat
|           |   |-- sub-005_ses-session2_acq-aascoutMPRcor_scout.dicom.tgz
|           |   |-- sub-005_ses-session2_acq-aascoutMPRsag_scout.dicom.tgz
|           |   |-- sub-005_ses-session2_acq-aascoutMPRtra_scout.dicom.tgz
|           |   |-- sub-005_ses-session2_acq-aascout_scout.dicom.tgz
|           |   |-- sub-005_ses-session2_acq-localizer_scout.dicom.tgz
|           |   `-- sub-005_ses-session2_acq-memprageRMS_T1w.dicom.tgz
|           |-- dwi
|           |   |-- sub-005_ses-session2_acq-b1500_dir-ap_dwi.dicom.tgz
|           |   |-- sub-005_ses-session2_acq-b1500_dir-ap_sbref.dicom.tgz
|           |   |-- sub-005_ses-session2_acq-b1500_dir-pa_dwi.dicom.tgz
|           |   `-- sub-005_ses-session2_acq-b1500_dir-pa_sbref.dicom.tgz
|           |-- fmap
|           |   |-- sub-005_ses-session2_acq-boldGRE_magnitude.dicom.tgz
|           |   |-- sub-005_ses-session2_acq-boldGRE_phasediff.dicom.tgz
|           |   |-- sub-005_ses-session2_acq-diffSE_dir-ap_epi.dicom.tgz
|           |   `-- sub-005_ses-session2_acq-diffSE_dir-pa_epi.dicom.tgz
|           `-- func
|               |-- sub-005_ses-session2_task-checks_run-01_bold.dicom.tgz
|               |-- sub-005_ses-session2_task-checks_run-02_bold.dicom.tgz
|               |-- sub-005_ses-session2_task-motionloc_bold.dicom.tgz
|               `-- sub-005_ses-session2_task-resting_bold.dicom.tgz
|-- sub-004
|   `-- ses-01
|       |-- dwi
|       |   |-- sub-004_ses-01_acq-b1500_dir-pa_dwi.bval
|       |   |-- sub-004_ses-01_acq-b1500_dir-pa_dwi.bvec
|       |   |-- sub-004_ses-01_acq-b1500_dir-pa_dwi.json
|       |   `-- sub-004_ses-01_acq-b1500_dir-pa_dwi.nii.gz
|       |-- fmap
|       |   |-- sub-004_ses-01_acq-diffSE_dir-pa_epi.json
|       |   `-- sub-004_ses-01_acq-diffSE_dir-pa_epi.nii.gz
|       `-- sub-004_ses-01_scans.tsv
|-- sub-005
|   |-- ses-session1
|   |   |-- anat
|   |   |   |-- sub-005_ses-session1_acq-memprageRMS_T1w.json
|   |   |   `-- sub-005_ses-session1_acq-memprageRMS_T1w.nii.gz
|   |   |-- dwi
|   |   |   |-- sub-005_ses-session1_acq-b1500_dir-ap_sbref.json
|   |   |   `-- sub-005_ses-session1_acq-b1500_dir-ap_sbref.nii.gz
|   |   |-- fmap
|   |   |   |-- sub-005_ses-session1_acq-boldGRE_magnitude1.json
|   |   |   |-- sub-005_ses-session1_acq-boldGRE_magnitude1.nii.gz
|   |   |   |-- sub-005_ses-session1_acq-boldGRE_magnitude2.json
|   |   |   `-- sub-005_ses-session1_acq-boldGRE_magnitude2.nii.gz
|   |   |-- func
|   |   |   |-- sub-005_ses-session1_task-checks_run-01_bold.json
|   |   |   |-- sub-005_ses-session1_task-checks_run-01_bold.nii.gz
|   |   |   `-- sub-005_ses-session1_task-checks_run-01_events.tsv
|   |   `-- sub-005_ses-session1_scans.tsv
|   `-- ses-session2
|       |-- anat
|       |   |-- sub-005_ses-session2_acq-memprageRMS_T1w.json
|       |   `-- sub-005_ses-session2_acq-memprageRMS_T1w.nii.gz
|       |-- dwi
|       |   |-- sub-005_ses-session2_acq-b1500_dir-ap_dwi.bval
|       |   |-- sub-005_ses-session2_acq-b1500_dir-ap_dwi.bvec
|       |   |-- sub-005_ses-session2_acq-b1500_dir-ap_dwi.json
|       |   |-- sub-005_ses-session2_acq-b1500_dir-ap_dwi.nii.gz
|       |   |-- sub-005_ses-session2_acq-b1500_dir-ap_sbref.json
|       |   |-- sub-005_ses-session2_acq-b1500_dir-ap_sbref.nii.gz
|       |   |-- sub-005_ses-session2_acq-b1500_dir-pa_dwi.bval
|       |   |-- sub-005_ses-session2_acq-b1500_dir-pa_dwi.bvec
|       |   |-- sub-005_ses-session2_acq-b1500_dir-pa_dwi.json
|       |   |-- sub-005_ses-session2_acq-b1500_dir-pa_dwi.nii.gz
|       |   |-- sub-005_ses-session2_acq-b1500_dir-pa_sbref.json
|       |   `-- sub-005_ses-session2_acq-b1500_dir-pa_sbref.nii.gz
|       |-- fmap
|       |   |-- sub-005_ses-session2_acq-boldGRE_magnitude1.json
|       |   |-- sub-005_ses-session2_acq-boldGRE_magnitude1.nii.gz
|       |   |-- sub-005_ses-session2_acq-boldGRE_magnitude2.json
|       |   |-- sub-005_ses-session2_acq-boldGRE_magnitude2.nii.gz
|       |   |-- sub-005_ses-session2_acq-boldGRE_phasediff.json
|       |   |-- sub-005_ses-session2_acq-boldGRE_phasediff.nii.gz
|       |   |-- sub-005_ses-session2_acq-diffSE_dir-ap_epi.json
|       |   |-- sub-005_ses-session2_acq-diffSE_dir-ap_epi.nii.gz
|       |   |-- sub-005_ses-session2_acq-diffSE_dir-pa_epi.json
|       |   `-- sub-005_ses-session2_acq-diffSE_dir-pa_epi.nii.gz
|       |-- func
|       |   |-- sub-005_ses-session2_task-checks_run-01_bold.json
|       |   |-- sub-005_ses-session2_task-checks_run-01_bold.nii.gz
|       |   |-- sub-005_ses-session2_task-checks_run-01_events.tsv
|       |   |-- sub-005_ses-session2_task-checks_run-02_bold.json
|       |   |-- sub-005_ses-session2_task-checks_run-02_bold.nii.gz
|       |   |-- sub-005_ses-session2_task-checks_run-02_events.tsv
|       |   |-- sub-005_ses-session2_task-motionloc_bold.json
|       |   |-- sub-005_ses-session2_task-motionloc_bold.nii.gz
|       |   |-- sub-005_ses-session2_task-motionloc_events.tsv
|       |   |-- sub-005_ses-session2_task-resting_bold.json
|       |   |-- sub-005_ses-session2_task-resting_bold.nii.gz
|       |   `-- sub-005_ses-session2_task-resting_events.tsv
|       `-- sub-005_ses-session2_scans.tsv
|-- task-checks_bold.json
|-- task-motionloc_bold.json
`-- task-resting_bold.json

```



</details>

[^1]: 
