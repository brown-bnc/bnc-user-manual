---
description: Preprocessing and applying a general linear model using AFNI
---

# Basic analysis example: checks task

This is a very simple visual task, with alternating 12s blocks of flashing checkerboard stimuli in the left and right visual hemifields. Because of the contralateral organization of visual cortex, we can identify the right visual cortex by selecting voxels that prefer stimulation on the left side of visual space, and vice versa. Here, we provide a bare-bones example using the [AFNI](https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/index.html) software package.&#x20;

#### Step 1: Download data from XNAT and automatically convert to BIDS format with xnat-tools

In this example, we will use the data from demodat participant 005, session 1. Running the following series of commands on the command line in Oscar will download the data we need, convert it to BIDS format, and run the BIDS validator to check for any issues. Be sure to change the `bids_root_dir` variable to your desired output location. This will create a source data folder for subject 005 within `$bids_root_dir/bnc/study-demodat/xnat-export` and a BIDS-compatible data directory for subject 005 within `$bids_root_dir/bnc/study-demodat/bids/`.

```shell
version=v1.1.1
#CHANGE THIS TO YOUR DESIRED OUTPUT DIRECTORY
bids_root_dir=/gpfs/data/mworden/${USER}/xnat-exports 
mkdir -m 775 ${bids_root_dir} || echo "Output directory already exists"
simg=/gpfs/data/bnc/simgs/brownbnc/xnat-tools-${version}.sif
XNAT_USER=${USER} 
XNAT_SESSION="XNAT_E00114"
SUBJECT_NUMBER="sub-005"
SESSION_NUMBER="01"
singularity exec --no-home --bind ${bids_root_dir} \
    ${simg} \
    xnat2bids ${XNAT_SESSION} ${bids_root_dir} \
    -u ${XNAT_USER} \
    --session-suffix ${SESSION_NUMBER}	\
    --skipseq 6

singularity exec --contain --bind ${bids_root_dir} ${simg} bids-postprocess -i ${SUBJECT_NUMBER} --session-suffix ${SESSION_NUMBER} ${XNAT_SESSION} ${bids_root_dir}/bnc/study-demodat/bids

val_version=v1.9.9
bids_dir=$bids_root_dir/bnc/study-demodat/bids/
simg=/gpfs/data/bnc/simgs/bids/validator-${val_version}.sif

singularity exec --bind ${bids_dir} ${simg} bids-validator ${bids_dir}
```

#### Step 2: Extract stimulus timing information from stimulus presentation output files.

To make our data BIDS compatible and facilitate future data sharing, we need to create events.tsv files that correspond to each of our functional runs and contain information about each stimulus event of interest (onset time, condition, etc.). First, download the participant's data files (in our case, created by PsychoPy) and place them in the sourcedata subfolder of your BIDS directory in a subfolder named 'beh'. So, for this participant and session, the full path should be: `$bids_root_dir/sourcedata/sub-005/ses-01/beh`.&#x20;

{% file src="../.gitbook/assets/sub-005_ses-1_beh.zip" %}
Demodat subject 005 session 1 behavioral data. For now, we'll only be using the two datafiles for the hemifield localizer task, with "LRChx" in their filenames.
{% endfile %}

Next, download our example python script make\_events.py, and run it from the command line with `python make_events.py --bids_dir {whatever your BIDS directory is} --subj sub-005 --sess ses-01`. For this script to run, you'll need both [numpy](https://numpy.org/install/) and [pandas](https://pandas.pydata.org/) installed in your python environment. This script will create BIDS-formatted events.tsv files corresponding to each functional run in `$bids_root_dir/sub-005/ses-01/func/`.&#x20;

{% file src="../.gitbook/assets/make_events.py" %}
example python script to read in csv files created by PsychoPy and create the events.tsv files corresponding to each fMRI run
{% endfile %}

If you are unable to run this script for any reason, you can download the events.tsv output files here, and manually place them in  `$bids_root_dir/sub-005/ses-01/func/` .

{% file src="../.gitbook/assets/sub-005_ses-01_eventsfiles.zip" %}

#### Step 3: Convert events.tsv files into AFNI stimulus timing files

We needed to make those events.tsv files for BIDS compatibility, but in order to run our statistical analysis in AFNI, we need to transform them into .1D text files required by AFNI for specifying stimulus timing information. Instead of one file per run, as we had with the events.tsv files, here we need one file per condition (e.g. left hemifield checks), with one line per run of the task, specifying all the onset times for that condition. We have created an example python script make\_afni\_stimtimes.py, which you can run from the command line just as you did make\_events.py: `python make_afni_stimtimes.py --bids_dir {whatever your BIDS directory is} --subj sub-005 --sess ses-01` . This will create stimulus timing files in `$bids_root_dir/derivatives/afni/sub-005/ses-01/stimtimes/` .

