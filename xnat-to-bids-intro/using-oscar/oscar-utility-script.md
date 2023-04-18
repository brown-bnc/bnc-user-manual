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

The BNC maintains a collection of helpful scripts on Oscar which can be found at: `/gpfs/data/bnc/shared/scripts/` &#x20;

* **`xnat-token`** : Generate a temporary authentication token for accessing XNAT
* **`singularity-sync`** :  Syncs latest release of deployed singularity images (admin only)
* **`dicomsort`** : Renames and sorts DICOM files alphabetically
* **`run_xnat2bids`** : Launches xnat2bids DICOM to BIDS conversion pipeline&#x20;

This documentation introduces **`run_xnat2bids`** and details user instructions.

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

Update the value of `mail-user` to be your e-mail. This will allow you to receive notifications on the status of your jobs!

For further details on all available parameter options, see Slurm's documentation here: [https://slurm.schedmd.com/srun.html](https://slurm.schedmd.com/srun.html).

#### 4.2 Update Config with XNAT2BIDS Arguments

Next, you'll need to configure what arguments to pass to `xnat2bids`, such as the session you would like to process, as well as any other arguments.

Paste the following text into your config file:

```toml
[xnat2bids-args]
sessions = ["XNAT_E00114"]
includeseq=[6]
```

