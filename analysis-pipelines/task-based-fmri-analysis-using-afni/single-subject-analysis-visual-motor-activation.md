---
description: >-
  Preprocessing a single subject/session and applying a general linear model
  using AFNI
---

# Single Subject Analysis: Visual/Motor Activation

### Step 1: Download data from XNAT and automatically convert to BIDS format with xnat-tools

In this example, we will use the data from demodat2 participant 101, session 1. Running the following series of commands on the command line in Oscar will download the data we need, convert it to BIDS format, and run the BIDS validator to check for any issues. We will be using the xnat-tools Oscar utility script explained [here](../../xnat-to-bids-intro/using-oscar/oscar-utility-script/).&#x20;

First, we need to create a configuration .toml file that contains some information xnat-tools needs to download the correct data and put it where we want. Let's call this file x2b\_demodat2\_config.toml and place wherever you'd like (simplest would be your home directory). Paste the following into your .toml file, and change `mail-user` to your email address. The script will default to placing the downloaded and BIDS-converted data in a folder called "bids-export" in your home directory; if you'd like to change this location, add a new line at the bottom with your desired path, i.e.: `bids_root="/oscar/home/<yourusername>/xnat-export"`. Make sure to save this .toml file when you are done editing.&#x20;

```toml
# Configuring arguments here will override default parameters.
[slurm-args]
mail-user = "example-user@brown.edu"
mail-type = "ALL"

[xnat2bids-args]
sessions = [
    "XNAT_E01849"
    ]
# Skip scanner-derived multi-planar reconstructions & non-distortion-corrected images 
# These are used for MRS voxel placement on the scanner and will cause xnat2bids to fail. 
skipseq=["anat-t1w_acq-memprage_MPR_Cor","anat-t1w_acq-memprage_MPR_Tra","anat-t1w_acq-memprage_MPR_Tra_ND","anat-t1w_acq-memprage RMS_ND","anat-t1w_acq-memprage_MPR_Cor_ND"]
verbose=1
```

To run the xnat-tools export and BIDS conversion, change directory to `/oscar/data/bnc/shared/scripts/`. On the command line, type:

`module load anaconda`

`python run_xnat2bids.py --config ~/x2b_demodat2_config.toml`

If you named your .toml file differently or placed it somewhere other than your home directory, make sure to include the full path to your file and the correct filename. Enter your XNAT username and password when prompted.&#x20;

You should receive output that looks like this:

```
Enter XNAT Username: example-username
Enter Password: 
DEBUG: {'message': 'Argument List', 'session': 'XNAT_E01849', 'slurm_param_list': ['--time 04:00:00', '--mem 16000', '--nodes 1', '--cpus-per-task 2', '--job-name xnat2bids', '--mail-user gillian_leblanc@brown.edu', '--mail-type ALL', '--output /oscar/scratch/gleblan1/logs/%x-XNAT_E01849-%J.txt'], 'x2b_param_list': ['XNAT_E01849', '/oscar/home/gleblan1/data/Demodat2_documentation', '--user gleblan1', '--host "https://xnat.bnc.brown.edu"', '--skipseq 3 --skipseq 4 --skipseq 5 --skipseq 7 --skipseq 8 --skipseq 19 --skipseq 20 --skipseq 21', '--overwrite', '--verbose']}
DEBUG: {'message': 'Executing xnat2bids', 'session': 'XNAT_E01849', 'command': ['sbatch', '--time', '04:00:00', '--mem', '16000', '--nodes', '1', '--cpus-per-task', '2', '--job-name', 'xnat2bids', '--mail-user', 'gillian_leblanc@brown.edu', '--mail-type', 'ALL', '--output', '/oscar/scratch/gleblan1/logs/%x-XNAT_E01849-%J.txt', '--wrap', '""apptainer exec --no-home -B /oscar/home/gleblan1/data/Demodat2_documentation /oscar/data/bnc/simgs/brownbnc/xnat-tools-v1.7.2.sif xnat2bids XNAT_E01849 /oscar/home/gleblan1/data/Demodat2_documentation --user gleblan1 --pass [REDACTED] --host "https://xnat.bnc.brown.edu" --skipseq 3 --skipseq 4 --skipseq 5 --skipseq 7 --skipseq 8 --skipseq 19 --skipseq 20 --skipseq 21 --overwrite --verbose""']}
sbatch: slurm_job_submit: No partition specified, moved to batch.
sbatch: slurm_job_submit: No partition specified, moved to batch.
INFO: Launched 1 xnat2bids job
INFO: Job ID: 11854472
INFO: Launched bids-validator to check BIDS compliance
INFO: Job ID: 11854473
INFO: Processed Scans Located At: /oscar/home/example-username/bids-export
```