{% file src="../.gitbook/assets/make_afni_stimtimes.py" %}
example python script to read in events.tsv files from each functional run and output the .1D stimulus timing files AFNI needs
{% endfile %}

If you are unable to run this script for any reason, you can download the .1D files here and manually place them in `$bids_root_dir/derivatives/afni/sub-005/ses-01/stimtimes/`.

{% file src="../.gitbook/assets/sub-005_stimtimes.zip" %}

#### Step 4: Use afni\_proc.py to create a simple preprocessing stream and run the general linear model for the checks task

This basic example of a univariate analysis with AFNI is based on the [example 6b](https://afni.nimh.nih.gov/pub/dist/doc/program\_help/afni\_proc.py.html) for afni\_proc.py. The -blocks flag lists the processing blocks that will be executed, in order:&#x20;

1. tshift (slice time correction)
2. align (aligning the EPIs to the anatomical scan)
3. volreg (motion correction within each functional run)
4. blur (spatial smoothing with a 4mm FWHM smoothing kernel),
5. mask (create a "brain" mask from the functional data, restricted by the anatomy)
6. scale (scale each voxel to have a mean of 100 per run)
7. regress (build a general linear model and execute with [3dREMLfit](https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/programs/3dREMLfit\_sphx.html))

For the regression, we use `-regress_stim_times` to provide the checks\_left\_stimtimes.1D and checks\_right\_stimtimes.1D files for this participant, `-regress_stim_labels` to assign those conditions the labels of "left" and "right" respectively, `-regress_basis` to model each stimulus as a block lasting 12 seconds, and `-regress_opts_3dD` to specify our contrasts. Here, we do a "left\_vs\_right" contrast to find voxels whose activity is greater for left hemifield stimulation than for right, and a "right\_vs\_left" contrast that does the opposite (and should yield the same statistical map, but with opposite-signed t-values).&#x20;

This `demodat_afniproc.sh` script will then create a much longer `proc.sub-005` tcsh script, which will be automatically executed because we included the -execute flag at the bottom of the script. Looking at the proc.sub-005 script is the best way to gain a deeper understanding of each of AFNI's processing steps.&#x20;

{% code title="demodat_afniproc.sh" %}
```bash
#!/bin/bash

bidsdir=/gpfs/home/elorenc1/data/elorenc1/xnat-exports/bnc/study-demodat/bids
subID='sub-005'
sess='ses-01'
task='checks'

afni_proc.py                                                         \
    -subj_id                  $subID                                 \
    -out_dir                  $bidsdir/derivatives/afni/$subID/$sess/$subID.$task.results  \
    -copy_anat                $bidsdir/$subID/$sess/anat/$subID\_$sess\_acq-memprageRMS_T1w.nii.gz        \
    -anat_has_skull           yes                                     \
    -dsets                    $bidsdir/$subID/$sess/func/*$task*nii*                 \
    -blocks                   tshift align volreg blur mask scale regress                          \
    -tcat_remove_first_trs    0                                      \
    -align_opts_aea           -cost lpc+ZZ                           \
                                -giant_move                            \
                                -check_flip                            \
    -volreg_align_to          MIN_OUTLIER                            \
    -volreg_align_e2a                                                \
    -mask_epi_anat            yes                                    \
    -blur_size                4.0                                    \
    -regress_stim_times       $bidsdir/derivatives/afni/$subID/$sess/stimtimes/$subID\_$task\_left_stimtimes.1D $bidsdir/derivatives/afni/$subID/$sess/stimtimes/$subID\_$task\_right_stimtimes.1D          \
    -regress_stim_labels      left right                                \
    -regress_basis            'BLOCK(12,1)'                          \
    -regress_opts_3dD         -jobs 2                                \
                                -gltsym 'SYM: left -right'                \
                                -glt_label 1 left_vs_right                       \
                                -gltsym 'SYM: right -left'                \
                                -glt_label 2 right_vs_left                       \
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

After the `demodat_afniproc.sh` script executes successfully, a results directory will be created: `$bidsdir/derivatives/afni/sub-005/ses-01/sub-005.checks.results`. Start AFNI from within this directory, set the underlay to anat\_final.sub-005 and the overlay to stats.sub-005\_REML. In the Define Overlay menu, set the OLay to "#7 left\_vs\_right#0\_Coef" and the Thr to "#8 left\_vs\_right#0\_Tstat", and change the threshold to your desired alpha (here we've used p = 0.001). This left vs. right contrast shows regions of the brain that show a stronger BOLD response to left vs. right visual hemifield stimulation, so  we can easily localize the right visual cortex and the right LGN, as expected.&#x20;

<figure><img src="../.gitbook/assets/Screen Shot 2022-12-06 at 2.50.06 PM.png" alt=""><figcaption><p>Results of a general linear test contrasting left vs. right visual hemifield stimulation, in demodat subject 005 session 1</p></figcaption></figure>