Here, we are setting the session to be processed as `XNAT_E00114`, which translates to session 1 of subject 5 in our [BNC demo dataset](https://xnat.bnc.brown.edu/app/action/DisplayItemAction/search\_element/xnat%3AprojectData/search\_field/xnat%3AprojectData.ID/search\_value/BNC\_DEMODAT). Notice that by defining `includeseq`, we are choosing to only process sequence "6", an anatomical T1-weighted image sequence using magnetization-prepared rapid acquisition gradient-echo, or "memprage", for short.

For a comprehensive list on all available options, see our [XNAT Tools documentation](https://brown-bnc.github.io/xnat-tools/1.1.1/xnat2bids/).

{% hint style="info" %}
By default, the root output directory for DICOM exports and converted BIDS files will be `/users/<your-user-name>/bids-export/`.  If you prefer a different path to your data, you can define BIDS\_ROOT in your `[xnat2bids-args]`list as following: **`bids_root="/path/to/bids-export"`**
{% endhint %}

#### 4.3  Running XNAT2BIDS SIngle Session

Now that you have a complete configuration file, you are ready to run the pipeline!

See the steps below ([#6.0-running-the-xnat2bids-script](oscar-utility-script.md#6.0-running-the-xnat2bids-script "mention") ) to launch with a custom config.

#### 4.4 Verify Output&#x20;

In your terminal, you should immediately see the following print statements:

```
INFO: Launched 1 job
INFO: Processed Scans Located At: /users/<your-username>/bids-export/
```

Check `/gpfs/scratch/<your-username>/logs/` for a new file `xnat2bids-XNAT_E00114-<JOB-ID>.txt.` The contents of that log file should look like this:

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
[xnat2bids-args]
sessions = [
    "XNAT_E00080", 
    "XNAT_E00114",  
    "XNAT_E00152",
    ]
overwrite=true
skipseq=[6]
verbose=1
```

**NOTE:**  Here, `overwrite=true` will tell `xnat2bids` to reprocess any existing session exports specified in your config file.  Enabling the `verbose=1` flag will 1) turn on DEBUG logging for your script and 2) signal `xnat2bids` to output more detailed printing to your logs.

#### 5.2 Define Custom Parameters for Each Session

There may be the case in which you would like to add new arguments or override default parameters for processing a given session—for instance, defining logging verbosity levels or including certain sequences.&#x20;

Add the following to the bottom of your config file:

```toml
[XNAT_E00152]
includeseq=[7,8,9,10,11]
verbose=1

[XNAT_E00114]
verbose=2
```

**NOTE:** The section name must match an entry in your `sessions` list.  Each session will inherit all default parameters and those specified under `[xnat2bids-args]`, overriding when necessary.

#### 5.3 Running XNAT2BIDS Multi-Session

Now that you have a complete configuration file, you are ready to run the pipeline!

See the steps below ([#6.0-running-the-xnat2bids-script](oscar-utility-script.md#6.0-running-the-xnat2bids-script "mention") ) to launch with a custom config.

#### 5.4 Verify Output

In your terminal, you should immediately see the following print statements:

```
DEBUG: {'message': 'Argument List', 'session': 'XNAT_E00114', 'slurm_param_list': ['--time 04:00:00', '--mem 16000', '--nodes 1', '--cpus-per-task 2', '--job-name xnat2bids', '--mail-user ford_mcdonald@brown.edu', '--mail-type ALL', '--out
put /gpfs/scratch/fmcdona4/logs/%x-XNAT_E00114-%J.txt'], 'x2b_param_list': ['XNAT_E00114', '/users/fmcdona4/bids-export/', '--host https://xnat.bnc.brown.edu', '--user fmcdona4', '--overwrite', '--verbose', '--
verbose', '--skipseq 6']}
DEBUG: {'message': 'Argument List', 'session': 'XNAT_E00152', 'slurm_param_list': ['--time 04:00:00', '--mem 16000', '--nodes 1', '--cpus-per-task 2', '--job-name xnat2bids', '--mail-user ford_mcdonald@brown.edu', '--mail-type ALL', '--out
put /gpfs/scratch/fmcdona4/logs/%x-XNAT_E00152-%J.txt'], 'x2b_param_list': ['XNAT_E00152', '/users/fmcdona4/bids-export/', '--host https://xnat.bnc.brown.edu', '--user fmcdona4', '--overwrite', '--verbose', '--
skipseq 6', '--includeseq 7 --includeseq 8 --includeseq 9 --includeseq 10 --includeseq 11']}
DEBUG: {'message': 'Executing xnat2bids', 'session': 'XNAT_E00114', 'command': ['sbatch', '-Q', '--time', '04:00:00', '--mem', '16000', '--nodes', '1', '--cpus-per-task', '2', '--job-name', 'xnat2bids', '--mail-user', 'ford_mcdonald@brown.
edu', '--mail-type', 'ALL', '--output', '/gpfs/scratch/fmcdona4/logs/%x-XNAT_E00114-%J.txt', '--wrap', '$(cat << EOF #!/bin/sh\n             apptainer exec --no-home -B /users/fmcdona4/bids-export/ /gpfs/data/bnc/simgs/brownbnc/xnat-tools-
v1.1.1.sif             xnat2bids XNAT_E00114 /users/fmcdona4/bids-export/ --host https://xnat.bnc.brown.edu --user fmcdona4 --overwrite --verbose --verbose --skipseq 6\nEOF\n)']}
DEBUG: {'message': 'Executing xnat2bids', 'session': 'XNAT_E00152', 'command': ['sbatch', '-Q', '--time', '04:00:00', '--mem', '16000', '--nodes', '1', '--cpus-per-task', '2', '--job-name', 'xnat2bids', '--mail-user', 'ford_mcdonald@brown.
edu', '--mail-type', 'ALL', '--output', '/gpfs/scratch/fmcdona4/logs/%x-XNAT_E00152-%J.txt', '--wrap', '$(cat << EOF #!/bin/sh\n             apptainer exec --no-home -B /users/fmcdona4/bids-export/ /gpfs/data/bnc/simgs/brownbnc/xnat-tools-
v1.1.1.sif             xnat2bids XNAT_E00152 /users/fmcdona4/bids-export/ --host https://xnat.bnc.brown.edu --user fmcdona4 --overwrite --verbose --skipseq 6 --includeseq 7 --includeseq 8 --includeseq 9 --includes
eq 10 --includeseq 11\nEOF\n)']}
INFO: Launched 3 jobs
INFO: Processed Scans Located At: /users/fmcdona4/bids-export/
```

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

### 6.0  Running the XNAT2BIDS Script

#### 6.1 Load Anaconda Module Into Environment

From the command line, run the following:

```
module load anaconda/2022.05
```

#### 6.2 Running with Defaults Only

If the default values for resource allocation are suitable and you do not need to pass any specific arguments to `xnat2bids`, you may run the script as follows:

```
python run_xnat2bids.py
```

Since, by default, no sessions are flagged for processing, you will immediately be prompted to enter a Session ID to proceed.  If you would like to processing multiple sessions, you can enter them as a comma-separated string.  Here's an example:

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

`singularity exec /gpfs/data/bnc/simgs/bids/validator-latest.sif bids-validator ./users/<your-username>/bids-export/bnc/study-demodat/bids`

#### 7.2 Verify Output

Validate no `ERR:` statements have been printed to your console. You should see the following summary:

```
Summary:                 Available Tasks:                          Available Modalities: 
103 Files, 1.97GB        checks                                    MRI                   
2 - Subjects             resting                                                         
3 - Sessions             motionloc                                                       
                         TODO: full task name for checks                                 
                         TODO: full task name for motionloc                              
                         TODO: full task name for resting     
```
