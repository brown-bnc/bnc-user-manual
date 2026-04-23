# Running xnat2bids with a custom configuration

Open a new file in your favorite text editor, and save it as something ending in **.toml** like x2b\_my\_first\_config.toml.

{% hint style="info" %}
To open VSCode in an interactive desktop, open a terminal with a right click followed by selecting 'Open Terminal Here".  Next, run the command: **`module load vscode`**

To launch VSCode, run **`code`** on the command line.
{% endhint %}

## 1. Configure slurm parameters

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

## 2. Configure xnat2bids parameters

Next, you'll need to configure what arguments to pass to `xnat2bids`, such as the session (or comma-separated list of sessions) you would like to process, as well as any other arguments.

<details>

<summary>💡Click here for a comprehensive list of all available options</summary>

{% code overflow="wrap" %}

```toml
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

validate_frames BOOLEAN: Use if you manually terminate your fMRI runs. If the final volume does not contain the expected number of slices, the associated DICOM file(s) will be deleted. [default: false]
```

{% endcode %}



</details>

For this demo, paste the following text into your config file:

```toml
[xnat2bids-args]
sessions = ["XNAT_E01849", "XNAT_E01867", "XNAT_E01943"]
skipseq=["anat-scout_acq-localizer", "anat-scout_acq-aascout"]
```