If you entered your email address, you should receive an email when your xnat2bids job begins, and another when it finishes.&#x20;

This will create a sourcedata folder for subject 101 within `$bids_root/bnc/study-demodat/xnat-export` and a BIDS-compatible data directory for subject 101 within `$bids_root/bnc/study-demodat/bids/`.

{% hint style="info" %}
We will call this output BIDS-compatible folder (`/oscar/home/<yourusername>/xnat-export/bnc/study-demodat/bids/` , unless you specified a different `$bids_root` location) `$bidsdir` for the remainder of the tutorial.
{% endhint %}

### Step 2: Extract stimulus timing information from stimulus presentation output files.

To make our data BIDS compatible and facilitate future data sharing, we need to create events.tsv files that correspond to each of our functional runs and contain information about each stimulus event of interest (onset time, condition, etc.). First, download the participant's data files (in our case, created by PsychoPy) and place them in the sourcedata subfolder of your BIDS directory in a subfolder named 'beh'. So, for this participant and session, the full path should be: `$bidsdir/sourcedata/sub-101/ses-01/beh`.&#x20;

{% file src="../../.gitbook/assets/sub-101_ses-01_beh.zip" %}
Demodat subject 101 session 01 behavioral data.&#x20;
{% endfile %}

Next, download our example python script make\_events.py, and run it from the command line with `python make_events_LRChx.py --bids_dir $bidsdir --subj sub-101 --sess ses-01`. For this script to run, you'll need both [numpy](https://numpy.org/install/) and [pandas](https://pandas.pydata.org/) installed in your python environment (if you're doing this on Oscar and you run `module load anaconda/latest`, you should be all set). This script will create BIDS-formatted events.tsv files corresponding to each functional run in `$bidsdir/sub-101/ses-01/func/`.&#x20;

{% file src="../../.gitbook/assets/make_events_LRChx (1).py" %}
Example python script to read in csv files created by PsychoPy and create the events.tsv files corresponding to each fMRI run
{% endfile %}

If you are unable to run this script for any reason, you can download the events.tsv output files here, and manually place them in  `$bidsdir/sub-101/ses-01/func/` .

{% file src="../../.gitbook/assets/sub-101_ses-01_eventsfiles.zip" %}

### Step 3: Convert events.tsv files into AFNI stimulus timing files

We needed to make those events.tsv files for BIDS compatibility, but in order to run our statistical analysis in AFNI, we need to transform them into .1D text files required by AFNI for specifying stimulus timing information. Instead of one file per run, as we had with the events.tsv files, here we need one file per condition (e.g. left hemifield checks or right button presses). These files are formatted to have one line per run of the task, specifying all the onset times for that condition. Since we collected two runs of the functional tasks, there should be two lines in this file. We have created an example python script make\_afni\_stimtimes\_LRChx.py, which you can run from the command line just as you did make\_events.py: `python make_afni_stimtimes_LRChx.py --bids_dir $bidsdir --subj sub-101 --sess ses-01` . This will create stimulus timing files in `$bidsdir/derivatives/afni/sub-101/ses-01/stimtimes/` .

{% file src="../../.gitbook/assets/make_afni_stimtimes_LRChx (1).py" %}
example python script to read in events.tsv files from each functional run and output the .1D stimulus timing files AFNI needs
{% endfile %}

