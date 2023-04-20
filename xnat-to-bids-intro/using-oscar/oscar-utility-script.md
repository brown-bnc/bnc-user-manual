# Oscar Utility Script 🆕

## Oscar Scripts: Running XNAT2BIDS

This script is a Python-based command-line tool that is designed to help neuroimaging researchers streamline the process of converting data from XNAT into BIDS format. It takes a user-specified configuration file that specifies the parameters for configuring Oscar resources as well as running the conversion pipeline, which can be customized for each individual session. The script then compiles a list of command-line arguments based on the configuration file and runs the XNAT2BIDS conversion pipeline in a Singularity container.&#x20;

### 1. Start an interactive session

#### 1.1 Desktop app on Open OnDemand&#x20;

[https://ood.ccv.brown.edu/pun/sys/dashboard](https://ood.ccv.brown.edu/pun/sys/dashboard)

Connecting via the Desktop app on Open OnDemand is a friendly way to request an graphical interactive session in Brown's supercomputer - Oscar. When you request a new Desktop session, you will be asked to specify the necessary resources. For this example, you can choose the basic job with `2 Cores and 7GB Memory`. Once logged in, you are already inside an interactive session.&#x20;

<figure><img src="../../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

Once your requested session is running, you can launch it by clicking the Launch Desktop button.

<figure><img src="../../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

At this point, simply open the terminal.

<figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

#### 1.2 SSH

To connect via SSH, you type `ssh username@ssh.ccv.brown.edu`. If this is your first time connecting via ssh, you will be asked to trust the remote computer (Oscar), your Brown credentials, and unless you are connected to VPN, you will be required to use DUO.

At this point you arrive at a login node. **We will need to start an interactive session/job** by typing

```
interact -n 2 -t 01:00:00 -m 8g
```

This starts an interactive job for one hour.

### 2.  BNC Utility Scripts

The BNC maintains a collection of helpful scripts on Oscar which can be found at: `/gpfs/data/bnc/shared/scripts/oscar-scripts` &#x20;

* **`xnat-token`** : Generate a temporary authentication token for accessing XNAT
* **`singularity-sync`** :  Syncs latest release of deployed singularity images (admin only)
* **`dicomsort`** : Renames and sorts DICOM files alphabetically
* **`run_xnat2bids`** : Launches xnat2bids DICOM to BIDS conversion pipeline&#x20;

This documentation introduces **`run_xnat2bids`** and outlines user instructions.

### 3.  Configuring Slurm and XNAT2BIDS

Before we are ready to kick off the script, it will be necessary to understand how each job is configured.  Each job consists of two essential pieces: the program and the resources it needs to successfully execute.  Some common resources that we will assign for our job are time, memory, cpus-per-task, and the number of compute nodes we want to allocate.  In this case, our program of interest will be `xnat2bids,` so we will need to configure its parameter options, as well.

{% hint style="info" %}
Previously, to run **`xnat2bids`** as a batch job, users had to provide an SBATCH script to the **`sbatch`** command. For more information on how to run batch jobs on Oscar, please refer to this link: [https://docs.ccv.brown.edu/oscar/submitting-jobs/batch](https://docs.ccv.brown.edu/oscar/submitting-jobs/batch)
{% endhint %}

To avoid the hassle of managing complex SBATCH scripts, we are leveraging the simplicity of TOML (Tom's Obvious Minimal Language) for specifying our configuration parameters.

We provide a default configuration of carefully chosen parameters that should likely never change. If you suspect your jobs will require more allocated resources than specified here, you can override those arguments in your own user-defined configuration file!

Take a look at our default configuration file `x2b_default_config.toml`:

```toml
[slurm-args]
time = "04:00:00"
mem = 16000
nodes = 1
cpus-per-task = 2
job-name = "xnat2bids"

[xnat2bids-args]
host="https://xnat.bnc.brown.edu"
```

**NOTE:**  By default, the latest version of `xnat-tools xnat2bids`, unless specified under `[xnat2bids-args]` with the following format: `version="vX.X.X"`

### 4.0 Running XNAT2BIDS (Single Session)

#### 4.1 Create Your Own Custom Config

Open a new file in your favorite text editor, and paste in the following:

```toml
[slurm-args]
mail-user = "example-user@brown.edu"
mail-type = "ALL"
```

{% hint style="info" %}
To open VSCode in an interactive desktop, open a terminal with a right click followed by selecting 'Open Terminal Here".  Next, run the command: **`module load vscode`**

To launch VSCode, run **`code`** on the command line.
{% endhint %}

Update the value of `mail-user` to be your e-mail. This will allow you to receive notifications on the status of your jobs!

For further details on all available parameter options, see Slurm's documentation here: [https://slurm.schedmd.com/sbatch.html](https://slurm.schedmd.com/sbatch.html)

{% hint style="info" %}
**NOTE:** By default, SBATCH output logs will be located at: `~/scratch/logs/`

If you would like your logs to live somewhere else, update your configuration as follows:

```toml
[slurm-args]
output="/path/to/logs/dir/%x-%J.txt"
```
{% endhint %}

#### 4.2 Update Config with XNAT2BIDS Arguments

Next, you'll need to configure what arguments to pass to `xnat2bids`, such as the session you would like to process, as well as any other arguments.

Paste the following text into your config file:

```toml
[xnat2bids-args]
sessions = ["XNAT_E00114"]
includeseq=[7, 10]
```

Here, we are setting the session to be processed as `XNAT_E00114`, which translates to session 1 of subject 5 in our [BNC demo dataset](https://xnat.bnc.brown.edu/app/action/DisplayItemAction/search\_element/xnat%3AprojectData/search\_field/xnat%3AprojectData.ID/search\_value/BNC\_DEMODAT). Notice that by defining `includeseq`, we are choosing to  process sequence "7", an anatomical T1-weighted image sequence using magnetization-prepared rapid acquisition gradient-echo, or "memprage", and sequence "10", and functional scan using the blood level oxygen dependent signal.

For a comprehensive list on all available options, see below:

{% code overflow="wrap" %}
```
sessions LIST[TEXT]: List of one or more Accession #s found on XNAT

bids_root TEXT: Root output directory for exporting the files [default: ~/bids-export/]

version TEXT: Version of xnat-tools [default: latest]

host TEXT: XNAT'sURL [default: https://xnat.bnc.brown.edu]

bidsmap-file TEXT: Bidsmap JSON file to correct sequence names

includeseq LIST[INTEGER]: Include this sequence(s) only

skipseq LIST[INTEGER]: Exclude this sequence(s) from processing

log-id TEXT: ID or suffix to append to logfile. If empty, current date is used [default: current date - MM-DD-YYYY-HH-MM-SS]

verbose INTEGER: Verbose level. This flag can be specified multiple times to increase verbosity [default: 0]

overwrite BOOLEAN: Remove directories where prior results for this session/participant [default: false]
```
{% endcode %}

{% hint style="info" %}
**NOTE:** By default, the root output directory for DICOM exports and converted BIDS files will be `/users/<your-user-name>/bids-export/`.  If you prefer a different path to your data, you can define BIDS\_ROOT in your `[xnat2bids-args]`list as following: **`bids_root="/path/to/bids-export"`**
{% endhint %}

{% hint style="info" %}
**NOTE:**  By default, `run_xnat2bids` uses the latest version of `xnat-tools xnat2bids`, unless specified under `[xnat2bids-args]` with the following format: `version="vX.X.X"`
{% endhint %}

#### 4.3  Running XNAT2BIDS Single Session

Now that you have a complete configuration file, you are ready to run the pipeline!

See the steps below ([#6.0-running-the-xnat2bids-script](oscar-utility-script.md#6.0-running-the-xnat2bids-script "mention") ) to launch with a custom config.

#### 4.4 Verify Output&#x20;

In your terminal, you should immediately see the following print statements:

```
INFO: Launched 1 job
INFO: Processed Scans Located At: /users/<your-username>/bids-export/
```

Check `~/scratch/logs/` for a new file `xnat2bids-XNAT_E00114-<JOB-ID>.txt.` The contents of that log file should look like this:

```
## SLURM PROLOG ###############################################################
##    Job ID : 9630859
##  Job Name : xnat2bids
##  Nodelist : node1319
##      CPUs : 
##  Mem/Node : 16000 MB
## Directory : /gpfs/data/bnc/shared/scripts/oscar-scripts
##   Job Started : Tue Apr 18 05:43:02 EDT 2023
###############################################################################
2023-04-18 05:43:04 node1319.oscar.ccv.brown.edu xnat_tools.xnat_utils[38480] INFO ------------------------------------------------
2023-04-18 05:43:04 node1319.oscar.ccv.brown.edu xnat_tools.xnat_utils[38480] INFO Get scans.
2023-04-18 05:43:04 node1319.oscar.ccv.brown.edu xnat_tools.xnat_utils[38480] INFO ------------------------------------------------
2023-04-18 05:43:04 node1319.oscar.ccv.brown.edu xnat_tools.bids_utils[38480] INFO bids_session_dir: /users/fmcdona4/bids-export/bnc/study-demodat/xnat-export/sub-005/ses-session1
2023-04-18 05:43:04 node1319.oscar.ccv.brown.edu xnat_tools.bids_utils[38480] INFO BIDSNAME: anat-T1w_acq-memprage
2023-04-18 05:43:04 node1319.oscar.ccv.brown.edu xnat_tools.bids_utils[38480] INFO Making scan DICOM directory /users/fmcdona4/bids-export/bnc/study-demodat/xnat-export/sub-005/ses-session1/anat-T1w_acq-memprage.
2023-04-18 05:43:04 node1319.oscar.ccv.brown.edu xnat_tools.bids_utils[38480] INFO Downloading files
2023-04-18 05:43:05 node1319.oscar.ccv.brown.edu py.warnings[38480] WARNING /usr/local/lib/python3.10/site-packages/xnat_tools/bids_utils.py:324: UserWarning: Changed DICOM HEADER[ProtocolName and SeriesDescription]:             anat-t1w_a
cq-memprage -> anat-T1w_acq-memprage             anat-t1w_acq-memprage -> anat-T1w_acq-memprage
  warnings.warn(
2023-04-18 05:44:25 node1319.oscar.ccv.brown.edu xnat_tools.bids_utils[38480] INFO Done.
2023-04-18 05:44:25 node1319.oscar.ccv.brown.edu xnat_tools.bids_utils[38480] INFO ---------------------------------
------------------------------------------------
Get project and subject information
Project: BNC_DEMODAT
Subject ID: XNAT_S00111
Session Suffix:  SESSION1
Subject label: 005
------------------------------------------------
Executing Heudiconv command: heudiconv -f reproin --bids     -o /users/fmcdona4/bids-export/bnc/study-demodat/bids     --dicom_dir_template /users/fmcdona4/bids-export//bnc/study-demodat/xnat-export/sub-{subject}/ses-{session}/*/*.dcm     
--subjects 005 --ses session1 --overwrite
INFO: Running heudiconv version 0.11.6 latest 0.12.2
INFO: Need to process 1 study sessions
INFO: PROCESSING STARTS: {'subject': '005', 'outdir': '/users/fmcdona4/bids-export/bnc/study-demodat/bids/', 'session': 'session1'}
INFO: Processing 704 dicoms
INFO: Analyzing 704 dicoms
INFO: Filtering out 0 dicoms based on their filename
INFO: Generated sequence info for 1 studies with 704 entries total
INFO: Processing 1 seqinfo entries
INFO: Doing conversion using dcm2niix
INFO: Converting /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprage_T1w (704 DICOMs) -> /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat . Converter: d
cm2niix . Output types: ('nii.gz', 'dicom')
230418-05:51:40,803 nipype.workflow INFO:
         [Node] Setting-up "convert" in "/tmp/dcm2niixjtqyf9or/convert".
INFO: [Node] Setting-up "convert" in "/tmp/dcm2niixjtqyf9or/convert".
230418-05:51:40,966 nipype.workflow INFO:
         [Node] Executing "convert" <nipype.interfaces.dcm2nii.Dcm2niix>
INFO: [Node] Executing "convert" <nipype.interfaces.dcm2nii.Dcm2niix>
230418-05:51:41,402 nipype.interface INFO:
         stdout 2023-04-18T05:51:41.402307:Chris Rorden's dcm2niiX version v1.0.20190902  (JP2:OpenJPEG) (JP-LS:CharLS) GCC5.5.0 (64-bit Linux)
INFO: stdout 2023-04-18T05:51:41.402307:Chris Rorden's dcm2niiX version v1.0.20190902  (JP2:OpenJPEG) (JP-LS:CharLS) GCC5.5.0 (64-bit Linux)
230418-05:51:41,402 nipype.interface INFO:
         stdout 2023-04-18T05:51:41.402307:Found 704 DICOM file(s)
INFO: stdout 2023-04-18T05:51:41.402307:Found 704 DICOM file(s)
230418-05:51:41,402 nipype.interface INFO:
         stdout 2023-04-18T05:51:41.402307:Slices not stacked: echo varies (TE 1.69, 7.27; echo 1, 4). Use 'merge 2D slices' option to force stacking
INFO: stdout 2023-04-18T05:51:41.402307:Slices not stacked: echo varies (TE 1.69, 7.27; echo 1, 4). Use 'merge 2D slices' option to force stacking
230418-05:51:41,402 nipype.interface INFO:
         stdout 2023-04-18T05:51:41.402307:Convert 176 DICOM as /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprage_T1w_heudiconv810_e1 (256x256x176x1)
INFO: stdout 2023-04-18T05:51:41.402307:Convert 176 DICOM as /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprage_T1w_heudiconv810_e1 (256x256x176x1)
230418-05:51:42,664 nipype.interface INFO:
         stdout 2023-04-18T05:51:42.664674:Convert 176 DICOM as /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprage_T1w_heudiconv810_e4 (256x256x176x1)
INFO: stdout 2023-04-18T05:51:42.664674:Convert 176 DICOM as /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprage_T1w_heudiconv810_e4 (256x256x176x1)
230418-05:51:43,933 nipype.interface INFO:
         stdout 2023-04-18T05:51:43.933424:Convert 176 DICOM as /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprage_T1w_heudiconv810_e3 (256x256x176x1)
INFO: stdout 2023-04-18T05:51:43.933424:Convert 176 DICOM as /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprage_T1w_heudiconv810_e3 (256x256x176x1)
230418-05:51:45,200 nipype.interface INFO:
         stdout 2023-04-18T05:51:45.200109:Convert 176 DICOM as /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprage_T1w_heudiconv810_e2 (256x256x176x1)
INFO: stdout 2023-04-18T05:51:45.200109:Convert 176 DICOM as /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprage_T1w_heudiconv810_e2 (256x256x176x1)
230418-05:51:46,420 nipype.interface INFO:
         stdout 2023-04-18T05:51:46.420417:Conversion required 5.376744 seconds (5.369291 for core code).
INFO: stdout 2023-04-18T05:51:46.420417:Conversion required 5.376744 seconds (5.369291 for core code).
230418-05:51:46,443 nipype.workflow INFO:
         [Node] Finished "convert", elapsed time 5.410614s.
INFO: [Node] Finished "convert", elapsed time 5.410614s.
WARNING: Failed to find task field in /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprage_echo-1_T1w.json.
WARNING: Failed to find task field in /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprage_echo-2_T1w.json.
WARNING: Failed to find task field in /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprage_echo-3_T1w.json.
WARNING: Failed to find task field in /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprage_echo-4_T1w.json.
WARNING: For now not embedding BIDS and info generated .nii.gz itself since sequence produced multiple files
INFO: Adding "IntendedFor" to the fieldmaps in /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1.
WARNING: We cannot add the IntendedFor field: no fmap/ in /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session1
INFO: Populating template files under /users/fmcdona4/bids-export/bnc/study-demodat/bids/
INFO: PROCESSING DONE: {'subject': '005', 'outdir': '/users/fmcdona4/bids-export/bnc/study-demodat/bids/', 'session': 'session1'}
```

### 5.0 Running XNAT2BIDS (Multi-Session)

#### 5.1 Adding Sessions to Your Config&#x20;

To process multiple sessions simultaneously, you only need to add those desired sessions to your config file's `sessions` list.&#x20;

```toml
[slurm-args]
mail-user = "example-user@brown.edu"
mail-type = "ALL"

[xnat2bids-args]
sessions = [
    "XNAT_E00080", 
    "XNAT_E00114",  
    "XNAT_E00152"
    ]
skipseq=[6]
overwrite=true
verbose=0
```

**NOTE:**  Here, `overwrite=true` will tell `xnat2bids` to reprocess any existing session exports specified in your config file.  Enabling the `verbose=1` flag will turn on DEBUG logging for your script and signal `xnat2bids` to output more detailed printing to your logs.

#### 5.2 Define Custom Parameters for Each Session

There may be the case in which you would like to add new arguments or override default parameters for processing a given session—for instance, defining logging verbosity levels or including certain sequences.&#x20;

Add the following to the bottom of your config file:

```toml
[XNAT_E00080]
includeseq=[19, 21]

[XNAT_E00114]
includeseq=[7,8,11,14]
verbose=2

[XNAT_E00152]
includeseq=[7,8,9,10,11]
verbose=1
```

**NOTE:** The section name must match an entry in your `sessions` list.  Each session will inherit all default parameters and those specified under `[xnat2bids-args]`, overriding when necessary.

#### 5.3 Running XNAT2BIDS Multi-Session

Now that you have a complete configuration file, you are ready to run the pipeline!

See the steps below ([#6.0-running-the-xnat2bids-script](oscar-utility-script.md#6.0-running-the-xnat2bids-script "mention") ) to launch with a custom config.

#### 5.4 Verify Output

In your terminal, you should immediately see the following print statements:

{% code overflow="wrap" lineNumbers="true" %}
```
DEBUG: {'message': 'Argument List', 'session': 'XNAT_E00114', 'slurm_param_list': ['--time 04:00:00', '--mem 16000', '--nodes 1', '--cpus-per-task 2', '--job-name xnat2bids', '--mail-user example-user@brown.edu', '--mail-type ALL', '--output /gpfs/scratch/fmcdona4/logs/%x-XNAT_E00114-%J.txt'], 'x2b_param_list': ['XNAT_E00114', '/users/fmcdona4/bids-export/', '--host https://xnat.bnc.brown.edu', '--user fmcdona4', '--skipseq 6', '--overwrite', '--verbose', '--verbose', '--includeseq 7 --includeseq 8 --includeseq 11 --includeseq 14']}
DEBUG: {'message': 'Argument List', 'session': 'XNAT_E00152', 'slurm_param_list': ['--time 04:00:00', '--mem 16000', '--nodes 1', '--cpus-per-task 2', '--job-name xnat2bids', '--mail-user example-user@brown.edu', '--mail-type ALL', '--output /gpfs/scratch/fmcdona4/logs/%x-XNAT_E00152-%J.txt'], 'x2b_param_list': ['XNAT_E00152', '/users/fmcdona4/bids-export/', '--host https://xnat.bnc.brown.edu', '--user fmcdona4', '--skipseq 6', '--overwrite', '--verbose', '--includeseq 7 --includeseq 8 --includeseq 9 --includeseq 10 --includeseq 11']}
DEBUG: {'message': 'Executing xnat2bids', 'session': 'XNAT_E00114', 'command': ['sbatch', '-Q', '--time', '04:00:00', '--mem', '16000', '--nodes', '1', '--cpus-per-task', '2', '--job-name', 'xnat2bids', '--mail-user', 'example-user@brown.edu', '--mail-type', 'ALL', '--output', '/gpfs/scratch/fmcdona4/logs/%x-XNAT_E00114-%J.txt', '--wrap', 'apptainer', 'exec', '--no-home', '-B', '/users/fmcdona4/bids-export/', '/gpfs/data/bnc/simgs/brownbnc/xnat-tools-v1.1.1.sif', 'xnat2bids', '[XNAT_E00114,', '/users/fmcdona4/bids-export/,', '--host,', 'https://xnat.bnc.brown.edu,', '--user,', 'fmcdona4,', '--skipseq,', '6,', '--overwrite,', '--verbose,', '--verbose,', '--includeseq,', '7,', '--includeseq,', '8,', '--includeseq,', '11,', '--includeseq,', '14]']}
DEBUG: {'message': 'Executing xnat2bids', 'session': 'XNAT_E00152', 'command': ['sbatch', '-Q', '--time', '04:00:00', '--mem', '16000', '--nodes', '1', '--cpus-per-task', '2', '--job-name', 'xnat2bids', '--mail-user', 'example-user@brown.edu', '--mail-type', 'ALL', '--output', '/gpfs/scratch/fmcdona4/logs/%x-XNAT_E00152-%J.txt', '--wrap', 'apptainer', 'exec', '--no-home', '-B', '/users/fmcdona4/bids-export/', '/gpfs/data/bnc/simgs/brownbnc/xnat-tools-v1.1.1.sif', 'xnat2bids', '[XNAT_E00152,', '/users/fmcdona4/bids-export/,', '--host,', 'https://xnat.bnc.brown.edu,', '--user,', 'fmcdona4,', '--skipseq,', '6,', '--overwrite,', '--verbose,', '--includeseq,', '7,', '--includeseq,', '8,', '--includeseq,', '9,', '--includeseq,', '10,', '--includeseq,', '11]']}
INFO: Launched 3 jobs
INFO: Processed Scans Located At: /users/fmcdona4/bids-export/
```
{% endcode %}

Check `/gpfs/scratch/<your-username>/logs/` for a three new log files

* `xnat2bids-XNAT_E00114-<JOB-ID>.txt`&#x20;
* `xnat2bids-XNAT_E00080-<JOB-ID>.txt`
* `xnat2bids-XNAT_E00152-<JOB-ID>.txt`&#x20;

The contents of each log should look similar to this:

```
## SLURM PROLOG ###############################################################
##    Job ID : 9630936
##  Job Name : xnat2bids
##  Nodelist : node1322
##      CPUs : 
##  Mem/Node : 16000 MB
## Directory : /gpfs/data/bnc/shared/scripts/oscar-scripts
##   Job Started : Tue Apr 18 06:25:24 EDT 2023
###############################################################################
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu xnat_tools.bids_utils[243475] INFO Removing existing xnat-export session directory /users/fmcdona4/bids-export/bnc/study-demodat/xnat-export/sub-005/ses-session2
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu xnat_tools.bids_utils[243475] INFO Making output xnat-export session directory /users/fmcdona4/bids-export/bnc/study-demodat/xnat-export/sub-005/ses-session2
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu xnat_tools.xnat_utils[243475] INFO ------------------------------------------------
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu xnat_tools.xnat_utils[243475] INFO Get scans.
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu urllib3.connectionpool[243475] DEBUG https://xnat.bnc.brown.edu:443 "GET /data/experiments/XNAT_E00152/scans?format=json HTTP/1.1" 200 None
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu xnat_tools.xnat_utils[243475] DEBUG Found scans 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22.
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu xnat_tools.xnat_utils[243475] DEBUG Series descriptions anat-scout_acq-localizer, anat-scout_acq-aascout, anat-scout_acq-aascout_MPR_sag, anat-scout_acq-aascout_MPR_cor, anat-scout_acq-aasco
ut_MPR_tra, anat-t1w_acq-memprage, anat-t1w_acq-memprage RMS, fmap_acq-boldGRE, fmap_acq-boldGRE, func-bold_task-checks_run+, func-bold_task-checks_run+, func-bold_task-motionloc, func-bold_task-resting, dwi_acq-b1500_dir-ap_SBRef, dwi_acq
-b1500_dir-ap, dwi_acq-b1500_dir-ap_TENSOR, fmap_acq-diffSE_dir-ap, dwi_acq-b1500_dir-pa_SBRef, dwi_acq-b1500_dir-pa, dwi_acq-b1500_dir-pa_TENSOR, fmap_acq-diffSE_dir-pa
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu xnat_tools.xnat_utils[243475] INFO ------------------------------------------------
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu urllib3.connectionpool[243475] DEBUG https://xnat.bnc.brown.edu:443 "GET /data/experiments/XNAT_E00152/scans/7/resources?format=json HTTP/1.1" 200 None
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu xnat_tools.bids_utils[243475] DEBUG Found DICOM resources: [{'file_count': '176', 'xnat_abstractresource_id': '12212', 'cat_desc': 'anat-t1w_acq-memprage RMS', 'cat_id': '7', 'format': 'DICO
M', 'label': 'DICOM', 'category': 'scans', 'element_name': 'xnat:resourceCatalog', 'file_size': '50195658', 'content': 'RAW', 'tags': ''}]
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu xnat_tools.bids_utils[243475] INFO bids_session_dir: /users/fmcdona4/bids-export/bnc/study-demodat/xnat-export/sub-005/ses-session2
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu xnat_tools.bids_utils[243475] INFO BIDSNAME: anat-T1w_acq-memprageRMS
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu xnat_tools.bids_utils[243475] INFO Making scan DICOM directory /users/fmcdona4/bids-export/bnc/study-demodat/xnat-export/sub-005/ses-session2/anat-T1w_acq-memprageRMS.
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu urllib3.connectionpool[243475] DEBUG https://xnat.bnc.brown.edu:443 "GET /data/experiments/XNAT_E00152/scans/7/resources/?format=json HTTP/1.1" 200 None
2023-04-18 06:25:25 node1322.oscar.ccv.brown.edu xnat_tools.bids_utils[243475] DEBUG resource label: DICOM
2023-04-18 06:25:26 node1322.oscar.ccv.brown.edu urllib3.connectionpool[243475] DEBUG https://xnat.bnc.brown.edu:443 "GET /data/experiments/XNAT_E00152/scans/7/resources/DICOM/files?format=json HTTP/1.1" 200 None
2023-04-18 06:25:26 node1322.oscar.ccv.brown.edu urllib3.connectionpool[243475] DEBUG https://xnat.bnc.brown.edu:443 "GET /data/experiments/XNAT_E00152/scans/7/resources/DICOM/files?format=json&locator=absolutePath HTTP/1.1" 200 None
2023-04-18 06:25:26 node1322.oscar.ccv.brown.edu xnat_tools.bids_utils[243475] INFO Downloading files
2023-04-18 06:25:26 node1322.oscar.ccv.brown.edu urllib3.connectionpool[243475] DEBUG https://xnat.bnc.brown.edu:443 "GET /data/experiments/XNAT_E00152/scans/7/resources/12212/files/1.3.12.2.1107.5.2.43.67050.30000022072412521308100000043-
7-103-a7opal.dcm HTTP/1.1" 200 285202
2023-04-18 06:25:26 node1322.oscar.ccv.brown.edu xnat_tools.xnat_utils[243475] DEBUG Downloaded remote file 1.3.12.2.1107.5.2.43.67050.30000022072412521308100000043-7-103-a7opal.dcm.
2023-04-18 06:25:26 node1322.oscar.ccv.brown.edu py.warnings[243475] WARNING /usr/local/lib/python3.10/site-packages/xnat_tools/bids_utils.py:324: UserWarning: Changed DICOM HEADER[ProtocolName and SeriesDescription]:             anat-t1w_
acq-memprage -> anat-T1w_acq-memprageRMS             anat-t1w_acq-memprage RMS -> anat-T1w_acq-memprageRMS
  warnings.warn(
...
-----------------------------------------------
Get project and subject information
Project: BNC_DEMODAT
Subject ID: XNAT_S00111
Session Suffix:  SESSION2
Subject label: 005
------------------------------------------------
************************
Overwrite - Removing heudi session directory /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session2
Overwrite - Removing sourcedata session directory /users/fmcdona4/bids-export/bnc/study-demodat/bids/sourcedata/sub-005/ses-session2
Overwrite - Removing hidden session directory /users/fmcdona4/bids-export/bnc/study-demodat/bids/.heudiconv/005/ses-session2
Executing Heudiconv command: heudiconv -f reproin --bids     -o /users/fmcdona4/bids-export/bnc/study-demodat/bids     --dicom_dir_template /users/fmcdona4/bids-export//bnc/study-demodat/xnat-export/sub-{subject}/ses-{session}/*/*.dcm  
INFO: Adding "IntendedFor" to the fieldmaps in /users/fmcdona4/bids-export/bnc/study-demodat/bids/sub-005/ses-session2.
INFO: Populating template files under /users/fmcdona4/bids-export/bnc/study-demodat/bids/
INFO: PROCESSING DONE: {'subject': '005', 'outdir': '/users/fmcdona4/bids-export/bnc/study-demodat/bids/', 'session': 'session2'}
Done with Heudiconv BIDS Convesion.
```

#### 5.5 Check BIDS Processed Data

Go to your \~/bids-export directory to check your exported DICOM data and processed BIDS directory structure!  It should look like this:

```
 |-bnc
 | |-study-demodat
 | | |-bids
 | | | |-README
 | | | |-sub-005
 | | | | |-ses-session1
 | | | | | |-fmap
 | | | | | | |-sub-005_ses-session1_acq-boldGRE_magnitude2.nii.gz
 | | | | | | |-sub-005_ses-session1_acq-boldGRE_magnitude1.json
 | | | | | | |-sub-005_ses-session1_acq-boldGRE_magnitude1.nii.gz
 | | | | | | |-sub-005_ses-session1_acq-boldGRE_magnitude2.json
 | | | | | |-anat
 | | | | | | |-sub-005_ses-session1_acq-memprageRMS_T1w.json
 | | | | | | |-sub-005_ses-session1_acq-memprageRMS_T1w.nii.gz
 | | | | | |-func
 | | | | | | |-sub-005_ses-session1_task-checks_run-01_bold.json
 | | | | | | |-sub-005_ses-session1_task-checks_run-01_events.tsv
 | | | | | | |-sub-005_ses-session1_task-checks_run-01_bold.nii.gz
 | | | | | |-dwi
 | | | | | | |-sub-005_ses-session1_acq-b1500_dir-ap_sbref.nii.gz
 | | | | | | |-sub-005_ses-session1_acq-b1500_dir-ap_sbref.json
 | | | | | |-sub-005_ses-session1_scans.tsv
 | | | | |-ses-session2
 | | | | | |-fmap
 | | | | | | |-sub-005_ses-session2_acq-boldGRE_phasediff.nii.gz
 | | | | | | |-sub-005_ses-session2_acq-boldGRE_magnitude1.json
 | | | | | | |-sub-005_ses-session2_acq-boldGRE_magnitude2.json
 | | | | | | |-sub-005_ses-session2_acq-boldGRE_phasediff.json
 | | | | | | |-sub-005_ses-session2_acq-boldGRE_magnitude2.nii.gz
 | | | | | | |-sub-005_ses-session2_acq-boldGRE_magnitude1.nii.gz
 | | | | | |-anat
 | | | | | | |-sub-005_ses-session2_acq-memprageRMS_T1w.json
 | | | | | | |-sub-005_ses-session2_acq-memprageRMS_T1w.nii.gz
 | | | | | |-func
 | | | | | | |-sub-005_ses-session2_task-checks_run-01_events.tsv
 | | | | | | |-sub-005_ses-session2_task-checks_run-01_bold.json
 | | | | | | |-sub-005_ses-session2_task-checks_run-01_bold.nii.gz
 | | | | | |-sub-005_ses-session2_scans.tsv
 | | | |-scans.json
 | | | |-participants.tsv
 | | | |-sourcedata
 | | | | |-README
 | | | | |-sub-005
 | | | | | |-ses-session1
 | | | | | | |-fmap
 | | | | | | | |-sub-005_ses-session1_acq-boldGRE_magnitude.dicom.tgz
 | | | | | | |-anat
 | | | | | | | |-sub-005_ses-session1_acq-memprageRMS_T1w.dicom.tgz
 | | | | | | |-func
 | | | | | | | |-sub-005_ses-session1_task-checks_run-01_bold.dicom.tgz
 | | | | | | |-dwi
 | | | | | | | |-sub-005_ses-session1_acq-b1500_dir-ap_sbref.dicom.tgz
 | | | | | |-ses-session2
 | | | | | | |-fmap
 | | | | | | | |-sub-005_ses-session2_acq-boldGRE_phasediff.dicom.tgz
 | | | | | | | |-sub-005_ses-session2_acq-boldGRE_magnitude.dicom.tgz
 | | | | | | |-anat
 | | | | | | | |-sub-005_ses-session2_acq-memprageRMS_T1w.dicom.tgz
 | | | | | | |-func
 | | | | | | | |-sub-005_ses-session2_task-checks_run-01_bold.dicom.tgz
 | | | | |-sub-004
 | | | | | |-ses-01
 | | | | | | |-fmap
 | | | | | | | |-sub-004_ses-01_acq-diffSE_dir-pa_epi.dicom.tgz
 | | | | | | |-dwi
 | | | | | | | |-sub-004_ses-01_acq-b1500_dir-pa_dwi.dicom.tgz
 | | | |-dataset_description.json
 | | | |-task-checks_bold.json
 | | | |-participants.json
 | | | |-.heudiconv
 | | | | |-004
 | | | | | |-ses-01
 | | | | | | |-info
 | | | | | | | |-004_ses-01.edit.txt
 | | | | | | | |-heuristic.py
 | | | | | | | |-004_ses-01.auto.txt
 | | | | | | | |-filegroup_ses-01.json
 | | | | | | | |-dicominfo_ses-01.tsv
 | | | | |-005
 | | | | | |-ses-session1
 | | | | | | |-info
 | | | | | | | |-heuristic.py
 | | | | | | | |-filegroup_ses-session1.json
 | | | | | | | |-dicominfo_ses-session1.tsv
 | | | | | | | |-005_ses-session1.auto.txt
 | | | | | | | |-005_ses-session1.edit.txt
 | | | | | |-ses-session2
 | | | | | | |-info
 | | | | | | | |-dicominfo_ses-session2.tsv
 | | | | | | | |-heuristic.py
 | | | | | | | |-filegroup_ses-session2.json
 | | | | | | | |-005_ses-session2.edit.txt
 | | | | | | | |-005_ses-session2.auto.txt
 | | | |-sub-004
 | | | | |-ses-01
 | | | | | |-fmap
 | | | | | | |-sub-004_ses-01_acq-diffSE_dir-pa_epi.json
 | | | | | | |-sub-004_ses-01_acq-diffSE_dir-pa_epi.nii.gz
 | | | | | |-sub-004_ses-01_scans.tsv
 | | | | | |-dwi
 | | | | | | |-sub-004_ses-01_acq-b1500_dir-pa_dwi.bvec
 | | | | | | |-sub-004_ses-01_acq-b1500_dir-pa_dwi.bval
 | | | | | | |-sub-004_ses-01_acq-b1500_dir-pa_dwi.json
 | | | | | | |-sub-004_ses-01_acq-b1500_dir-pa_dwi.nii.gz
 | | | |-CHANGES
```

### 6.0  Running the XNAT2BIDS Script

#### 6.1 Load Anaconda Module Into Environment

From the command line, run the following:

```
module load anaconda/latest
```

#### 6.2 Running with Defaults Only

If the default values for resource allocation are suitable and you do not need to pass any specific arguments to `xnat2bids`, you may run the script as follows:

```
python run_xnat2bids.py
```

Since, by default, no sessions are flagged for processing, you will immediately be prompted to enter a Session ID to proceed.  If you would like to process multiple sessions simultaneously, you can enter them as a comma-separated string.  Here's an example:

```
Enter Session(s) (comma separated): XNAT_E00080, XNAT_E00114,  XNAT_E00152
```

After your jobs have completed, you can find all DICOM export and BIDS output data at the following location: `/gpfs/scratch/<your_username>/bids-export/`

Likewise, logs can be found at `/gpfs/scratch/<your_username>/logs/` under the following format: `xnat2bids-<session-id>-<array-job-id>.txt`

#### 6.3 Running with Custom Configuration

To load a custom parameters, use `--config` to specify your custom configuration file.

```
python run_xnat2bids.py --config <example_user_config.toml> 
```

**NOTE:** For helpful debugging statements containing the executed command and argument lists to be printed to your terminal, make sure `verbose >= 1` in your configuration's `[xnat2bids-args]` list.

### 7.0 Validate the BIDS output

After successfully running `run_xnat2bids.py` you'll need to make sure that BIDS validation passes. This process is explained in the [BIDS Validation Section](../bids-validation/)

#### 7.1 Running BIDS-Validator

Run the following command:

`singularity exec --no-home -B ~/bids-export/bnc/study-demodat/bids /gpfs/data/bnc/simgs/bids/validator-latest.sif bids-validator ~/bids-export/bnc/study-demodat/bids`

#### 7.2 Verify Output

Validate no `ERR:` statements have been printed to your console. You should see the following summary:

```
Summary:                  Available Tasks:                       Available Modalities: 
38 Files, 343.22MB        checks                                 MRI                   
2 - Subjects              TODO: full task name for checks                              
3 - Sessions                                                                           
```