Here, we are setting the sessions to be processed as XNAT\_E01849, XNAT\_E01867, and XNAT\_E01943, which are the XNAT Accession numbers for subject 101 (sessions 1 and 2) and subject 102 (session 1) in our [BNC demo dataset](https://xnat.bnc.brown.edu/app/action/DisplayItemAction/search_element/xnat%3AprojectData/search_field/xnat%3AprojectData.ID/search_value/BNC_DEMODAT). Notice that by defining `skipseq`, we are choosing to  process everything except the scan with a "series description" on XNAT of "anat-scout\_acq-localizer" and "anat-scout\_acq-aascout". You can skip or include particular scans either by their series description like this, or by their scan number on XNAT (i.e. `includeseq = [7,10]`).

### 2.1 (Optional) Specify sessions to process with Project ID and Subject IDs rather than Accession numbers

To process all sessions from a given project, you only need to add the Project ID to your config file's `project` field.  If you only would like to process sessions from a subset of a project's subjects, add the `subjects` field with a list of one or more Subject IDs. _If you specify a project and subject(s) this way, you do not need to include a "sessions" list of Accession numbers._

<pre class="language-toml"><code class="lang-toml"><strong>[xnat2bids-args]
</strong>project="BNC_DEMODAT2"
subjects=["101", "102"]
skipseq=["anat-scout_acq-localizer", "anat-scout_acq-aascout"]
overwrite=true
verbose=0
</code></pre>

**NOTE:**  If exporting sessions by Subject IDs, the subjects field must be accompanied by a valid Project ID in the project field.&#x20;

**NOTE:**  Here, `overwrite=true` will tell `xnat2bids` to reprocess any existing session exports specified in your config file. Use this with caution- it may also overwrite any preprocessing done in the '/bids/derivatives' folder. Enabling the `verbose=1` flag will turn on DEBUG logging for your script and signal `xnat2bids` to output more detailed printing to your logs.

### 2.2 (Optional) Define Custom Parameters for Each Session

There may be the case in which you would like to add new arguments or override default parameters for processing a given session—for instance, defining logging verbosity levels or including or excluding certain sequences.&#x20;

Add the following to the bottom of your config file:

```toml
[XNAT_E01849]
includeseq=[18, 23]

[XNAT_E01867]
includeseq=[6,15,19,21]

[XNAT_E01943]
verbose=1
```

**NOTE:** The section name must match an entry in your `sessions` list.  Each session will inherit all default parameters and those specified under `[xnat2bids-args]`, overriding when necessary. _At the moment, you need to provide a sessions list of Accession numbers (rather than Project/Subject IDs) if you want to define custom parameters for each session._

### 2.3 (Optional) Executing Pipeline Components Separately: Export Only or Skip Export Flags

If you're only interested in exporting your data from XNAT without converting your DICOM data into BIDS, you can add the following entry to your user config:

```toml
export-only=true
```

Similarly, if you would like to BIDS-convert data already exported to Oscar, you can add the following entry to your user config:

```toml
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

## 3.  Running XNAT2BIDS

Now that you have a complete configuration file like this, you are ready to run the pipeline!

```toml
[slurm-args]
mail-user = "example-user@brown.edu"
mail-type = "ALL"

[xnat2bids-args]
sessions = ["XNAT_E01849", "XNAT_E01867", "XNAT_E01943"]
skipseq=["anat-scout_acq-localizer", "anat-scout_acq-aascout"]

[XNAT_E01849]
includeseq=[18, 23]

[XNAT_E01867]
includeseq=[6,15,19,21]

[XNAT_E01943]
verbose=1
```

First, we need to load a module that will give us access to python and a few basic packages. From the command line, run the following:

```bash
module load anaconda3
```

Then we can launch the script, using `--config` to specify your custom configuration file.

```bash
python /oscar/data/bnc/scripts/run_xnat2bids.py --config <example_user_config.toml> 
```

{% hint style="warning" %}
As of January 2026 (and depending on which modules you already have loaded), loading the anaconda3 module can interfere with other modules like vscode. If you have trouble, load the anaconda3 module immediately before launching the run\_xnat2bids.py script, and open a new terminal once your job is off and running.
{% endhint %}

***

In your terminal, you should immediately see the following print statements:

```console
DEBUG: {'message': 'Argument List', 'session': 'XNAT_E01943', 'slurm_param_list': ['--time 04:00:00', '--mem 16000', '--nodes 1', '--cpus-per-task 2', '--job-name xnat2bids', '--mail-user gillian_leblanc@brown.edu', '--mail-type ALL', '--output /oscar/scratch/gleblan1/logs/%x-XNAT_E01943-%J.txt'], 'x2b_param_list': ['XNAT_E01943', '/users/gleblan1/bids-export/', '--host "https://xnat.bnc.brown.edu"', '--user gleblan1', '--skipseq "anat-scout_acq-localizer" --skipseq "anat-scout_acq-aascout"', '--verbose']}
sbatch: slurm_job_submit: No partition specified, moved to batch.
sbatch: slurm_job_submit: No partition specified, moved to batch.
DEBUG: {'message': 'Executing xnat2bids', 'session': 'XNAT_E01943', 'command': 'sbatch --time 04:00:00 --mem 16000 --nodes 1 --cpus-per-task 2 --job-name xnat2bids --mail-user gillian_leblanc@brown.edu --mail-type ALL --output /oscar/scratch/gleblan1/logs/%x-XNAT_E01943-%J.txt --wrap \'""apptainer exec --no-home -B /users/gleblan1/bids-export/ /oscar/data/bnc/simgs/brownbnc/xnat-tools-v2.3.0.sif xnat2bids XNAT_E01943 /users/gleblan1/bids-export/ --host "https://xnat.bnc.brown.edu" --user gleblan1 --pass [REDACTED] --skipseq "anat-scout_acq-localizer" --skipseq "anat-scout_acq-aascout" --verbose""\''}
sbatch: slurm_job_submit: No partition specified, moved to batch.
DEBUG: {'message': 'Executing bids validator', 'command': "sbatch -d afterok:992820:992821:992822 --time 04:00:00 --mem 16000 --nodes 1 --cpus-per-task 2 --job-name bids-validator --mail-user gillian_leblanc@brown.edu --mail-type ALL --output /oscar/scratch/gleblan1/logs/%x-%J.txt --kill-on-invalid-dep=yes --wrap 'export DENO_DIR=/scratch/deno; apptainer exec --no-home -B /users/gleblan1/bids-export//bnc/study-demodat2/bids:/bids:ro -B /oscar/scratch/gleblan1:/scratch /oscar/data/bnc/simgs/brownbnc/xnat-tools-v2.3.0.sif deno run -A -qr jsr:@bids/validator /bids'"}
sbatch: slurm_job_submit: No partition specified, moved to batch.
INFO: Launched 3 xnat2bids jobs
INFO: Job IDs: 992820 992821 992822
INFO: Launched 1 bids-validator job to check BIDS compliance
INFO: Job ID: 992824
INFO: 

***********
We have recently upgraded to the BIDS validator 2.0.

This version checks metadata more thoroughly, so it identifies errors that the legacy validator (https://bids-standard.github.io/legacy-validator/) did not.
To make existing data in this BIDS directory compatible with the new validator, paste the following into the terminal (on OOD or an interact session):

apptainer exec --no-home -B /users/gleblan1/bids-export/:/bids /oscar/data/bnc/simgs/brownbnc/xnat-tools-v2.3.0.sif python -c 'from xnat_tools.bids_utils import correct_for_bids_schema_validator; correct_for_bids_schema_validator("/bids")'

Then re-run BIDS validation with:
export DENO_DIR=/scratch/deno; apptainer exec --no-home -B /users/gleblan1/bids-export//bnc/study-demodat2/bids:/bids:ro -B /oscar/scratch/gleblan1:/scratch /oscar/data/bnc/simgs/brownbnc/xnat-tools-v2.3.0.sif deno run -A -qr jsr:@bids/validator /bids

Please contact cobre-bnc@brown.edu with any issues!

***********
INFO: Processed Scans Located At: /users/your-username/bids-export/

```

Check `/oscar/scratch/<your-username>/logs/` for four new log files

* `xnat2bids-XNAT_E01849-<JOB-ID>.txt`&#x20;
* `xnat2bids-XNAT_E01867-<JOB-ID>.txt`
* `xnat2bids-XNAT_E01943-<JOB-ID>.txt`&#x20;
* `bids-validator-<JOB-ID>.txt`

<details>

<summary>Click here for an example <code>xnat2bids</code> output log</summary>

```bash
## SLURM PROLOG ###############################################################
##    Job ID : 992820
##  Job Name : xnat2bids
##  Nodelist : node2314
##      CPUs : 6
##  Mem/Node : 16000 MB
## Directory : /oscar/data/mworden/gleblan1/Demodat2_documentation/utility_script_example
##   Job Started : Mon Mar 23 16:18:11 EDT 2026
###############################################################################
mkdir -p failed for path /users/gleblan1/.ood_config/matplotlib: [Errno 30] Read-only file system: '/users/gleblan1/.ood_config'
Matplotlib created a temporary cache directory at /tmp/matplotlib-vp7_damq because there was an issue with the default path (/users/gleblan1/.ood_config/matplotlib); it is highly recommended to set the MPLCONFIGDIR environment variable to a writable directory, in particular to speed up the import of Matplotlib and to better support multiprocessing.
2026-03-23 16:18:19 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO Making output xnat-export session directory /users/gleblan1/bids-export/bnc/study-demodat2/xnat-export/sub-101/ses-01
2026-03-23 16:18:19 node2314.oscar.ccv.brown.edu xnat_tools.xnat_utils[1661466] INFO ------------------------------------------------
2026-03-23 16:18:19 node2314.oscar.ccv.brown.edu xnat_tools.xnat_utils[1661466] INFO Get scans.
2026-03-23 16:18:19 node2314.oscar.ccv.brown.edu xnat_tools.xnat_utils[1661466] INFO ------------------------------------------------
2026-03-23 16:18:19 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO bids_session_dir: /users/gleblan1/bids-export/bnc/study-demodat2/xnat-export/sub-101/ses-01
2026-03-23 16:18:19 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO BIDSNAME: dwi_acq-b1500_dir-ap
2026-03-23 16:18:19 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO Making scan DICOM directory /users/gleblan1/bids-export/bnc/study-demodat2/xnat-export/sub-101/ses-01/dwi_acq-b1500_dir-ap.
2026-03-23 16:18:19 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO Downloading files
2026-03-23 16:18:46 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO Done.
2026-03-23 16:18:46 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO ---------------------------------
2026-03-23 16:18:46 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO bids_session_dir: /users/gleblan1/bids-export/bnc/study-demodat2/xnat-export/sub-101/ses-01
2026-03-23 16:18:46 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO BIDSNAME: dwi_acq-b1500_dir-pa
2026-03-23 16:18:46 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO Making scan DICOM directory /users/gleblan1/bids-export/bnc/study-demodat2/xnat-export/sub-101/ses-01/dwi_acq-b1500_dir-pa.
2026-03-23 16:18:46 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO Downloading files
2026-03-23 16:19:12 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO Done.
2026-03-23 16:19:13 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO ---------------------------------
2026-03-23 16:22:34 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO List of sessions sub-directories ['ses-01']
2026-03-23 16:22:34 node2314.oscar.ccv.brown.edu xnat_tools.bids_utils[1661466] INFO Checking for missing phase units in jsons at path /users/gleblan1/bids-export//bnc/study-demodat2/bids/sub-101/ses-01
------------------------------------------------
Get project and subject information
Project: BNC_DEMODAT2
Subject ID: XNAT_S01516
Subject label: 101
Session Suffix:  01
------------------------------------------------
************************
Making output BIDS Session directory /users/gleblan1/bids-export/bnc/study-demodat2/bids
Executing Heudiconv command: heudiconv -f reproin --bids -o /users/gleblan1 --files /users/gleblan1/bids-export/bnc/study-demodat2/xnat-export/sub-101/ses-01/dwi_acq-b1500_dir-ap /users/gleblan1/bids-export/bnc/study-demodat2/xnat-export/sub-101/ses-01/dwi_acq-b1500_dir-pa --locator bids-export/bnc/study-demodat2/bids --subjects 101 --ses 01
260323-16:19:32,824 nipype.workflow INFO:
	 [Node] Setting-up "convert" in "/tmp/dcm2niix0tp5npm1/convert".
260323-16:19:32,871 nipype.workflow INFO:
	 [Node] Executing "convert" <nipype.interfaces.dcm2nii.Dcm2niix>
260323-16:19:33,574 nipype.interface INFO:
	 stdout 2026-03-23T16:19:33.574391:Chris Rorden's dcm2niiX version v1.0.20241211  (JP2:OpenJPEG) (JP-LS:CharLS) GCC8.4.0 x86-64 (64-bit Linux)
260323-16:19:33,574 nipype.interface INFO:
	 stdout 2026-03-23T16:19:33.574391:Found 106 DICOM file(s)
260323-16:19:33,574 nipype.interface INFO:
	 stdout 2026-03-23T16:19:33.574391:Convert 106 DICOM as /users/gleblan1/bids-export/bnc/study-demodat2/bids/sub-101/ses-01/dwi/sub-101_ses-01_acq-b1500_dir-ap_dwi_heudiconv088 (140x140x84x106)
260323-16:19:42,616 nipype.interface INFO:
	 stdout 2026-03-23T16:19:42.616926:Conversion required 9.616262 seconds (9.300509 for core code).
260323-16:19:42,648 nipype.workflow INFO:
	 [Node] Finished "convert", elapsed time 9.658842s.
260323-16:20:20,549 nipype.workflow INFO:
	 [Node] Setting-up "embedder" in "/tmp/embedmetaizrjevsa/embedder".
260323-16:20:20,567 nipype.workflow INFO:
	 [Node] Executing "embedder" <nipype.interfaces.utility.wrappers.Function>
260323-16:21:03,818 nipype.workflow INFO:
	 [Node] Finished "embedder", elapsed time 42.982494s.
260323-16:21:03,819 nipype.workflow WARNING:
	 Storing result file without outputs
260323-16:21:03,820 nipype.workflow WARNING:
	 [Node] Error on "embedder" (/tmp/embedmetaizrjevsa/embedder)
260323-16:21:03,871 nipype.workflow INFO:
	 [Node] Setting-up "convert" in "/tmp/dcm2niix5k98bllz/convert".
260323-16:21:03,889 nipype.workflow INFO:
	 [Node] Executing "convert" <nipype.interfaces.dcm2nii.Dcm2niix>
260323-16:21:04,375 nipype.interface INFO:
	 stdout 2026-03-23T16:21:04.375881:Chris Rorden's dcm2niiX version v1.0.20241211  (JP2:OpenJPEG) (JP-LS:CharLS) GCC8.4.0 x86-64 (64-bit Linux)
260323-16:21:04,376 nipype.interface INFO:
	 stdout 2026-03-23T16:21:04.375881:Found 106 DICOM file(s)
260323-16:21:04,376 nipype.interface INFO:
	 stdout 2026-03-23T16:21:04.375881:Convert 106 DICOM as /users/gleblan1/bids-export/bnc/study-demodat2/bids/sub-101/ses-01/dwi/sub-101_ses-01_acq-b1500_dir-pa_dwi_heudiconv957 (140x140x84x106)
260323-16:21:13,367 nipype.interface INFO:
	 stdout 2026-03-23T16:21:13.367392:Conversion required 9.465933 seconds (9.185854 for core code).
260323-16:21:13,525 nipype.workflow INFO:
	 [Node] Finished "convert", elapsed time 9.634832s.
260323-16:21:50,811 nipype.workflow INFO:
	 [Node] Setting-up "embedder" in "/tmp/embedmeta9qnc358d/embedder".
260323-16:21:50,825 nipype.workflow INFO:
	 [Node] Executing "embedder" <nipype.interfaces.utility.wrappers.Function>
260323-16:22:33,723 nipype.workflow INFO:
	 [Node] Finished "embedder", elapsed time 42.661512s.
260323-16:22:33,723 nipype.workflow WARNING:
	 Storing result file without outputs
260323-16:22:33,724 nipype.workflow WARNING:
	 [Node] Error on "embedder" (/tmp/embedmeta9qnc358d/embedder)
Done with Heudiconv BIDS conversion.
------------------------------------------------
Get project and subject information
Project: BNC_DEMODAT2
Subject ID: XNAT_S01516
Subject label: 101
Session Suffix:  01
------------------------------------------------
```

</details>

<details>

<summary>Click here for an example <code>bids-validator</code> output log</summary>

```bash
## SLURM PROLOG ###############################################################
##    Job ID : 992824
##  Job Name : bids-validator
##  Nodelist : node2314
##      CPUs : 6
##  Mem/Node : 16000 MB
## Directory : /oscar/data/mworden/gleblan1/Demodat2_documentation/utility_script_example
##   Job Started : Mon Mar 23 16:32:24 EDT 2026
###############################################################################
	[WARNING] README_FILE_SMALL The recommended file '/README' is very small.
Please consider expanding it with additional information about the dataset.

		/README

	Please visit https://neurostars.org/search?q=README_FILE_SMALL for existing conversations about this issue.

	[WARNING] JSON_KEY_RECOMMENDED A JSON file is missing a key listed as recommended.
		HEDVersion
		/dataset_description.json - Field description: If HED tags are used:
The version of the HED schema used to validate HED tags for study.
May include a single schema or a base schema and one or more library schema.


		GeneratedBy
		/dataset_description.json - Field description: Used to specify provenance of the dataset.


		SourceDatasets
		/dataset_description.json - Field description: Used to specify the locations and relevant attributes of all source datasets (BIDS or not).
Valid keys in each object include `"URL"`, `"DOI"` (see
[URI](https://bids-specification.readthedocs.io/en/stable/common-principles.md#uniform-resource-indicator)), and
`"Version"` with
[string](https://www.w3schools.com/js/js_json_datatypes.asp)
values.


	Please visit https://neurostars.org/search?q=JSON_KEY_RECOMMENDED for existing conversations about this issue.

	[WARNING] SIDECAR_KEY_RECOMMENDED A data file's JSON sidecar is missing a key listed as recommended.
		PulseSequenceType
		/sub-101/ses-01/dwi/sub-101_ses-01_acq-b1500_dir-ap_dwi.nii.gz - Field description: A general description of the pulse sequence used for the scan.

		/sub-101/ses-01/dwi/sub-101_ses-01_acq-b1500_dir-pa_dwi.nii.gz - Field description: A general description of the pulse sequence used for the scan.


		15 more files with the same issue

		SequenceName
		/sub-101/ses-01/dwi/sub-101_ses-01_acq-b1500_dir-ap_dwi.nii.gz - Field description: Manufacturer's designation of the sequence name.
Corresponds to [DICOM Tag 0018, 0024](http://www.dicomlookup.com/dicomtags/(0018,0024))
`Sequence Name`.

		/sub-101/ses-01/dwi/sub-101_ses-01_acq-b1500_dir-pa_dwi.nii.gz - Field description: Manufacturer's designation of the sequence name.
Corresponds to [DICOM Tag 0018, 0024](http://www.dicomlookup.com/dicomtags/(0018,0024))
`Sequence Name`.


		13 more files with the same issue

		InstitutionalDepartmentName
		/sub-101/ses-01/dwi/sub-101_ses-01_acq-b1500_dir-ap_dwi.nii.gz - Field description: The department in the institution in charge of the equipment that produced
the measurements.

		/sub-101/ses-01/dwi/sub-101_ses-01_acq-b1500_dir-pa_dwi.nii.gz - Field description: The department in the institution in charge of the equipment that produced
the measurements.


		15 more files with the same issue

		PartialFourierDirection
		/sub-101/ses-02/anat/sub-101_ses-02_acq-memprageRMS_T1w.nii.gz - Field description: The direction where only partial Fourier information was collected.
Corresponds to [DICOM Tag 0018, 9036](http://www.dicomlookup.com/dicomtags/(0018,9036))
`Partial Fourier Direction`.

		/sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.nii.gz - Field description: The direction where only partial Fourier information was collected.
Corresponds to [DICOM Tag 0018, 9036](http://www.dicomlookup.com/dicomtags/(0018,9036))
`Partial Fourier Direction`.


		7 more files with the same issue

		ParallelReductionFactorOutOfPlane
		/sub-101/ses-02/anat/sub-101_ses-02_acq-memprageRMS_T1w.nii.gz - Field description: The parallel imaging (for instance, GRAPPA) factor in the second phase encoding dimension of 3D sequences.
Use the denominator of the fraction of k-space encoded in the second phase encoding dimension.
For example, 2 means half of k-space is encoded.
Will typically be 1 for 2D sequences, as each slice in a 2D acquisition is usually fully encoded.
`ParallelReductionFactorOutOfPlane` should not be confused with `MultibandAccelerationFactor`,
as they imply different methods of accelerating the acquisition.
Corresponds to [DICOM Tag 0018, 9155](http://www.dicomlookup.com/dicomtags/(0018,9155))
`Parallel Reduction Factor out-of-plane`.

		/sub-102/ses-01/anat/sub-102_ses-01_acq-memprageRMS_T1w.nii.gz - Field description: The parallel imaging (for instance, GRAPPA) factor in the second phase encoding dimension of 3D sequences.
Use the denominator of the fraction of k-space encoded in the second phase encoding dimension.
For example, 2 means half of k-space is encoded.
Will typically be 1 for 2D sequences, as each slice in a 2D acquisition is usually fully encoded.
`ParallelReductionFactorOutOfPlane` should not be confused with `MultibandAccelerationFactor`,
as they imply different methods of accelerating the acquisition.
Corresponds to [DICOM Tag 0018, 9155](http://www.dicomlookup.com/dicomtags/(0018,9155))
`Parallel Reduction Factor out-of-plane`.


		Instructions
		/sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.nii.gz - Field description: Text of the instructions given to participants before the recording.

		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.nii.gz - Field description: Text of the instructions given to participants before the recording.


		2 more files with the same issue

		TaskDescription
		/sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.nii.gz - Field description: Longer description of the task.

		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.nii.gz - Field description: Longer description of the task.


		2 more files with the same issue

		CogPOID
		/sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.nii.gz - Field description: [URI](https://bids-specification.readthedocs.io/en/stable/common-principles.md#uniform-resource-indicator)
of the corresponding [CogPO](http://www.cogpo.org/) term.

		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.nii.gz - Field description: [URI](https://bids-specification.readthedocs.io/en/stable/common-principles.md#uniform-resource-indicator)
of the corresponding [CogPO](http://www.cogpo.org/) term.


		2 more files with the same issue

		MatrixCoilMode
		/sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.nii.gz - Field description: (If used)
A method for reducing the number of independent channels by combining in
analog the signals from multiple coil elements.
There are typically different default modes when using un-accelerated or
accelerated (for example, `"GRAPPA"`, `"SENSE"`) imaging.

		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.nii.gz - Field description: (If used)
A method for reducing the number of independent channels by combining in
analog the signals from multiple coil elements.
There are typically different default modes when using un-accelerated or
accelerated (for example, `"GRAPPA"`, `"SENSE"`) imaging.


		2 more files with the same issue

		StimulusPresentation
		/sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_events.tsv - Field description: Object containing key-value pairs related to the software used to present
the stimuli during the experiment.

		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_events.tsv - Field description: Object containing key-value pairs related to the software used to present
the stimuli during the experiment.


		2 more files with the same issue

		PhysioType
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_recording-cardiac_physio.tsv.gz - Field description: Defines the specific type of physiological recording.
For backwards compatibility, the default value is `"generic"`.

		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_recording-respiratory_physio.tsv.gz - Field description: Defines the specific type of physiological recording.
For backwards compatibility, the default value is `"generic"`.


		4 more files with the same issue

		TaskName
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_recording-cardiac_physio.tsv.gz - Field description: Name of the task.
No two tasks should have the same name.
The task label included in the filename MAY be derived from this `"TaskName"` field
by removing all non-alphanumeric or `+` characters (that is, all except those matching `[0-9a-zA-Z+]`),
and potentially replacing spaces with `+` to ease readability.
For example `"TaskName"` `"faces n-back"` or `"head nodding"` could correspond to task labels
`faces+n+back` or `facesnback` and `head+nodding` or `headnodding`, respectively.

		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_recording-respiratory_physio.tsv.gz - Field description: Name of the task.
No two tasks should have the same name.
The task label included in the filename MAY be derived from this `"TaskName"` field
by removing all non-alphanumeric or `+` characters (that is, all except those matching `[0-9a-zA-Z+]`),
and potentially replacing spaces with `+` to ease readability.
For example `"TaskName"` `"faces n-back"` or `"head nodding"` could correspond to task labels
`faces+n+back` or `facesnback` and `head+nodding` or `headnodding`, respectively.


		4 more files with the same issue

		StationName
		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.nii.gz - Field description: Institution defined name of the machine that produced the measurements.

		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz - Field description: Institution defined name of the machine that produced the measurements.


		MagneticFieldStrength
		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.nii.gz - Field description: Nominal field strength of MR magnet in Tesla.
Corresponds to [DICOM Tag 0018, 0087](http://www.dicomlookup.com/dicomtags/(0018,0087))
`Magnetic Field Strength`.

		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz - Field description: Nominal field strength of MR magnet in Tesla.
Corresponds to [DICOM Tag 0018, 0087](http://www.dicomlookup.com/dicomtags/(0018,0087))
`Magnetic Field Strength`.


		ReceiveCoilName
		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.nii.gz - Field description: Information describing the receiver coil.
Corresponds to [DICOM Tag 0018, 1250](http://www.dicomlookup.com/dicomtags/(0018,1250))
`Receive Coil Name`,
although not all vendors populate that DICOM Tag,
in which case this field can be derived from an appropriate
private DICOM field.

		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz - Field description: Information describing the receiver coil.
Corresponds to [DICOM Tag 0018, 1250](http://www.dicomlookup.com/dicomtags/(0018,1250))
`Receive Coil Name`,
although not all vendors populate that DICOM Tag,
in which case this field can be derived from an appropriate
private DICOM field.


		ReceiveCoilActiveElements
		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.nii.gz - Field description: Information describing the active/selected elements of the receiver coil.
This does not correspond to a tag in the DICOM ontology.
The vendor-defined terminology for active coil elements can go in this field.

		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz - Field description: Information describing the active/selected elements of the receiver coil.
This does not correspond to a tag in the DICOM ontology.
The vendor-defined terminology for active coil elements can go in this field.


		ScanningSequence
		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.nii.gz - Field description: Description of the type of data acquired.

		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz - Field description: Description of the type of data acquired.


		PulseSequenceDetails
		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.nii.gz - Field description: Information beyond pulse sequence type that identifies the specific pulse
sequence used (for example,
`"Standard Siemens Sequence distributed with the VB17 software"`,
`"Siemens WIP ### version #.##,"` or
`"Sequence written by X using a version compiled on MM/DD/YYYY"`).

		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz - Field description: Information beyond pulse sequence type that identifies the specific pulse
sequence used (for example,
`"Standard Siemens Sequence distributed with the VB17 software"`,
`"Siemens WIP ### version #.##,"` or
`"Sequence written by X using a version compiled on MM/DD/YYYY"`).


		WaterSuppression
		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.nii.gz - Field description: Boolean indicating whether water suppression was used prior to acquisition.

		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz - Field description: Boolean indicating whether water suppression was used prior to acquisition.


		NumberOfSpectralPoints
		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.nii.gz - Field description: The number of complex data points in each recorded transient of the detected time-domain MR
signal, equivalent to the number of points in a single spectrum.

		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz - Field description: The number of complex data points in each recorded transient of the detected time-domain MR
signal, equivalent to the number of points in a single spectrum.


		MixingTime
		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.nii.gz - Field description: In the context of a stimulated- and spin-echo 3D EPI sequence for B1+ mapping
or a stimulated-echo MRS sequence,
corresponds to the interval between spin- and stimulated-echo pulses.
In the context of a diffusion-weighted double spin-echo sequence,
corresponds to the interval between two successive diffusion sensitizing
gradients, specified in seconds.

		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz - Field description: In the context of a stimulated- and spin-echo 3D EPI sequence for B1+ mapping
or a stimulated-echo MRS sequence,
corresponds to the interval between spin- and stimulated-echo pulses.
In the context of a diffusion-weighted double spin-echo sequence,
corresponds to the interval between two successive diffusion sensitizing
gradients, specified in seconds.


		FlipAngle
		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.nii.gz - Field description: Flip angle (FA) for the acquisition, specified in degrees.
Corresponds to: [DICOM Tag 0018, 1314](http://www.dicomlookup.com/dicomtags/(0018,1314))
`Flip Angle`.
The data type number may apply to files from any MRI modality concerned with
a single value for this field, or to the files in a
[file collection](https://bids-specification.readthedocs.io/en/stable/appendices/file-collections.md)
where the value of this field is iterated using the
[`flip` entity](https://bids-specification.readthedocs.io/en/stable/appendices/entities.md#flip).

		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz - Field description: Flip angle (FA) for the acquisition, specified in degrees.
Corresponds to: [DICOM Tag 0018, 1314](http://www.dicomlookup.com/dicomtags/(0018,1314))
`Flip Angle`.
The data type number may apply to files from any MRI modality concerned with
a single value for this field, or to the files in a
[file collection](https://bids-specification.readthedocs.io/en/stable/appendices/file-collections.md)
where the value of this field is iterated using the
[`flip` entity](https://bids-specification.readthedocs.io/en/stable/appendices/entities.md#flip).


		AcquisitionVoxelSize
		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.nii.gz - Field description: An array of numbers with a length of 3, in millimeters.
This field denotes the original acquisition voxel size,
excluding any inter-slice gaps and before any interpolation or resampling
within reconstruction or image processing.
Any point spread function effects, for example due to T2-blurring,
that would decrease the effective resolution are not considered here.

		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz - Field description: An array of numbers with a length of 3, in millimeters.
This field denotes the original acquisition voxel size,
excluding any inter-slice gaps and before any interpolation or resampling
within reconstruction or image processing.
Any point spread function effects, for example due to T2-blurring,
that would decrease the effective resolution are not considered here.


		ReferenceSignal
		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.nii.gz - Field description: The path(s) to the MRS reference file(s), if present, to which the associated
MRS data file corresponds.
Contains one or more [BIDS URIs](https://bids-specification.readthedocs.io/en/stable/common-principles.md#bids-uri).

		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz - Field description: The path(s) to the MRS reference file(s), if present, to which the associated
MRS data file corresponds.
Contains one or more [BIDS URIs](https://bids-specification.readthedocs.io/en/stable/common-principles.md#bids-uri).


		NumberOfTransients
		/sub-102/ses-01/mrs/sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz - Field description: The number of single applications of the pulse sequence recorded during an MRS acquisition.


	Please visit https://neurostars.org/search?q=SIDECAR_KEY_RECOMMENDED for existing conversations about this issue.

	[WARNING] SIDECAR_FIELD_OVERRIDE Sidecar files should not override values assigned at a higher level.
		ImageType
		/sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.json - Sidecar key defined in /task-resting_bold.json overrides previous value (ORIGINAL,PRIMARY,FMRI,NONE,MAGNITUDE) from /sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.json
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json - Sidecar key defined in /task-checks_bold.json overrides previous value (ORIGINAL,PRIMARY,FMRI,NONE,MAGNITUDE) from /sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json

		2 more files with the same issue

		ImageTypeText
		/sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.json - Sidecar key defined in /task-resting_bold.json overrides previous value (ORIGINAL,PRIMARY,M,ND,NORM) from /sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.json
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json - Sidecar key defined in /task-checks_bold.json overrides previous value (ORIGINAL,PRIMARY,M,ND,NORM) from /sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json

		2 more files with the same issue

		TablePosition
		/sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.json - Sidecar key defined in /task-resting_bold.json overrides previous value (0,0,0) from /sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.json
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json - Sidecar key defined in /task-checks_bold.json overrides previous value (0,0,0) from /sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json

		2 more files with the same issue

		TaskName
		/sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.json - Sidecar key defined in /task-resting_bold.json overrides previous value (TODO: full task name for resting) from /sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.json
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json - Sidecar key defined in /task-checks_bold.json overrides previous value (TODO: full task name for checks) from /sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json

		2 more files with the same issue

		ImageOrientationPatientDICOM
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json - Sidecar key defined in /task-checks_bold.json overrides previous value (0.998603,-0.0363826,-0.038307,0.0364426,0.999335,0.000868204) from /sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-02_bold.json - Sidecar key defined in /task-checks_bold.json overrides previous value (0.998603,-0.0363826,-0.038307,0.0364426,0.999335,0.000868204) from /sub-102/ses-01/func/sub-102_ses-01_task-checks_run-02_bold.json

		ShimSetting
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json - Sidecar key defined in /task-checks_bold.json overrides previous value (1738,-9122,4433,931,-153,24,-19,27) from /sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-02_bold.json - Sidecar key defined in /task-checks_bold.json overrides previous value (1738,-9122,4433,931,-153,24,-19,27) from /sub-102/ses-01/func/sub-102_ses-01_task-checks_run-02_bold.json

		SliceTiming
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json - Sidecar key defined in /task-checks_bold.json overrides previous value (1.485,0,0.99,0.0825,1.0725,0.165,1.155,0.2475,1.2375,0.33,1.32,0.4125,1.4025,0.5775,1.5675,0.66,1.65,0.7425,1.7325,0.825,1.815,0.9075,1.8975,0.495,1.485,0,0.99,0.0825,1.0725,0.165,1.155,0.2475,1.2375,0.33,1.32,0.4125,1.4025,0.5775,1.5675,0.66,1.65,0.7425,1.7325,0.825,1.815,0.9075,1.8975,0.495) from /sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.json
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-02_bold.json - Sidecar key defined in /task-checks_bold.json overrides previous value (1.485,0,0.99,0.0825,1.0725,0.165,1.155,0.2475,1.2375,0.33,1.32,0.4125,1.4025,0.5775,1.5675,0.66,1.65,0.7425,1.7325,0.825,1.815,0.9075,1.8975,0.495,1.485,0,0.99,0.0825,1.0725,0.165,1.155,0.2475,1.2375,0.33,1.32,0.4125,1.4025,0.5775,1.5675,0.66,1.65,0.7425,1.7325,0.825,1.815,0.9075,1.8975,0.495) from /sub-102/ses-01/func/sub-102_ses-01_task-checks_run-02_bold.json

	Please visit https://neurostars.org/search?q=SIDECAR_FIELD_OVERRIDE for existing conversations about this issue.

	[WARNING] SUSPICIOUSLY_SHORT_EVENT_DESIGN The onset of the last event is less than half the total duration of the corresponding scan.
This design is suspiciously short.

		/sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_bold.nii.gz
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_bold.nii.gz

		2 more files with the same issue

	Please visit https://neurostars.org/search?q=SUSPICIOUSLY_SHORT_EVENT_DESIGN for existing conversations about this issue.

	[WARNING] TSV_ADDITIONAL_COLUMNS_UNDEFINED A TSV file has extra columns which are not defined in its associated JSON sidecar
		TODO -- fill in rows and add more tab-separated columns if desired
		/sub-101/ses-02/func/sub-101_ses-02_task-resting_run-01_events.tsv
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_events.tsv

		2 more files with the same issue

	Please visit https://neurostars.org/search?q=TSV_ADDITIONAL_COLUMNS_UNDEFINED for existing conversations about this issue.

	[WARNING] GZIP_HEADER_MTIME The gzip header contains a non-zero timestamp.
This may leak sensitive information or indicate a non-reproducible conversion process.

		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_recording-cardiac_physio.tsv.gz
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_recording-respiratory_physio.tsv.gz

		4 more files with the same issue

	Please visit https://neurostars.org/search?q=GZIP_HEADER_MTIME for existing conversations about this issue.

	[WARNING] GZIP_HEADER_FILENAME The gzip header contains a non-empty filename.
This may leak sensitive information or indicate a non-reproducible conversion process.

		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_recording-cardiac_physio.tsv.gz
		/sub-102/ses-01/func/sub-102_ses-01_task-checks_run-01_recording-respiratory_physio.tsv.gz

		4 more files with the same issue

	Please visit https://neurostars.org/search?q=GZIP_HEADER_FILENAME for existing conversations about this issue.


          Summary:                         Available Tasks:                        Available Modalities:
          73 Files, 1.62 GB                TODO: full task name for checks         MRI                  
          2 - Subjects 2 - Sessions        TODO: full task name for resting        mrs                  
                                           resting                                                      
                                           checks                                                       


```



</details>

Finally, go to your \~/bids-export directory to check your exported DICOM data and processed BIDS directory structure! 🎉

<details>

<summary>Click here to see how it should look</summary>

```bash
bnc/study-demodat/bids/
|-- CHANGES
|-- README
|-- dataset_description.json
|-- participants.json
|-- participants.tsv
|-- scans.json
|-- sourcedata
|   |-- README
|   |-- sub-101
|       |-- ses-01
|           |-- dwi
|               |-- sub-101_ses-01_acq-b1500_dir-ap_dwi.dicom.tgz
|               |-- sub-101_ses-01_acq-b1500_dir-pa_dwi.dicom.tgz
|       |-- ses-02
|           |-- anat
|               |-- sub-101_ses-02_acq-memprageRMS_T1w.dicom.tgz
|           |-- dwi
|               |-- sub-101_ses-02_acq-b1500_dir-ap_dwi.dicom.tgz
|               |-- sub-101_ses-02_acq-b1500_dir-pa_dwi.dicom.tgz
|           |-- func
|               |-- sub-101_ses-02_task-resting_run-01_bold.dicom.tgz
|   |-- sub-102
|        |-- ses-01
|           |-- anat
|               |-- sub-102_ses-01_acq-memprage_MPR_Tra_ND_T1w.dicom.tgz
|               |-- sub-102_ses-01_acq-memprage_MPR_Tra_T1w.dicom.tgz
|               |-- sub-102_ses-01_acq-memprage_MPR_Cor_ND_T1w.dicom.tgz
|               |-- sub-102_ses-01_acq-memprage_MPR_Cor_T1w.dicom.tgz
|               |-- sub-102_ses-01_acq-memprageRMS_ND_T1w.dicom.tgz
|               |-- sub-102_ses-01_acq-aascoutMPRcor_scout.dicom.tgz
|               |-- sub-102_ses-01_acq-aascoutMPRsag_scout.dicom.tgz
|               |-- sub-102_ses-01_acq-aascoutMPRtra_scout.dicom.tgz
|           |-- dwi
|               |-- sub-102_ses-01_acq-b1500_dir-pa_dwi.dicom.tgz
|               |-- sub-102_ses-01_acq-b1500_dir-ap_dwi.dicom.tgz
|           |-- fmap
|               |-- sub-102_ses-01_acq-boldGRE_phasediff.dicom.tgz
|               |-- sub-102_ses-01_acq-boldGRE_magnitude.dicom.tgz
|           |-- func
|               |-- sub-102_ses-01_task-resting_run-01_bold.dicom.tgz
|               |-- sub-102_ses-01_task-checks_run-02_bold.dicom.tgz
|               |-- sub-102_ses-01_task-checks_run-01_bold.dicom.tgz
|           |-- mrs
|               |-- sub-102_ses-01_acq-PRESS_voi-Lacc_svs.dcm
|               |-- sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.dcm
|-- sub-101
|   |-- ses-01
|       |-- dwi
|           |-- sub-101_ses-01_acq-b1500_dir-pa_dwi.json
|           |-- sub-101_ses-01_acq-b1500_dir-pa_dwi.nii.gz
|           |-- sub-101_ses-01_acq-b1500_dir-pa_dwi.bval
|           |-- sub-101_ses-01_acq-b1500_dir-pa_dwi.bvec
|           |-- sub-101_ses-01_acq-b1500_dir-ap_dwi.json
|           |-- sub-101_ses-01_acq-b1500_dir-ap_dwi.nii.gz
|           |-- sub-101_ses-01_acq-b1500_dir-ap_dwi.bval
|           |-- sub-101_ses-01_acq-b1500_dir-ap_dwi.bvec
|       |-- sub-101_ses-01_scans.tsv
|   |-- ses-02
|       |-- anat
|           |-- sub-101_ses-02_acq-memprageRMS_T1w.json
|           |-- sub-101_ses-02_acq-memprageRMS_T1w.nii.gz
|       |-- dwi
|           |-- sub-101_ses-02_acq-b1500_dir-pa_dwi.json
|           |-- sub-101_ses-02_acq-b1500_dir-pa_dwi.nii.gz
|           |-- sub-101_ses-02_acq-b1500_dir-pa_dwi.bval
|           |-- sub-101_ses-02_acq-b1500_dir-pa_dwi.bvec
|           |-- sub-101_ses-02_acq-b1500_dir-ap_dwi.json
|           |-- sub-101_ses-02_acq-b1500_dir-ap_dwi.nii.gz
|           |-- sub-101_ses-02_acq-b1500_dir-ap_dwi.bval
|           |-- sub-101_ses-02_acq-b1500_dir-ap_dwi.bvec
|       |-- func
|           |-- sub-101_ses-02_task-resting_run-01_bold.json
|           |-- sub-101_ses-02_task-resting_run-01_events.tsv
|           |-- sub-101_ses-02_task-resting_run-01_bold.nii.gz
|       |-- sub-101_ses-02_scans.tsv
|-- sub-102
|   |-- ses-01
|       |-- anat
|           |-- sub-102_ses-01_acq-memprageRMS_T1w.json
|           |-- sub-102_ses-01_acq-memprageRMS_T1w.nii.gz
|       |-- dwi
|           |-- sub-102_ses-01_acq-b1500_dir-pa_dwi.json
|           |-- sub-102_ses-01_acq-b1500_dir-pa_dwi.nii.gz
|           |-- sub-102_ses-01_acq-b1500_dir-pa_dwi.bval
|           |-- sub-102_ses-01_acq-b1500_dir-pa_dwi.bvec
|           |-- sub-102_ses-01_acq-b1500_dir-ap_dwi.json
|           |-- sub-102_ses-01_acq-b1500_dir-ap_dwi.nii.gz
|           |-- sub-102_ses-01_acq-b1500_dir-ap_dwi.bval
|           |-- sub-102_ses-01_acq-b1500_dir-ap_dwi.bvec
|       |-- fmap
|           |-- sub-102_ses-01_acq-boldGRE_magnitude1.json
|           |-- sub-102_ses-01_acq-boldGRE_magnitude2.json
|           |-- sub-102_ses-01_acq-boldGRE_phasediff.json
|           |-- sub-102_ses-01_acq-boldGRE_magnitude1.nii.gz
|           |-- sub-102_ses-01_acq-boldGRE_magnitude2.nii.gz
|           |-- sub-102_ses-01_acq-boldGRE_phasediff.nii.gz
|       |-- func
|           |-- sub-102_ses-01_task-resting_run-01_recording-cardiac_physio.json
|           |-- sub-102_ses-01_task-resting_run-01_recording-cardiac_physio.tsv.gz
|           |-- sub-102_ses-01_task-resting_run-01_recording-respiratory_physio.json
|           |-- sub-102_ses-01_task-resting_run-01_recording-respiratory_physio.tsv.gz
|           |-- sub-102_ses-01_task-checks_run-02_recording-cardiac_physio.json
|           |-- sub-102_ses-01_task-checks_run-02_recording-cardiac_physio.tsv.gz
|           |-- sub-102_ses-01_task-checks_run-02_recording-respiratory_physio.json
|           |-- sub-102_ses-01_task-checks_run-02_recording-respiratory_physio.tsv.gz
|           |-- sub-102_ses-01_task-checks_run-01_recording-cardiac_physio.json
|           |-- sub-102_ses-01_task-checks_run-01_recording-cardiac_physio.tsv.gz
|           |-- sub-102_ses-01_task-checks_run-01_recording-respiratory_physio.json
|           |-- sub-102_ses-01_task-checks_run-01_recording-respiratory_physio.tsv.gz
|           |-- sub-102_ses-01_task-checks_run-01_bold.json
|           |-- sub-102_ses-01_task-checks_run-02_bold.json
|           |-- sub-102_ses-01_task-resting_run-01_bold.json
|           |-- sub-102_ses-01_task-checks_run-01_events.tsv
|           |-- sub-102_ses-01_task-checks_run-02_events.tsv
|           |-- sub-102_ses-01_task-resting_run-01_events.tsv
|           |-- sub-102_ses-01_task-resting_run-01_bold.nii.gz
|           |-- sub-102_ses-01_task-checks_run-02_bold.nii.gz
|           |-- sub-102_ses-01_task-checks_run-01_bold.nii.gz
|       |-- mrs
|           |-- sub-102_ses-01_acq-PRESS_voi-Lacc_svs.json
|           |-- sub-102_ses-01_acq-PRESS_voi-Lacc_svs.nii.gz
|           |-- sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.json
|           |-- sub-102_ses-01_acq-PRESS_voi-Lacc_mrsref.nii.gz
|       |-- sub-102_ses-01_scans.tsv
|-- task-checks_bold.json
|-- task-motionloc_bold.json
|-- task-resting_bold.json
|-- .bidsignore

```



</details>