If you are unable to run this script for any reason, you can download the .1D files here and manually place them in `$bidsdir/derivatives/afni/sub-101/ses-01/stimtimes/`.

{% file src="../../.gitbook/assets/sub-101_ses-01_stimtimes.zip" %}

### Step 4: Use afni\_proc.py to create a simple preprocessing stream and run the general linear model for the checks task

{% hint style="info" %}
To access AFNI on Oscar, type `module load afni`.
{% endhint %}

This basic example of a univariate analysis with AFNI is based on the [example 6b](https://afni.nimh.nih.gov/pub/dist/doc/program_help/afni_proc.py.html) for afni\_proc.py. The -blocks flag lists the processing blocks that will be executed, in order:&#x20;

1. tshift (slice time correction)
2. align (aligning the EPIs to the anatomical scan)
3. volreg (motion correction within each functional run)
4. blur (spatial smoothing with a 4mm FWHM smoothing kernel)
5. mask (create a "brain" mask from the functional data, restricted by the anatomy)
6. scale (scale each voxel to have a mean of 100 per run)
7. regress (build a general linear model and execute with [3dREMLfit](https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/programs/3dREMLfit_sphx.html))

**For the visual hemifield localizer regression, we use:**

`-regress_stim_times` to provide the stimulus timing files for this participant (sub-101\_checks\_left\_stimtimes.1D and sub-101\_checks\_right\_stimtimes.1D)

`-regress_stim_labels` to assign those conditions the labels of "leftchx" and "rightchx" respectively

`-regress_basis` to model each stimulus as a block lasting 12 seconds

`-regress_opts_3dD` to specify our contrasts. Here, we do a "left\_vs\_right\_chx" contrast to find voxels whose activity is greater for the left hemifield stimulation than for the right.&#x20;

**For the motor task (keypress) regression, we use:**

`-regress_stim_times` to provide the stimulus timing files for this participant (sub-101\_keypress\_left\_stimtimes.1D and sub-101\_keypress\_right\_stimtimes.1D)

`-regress_stim_labels` to assign those conditions the labels of "leftpress" and "rightpress" respectively

`-regress_basis` to model each stimulus as an instantaneous event (indicated by using AFNI's 'GAM' function)

`-regress_opts_3dD` to specify our contrasts. Here, we do a "left\_vs\_right\_press" contrast to find voxels whose activity is greater for the left index finger motor activation than for the right.&#x20;

#### Run the batch script

Copy the text in the box below into a file editor on Oscar.  Change your email in the beginning section, and change the value of the `bidsdir` variable to your own location (path should end in `/bids`). Save this script as a file called `demodat2_afniproc.sh`, and then execute it on the command line with `sbatch demodat2_afniproc.sh`. It will launch as a batch script, similar to how xnat2bids is used. You will receive an email when the job has completed.&#x20;

{% hint style="info" %}
afniproc.py will create its output folders in the directory that it is run from. To ensure all outputs are organized in the appropriate BIDS derivatives folder, the batch script will navigate to the output directory before launching afniproc.py.  Because of this, you can launch the batch script from any directory!&#x20;
{% endhint %}

This `demodat2_afniproc.sh` script will create a much longer `proc.sub-101_ses-01` tcsh script, which will be automatically executed because we included the -execute flag at the bottom of the script. Looking at the proc.sub-101\_ses-01 script is the best way to gain a deeper understanding of each of AFNI's processing steps.&#x20;

{% code title="demodat2_afniproc.sh" %}
```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -c 8
#SBATCH --mem=10G
#SBATCH --time 2:00:00
#SBATCH -J demodat2_afniproc_sub-101_ses-01
#SBATCH --output demodat2_afniproc_sub-101_ses-01-%J.txt
#SBATCH --mail-user example-user@brown.edu
#SBATCH --mail-type ALL

# This script runs GLM regressions for both the hemifield activation task (LRChx) and the motor task (key press). 

bidsdir='enter your $bidsdir path here'
subID='sub-101'
sess='ses-01'

#navigate to this subject/session's output directory
cd $bidsdir/derivatives/afni/$subID/$sess

module load afni

afni_proc.py                                                         \
    -subj_id                  ${subID}_${sess}                               \
    -out_dir                  $bidsdir/derivatives/afni/$subID/$sess/$subID.results  \
    -copy_anat                $bidsdir/$subID/$sess/anat/${subID}_${sess}_acq-memprageRMS_T1w.nii.gz        \
    -anat_has_skull           yes                                     \
    -dsets                    $bidsdir/$subID/$sess/func/*checks*nii*                 \
    -blocks                   tshift align volreg blur mask scale regress                          \
    -tcat_remove_first_trs    0                                      \
    -align_opts_aea           -cost lpc+ZZ                           \
                                -giant_move                            \
                                -check_flip                            \
    -volreg_align_to          MIN_OUTLIER                            \
    -volreg_align_e2a                                                \
    -mask_epi_anat            yes                                    \
    -blur_size                4.0                                    \
    -regress_stim_times       $bidsdir/derivatives/afni/$subID/$sess/stimtimes/${subID}_checks_left_stimtimes.1D $bidsdir/derivatives/afni/$subID/$sess/stimtimes/${subID}_checks_right_stimtimes.1D  \
                              $bidsdir/derivatives/afni/$subID/$sess/stimtimes/${subID}_keypress_left_stimtimes.1D $bidsdir/derivatives/afni/$subID/$sess/stimtimes/${subID}_keypress_right_stimtimes.1D   \
    -regress_stim_labels      leftchx rightchx leftpress rightpress                               \
    -regress_basis_multi      'BLOCK(12,1)' 'BLOCK(12,1)' 'GAM' 'GAM'                          \
    -regress_opts_3dD         -jobs 2                                \
                                -gltsym 'SYM: leftchx -rightchx'                \
                                -glt_label 1 left_vs_right_chx                       \
                                -gltsym 'SYM: leftpress -rightpress'     \
                                -glt_label 2 left_vs_right_press        \
    -regress_motion_per_run                                          \
    -regress_censor_motion    0.3                                    \
    -regress_censor_outliers  0.05                                   \
    -regress_reml_exec                                               \
    -regress_compute_fitts                                           \
    -regress_make_ideal_sum   sum_ideal.1D                           \
    -regress_est_blur_epits                                          \
    -regress_est_blur_errts                                          \
    -regress_run_clustsim     yes                                     \
    -html_review_style        pythonic                               \
    -execute
```
{% endcode %}

### Step 5: Viewing the Output

#### Visual Hemifield Localizer Task

After the `demodat2_afniproc.sh` script executes successfully, a results directory will be created: `$bidsdir/derivatives/afni/sub-101/ses-01/sub-101_results`. Start AFNI from within this directory (just type `afni` on the command line), set the underlay to `anat_final.sub-101_ses-01` and the overlay to `stats.sub-101_ses-01_REML`. In the Define Overlay menu, set the OLay to `#13 left_vs_right_chx#0_Coef` , the Thr to `#13left_vs_right_chx#0_Tstat`, and change the threshold to your desired alpha (here we've used p = 0.001). This left vs. right contrast shows regions of the brain that show a stronger BOLD response to left vs. right visual hemifield stimulation, so we can easily localize the right visual cortex and the right LGN, as expected.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-26 at 4.48.38 PM.png" alt=""><figcaption><p>Results of a general linear test contrasting left vs. right visual hemifield stimulation, in demodat subject 101 session 01</p></figcaption></figure>

#### Motor Activation (Button Press) Task&#x20;

To view the GLT results for left versus right button presses, change the overlay to `#16left_vs_right_press#0_Coef` and the Thr to `#17left_vs_right_press#0_Tstat`.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-26 at 4.52.00 PM.png" alt=""><figcaption></figcaption></figure>
