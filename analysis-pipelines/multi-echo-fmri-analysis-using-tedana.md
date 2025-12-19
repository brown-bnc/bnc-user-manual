# Multi-Echo fMRI Analysis Using tedana

This tutorial is a walkthrough of task-based multi-echo fMRI preprocessing using fmriprep, tedana, and afni. There are multiple pipelines available that can be customized to your specific project and which utilize different combination methods. Even if you do not choose to use tedana, their documentation is very thoroughly and provides a strong basis to build your own workflow. Their background on multi-echo methods and general guidelines for preprocessing can be found [at this link.](https://tedana.readthedocs.io/en/stable/multi-echo.html) A more comprehensive list of resources will be listed at the end of this tutorial.&#x20;

## Background

### What is Multi-Echo fMRI?&#x20;

Researchers interested in multi-echo (ME) fMRI are likely already familiar with standard, single-echo (SE) fMRI sequences. In SE fMRI, one volume is collected at each repetition time (TR). This is done with an excitation pulse, followed by one readout of the data at the echo time (TE). Choosing an echo time depends on what tissue type and brain region you are interested in- typically it is chosen to maximize bold contrast across the brain (the average T2\* of brain). Since you are measuring one readout for every TR, the resulting dataset is a complete time series for every voxel as depicted below.&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2025-12-11 at 3.29.30 PM.png" alt=""><figcaption><p>A typical time series for one voxel, as seen in the afni viewer. This time series is taken from the occipital lobe of a brain scanned using a standard single echo EPI fMRI sequence. The vertical y axis is the raw signal of the voxel and the horizontal x axis is time. </p></figcaption></figure>

ME fMRI is similar to SE fMRI in that there is only one initial excitation pulse. However, immediately following that pulse, multiple readouts are acquired at various chosen echo times. The subsequent "echos" come at the cost of an increased TR, but with the integration of acceleration methods like GRAPPA and multiband, little TR sacrifice (if any) is necessary. The number of echos typically ranges from 3-5, but it is possible to acquire more. The upper limit to the number of echos is when the signal fully decays, requiring another excitation pulse.&#x20;

Typically, the first echo is acquired immediately following the excitation pulse, followed by a second echo at what would be the typical TE (\~40-60ms), and then all remaining echos.&#x20;

The result of ME fMRI is multiple complete time series per voxel (one for each echo). These separate time series can be combined using various methods.

<figure><img src="../.gitbook/assets/Screenshot 2025-12-11 at 4.04.18 PM.png" alt=""><figcaption><p>Time series of one voxel, across the three echos acquired (single-subject ME fMRI data collected at Brown University's MRF). </p></figcaption></figure>

#### Why collect multiple echos?

<figure><img src="../.gitbook/assets/Screenshot 2025-12-02 at 10.46.45 AM.png" alt=""><figcaption><p>Single-subject ME fMRI data collected at Brown University's MRF. This scan collected three echos, viewed from left to right: TE=12.2, 30.66, and 49.10. This data is presented prior to any preprocessing. </p></figcaption></figure>

As TE increases, signal decays. Typically, in SE fMRI, researchers select a TE that maximizes the BOLD contrast across the brain. This is not perfect, due to variations in susceptibility across different tissue types, blood, CSF, and the sinuses. Choosing a TE that maximizes BOLD contrast across the brain often results in signal dropout in regions near air/sinuses. For example, you can see below that the signal in the temporal lobe decays at a faster rate than other brain regions. This is due to its close proximity to air in the ear canals.&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2025-12-02 at 1.03.59 PM.png" alt=""><figcaption><p>This view of the brain across multiple echos clearly depicts signal dropout at the tissue border between the temporal lobe and the air in the ear canals. One benefit of combining echos is the recovery of signal in these regions. </p></figcaption></figure>

Each echo comes with a unique cost/benefit:

1. EARLY: An echo captured as soon as possible will have low contrast but high SNR
2. OPTIMAL: the optimal TE (30-60ms) is a "happy medium", with some noise but with the additional bold sensitivity/contrast
3. LATE: high contrast and low SNR

The aim of ME processing is to take advantage of the benefit of each echo by combining them into one image/time series.&#x20;

## Multi-Echo fMRI Preprocessing

{% hint style="info" %}
tedana is not a complete workflow- it requires preprocessing before being used, and it does not run a GLM/regression after it is used. Here, the preprocessing is done using fmriprep. Whatever you choose to use, it is important that it does not combine the echos. When using fmriprep, the “--me-output-echos” flag will provide individual echos that have been minimally preprocessed and are ready to be handed to tedana. These echos have the following steps applied: slice time corrected, head motion corrected, and susceptibility distortion corrected. <br>

tedana then takes individual echoes and combines them in various ways. It will produce an ‘optimally combined’ dataset, and a dataset that has undergone multi-echo independent component analysis (MEICA). This is referred to as the "denoised" dataset. When feeding the data into a regression, you do not use both the optimally combined and the denoised data, you choose one (unless you are comparing them). In this tutorial, regressions are completed on the denoised data using afni. <br>
{% endhint %}

### General Overview

1. Pre-tedana Steps (fmriprep):
   1. Motion Correction
   2. Slice timing correction&#x20;
2. Echo Combination/ME Denoising (tedana)
3. Final Preprocessing/Regression (afni)
   1. Distortion correction
   2. Spatial normalization
   3. Smoothing
   4. Rescaling or filtering
   5. Regression Analysis

### Step by Step Guide

#### **Install tedana and organize data**

1. Install tedana
   1. For ease of use, you can [download tedana](https://tedana.readthedocs.io/en/stable/installation.html) to your local bin directory on Oscar
2. Download your MRI data and save it in a BIDS formatted directory
   1. This can be completed via xnat2bids on oscar ([Instructions here](https://docs.ccv.brown.edu/bnc-user-manual/xnat-to-bids-intro/using-oscar/oscar-utility-script))
3. Prepare behavioral task timing files (If doing task based ME-EPI)
   1. Download your behavioral timing files (e.g. from psychopy) and place them in `$bidsroot/sourcedata/sub-xxx/ses-xx/beh`
      1. Convert them to BIDS-friendly tsv files located in `$bidsroot/sub-xxx/ses-xx/func` &#x20;
      2. If you are doing your regression with afni, they need to be converted to 1D files
         1. These 1D files should be stored in `$bidsroot/derivatives/afni/sub-xxx/ses-xx/stimtimes`
   2. Example file conversion scripts for both single subject and group analysis can be found in our [documentation on task-based fMRI analysis](https://docs.ccv.brown.edu/bnc-user-manual/analysis-pipelines/task-based-fmri-analysis-using-afni).  &#x20;

#### Preprocess the individual echos using fmriprep

1. &#x20;Launch the script below by following [the instructions found here](https://docs.ccv.brown.edu/bnc-user-manual/bids/fmriprep).
   1. It is important that the “`--me-output-echos`” flag is included
   2. Data can be in any space you want
   3. **Input:** the BIDS-formatted data per subject
   4. **Output:** Preprocessed dataset, including individual echos. Output is located in `$bidsroot/derivatives/fmriprep`

```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -c 8
#SBATCH --mem=40G
#SBATCH --time 24:00:00
#SBATCH -J fmriprep_job
#SBATCH --output fmriprep-log-%J.txt
#SBATCH --mail-user example_user@brown.edu
#SBATCH --mail-type ALL

#---------CONFIGURE THESE VARIABLES--------------
export_dir=/path/to/dir/ # <- This should be one directory above/parent to BIDS
participant_label=subID # <- Change this to your subject ID (excluding the "sub-" prefix)
fmriprep_version=24.1.0
user=yourID # <- Change this to your oscar username

#---------END OF VARIABLES------------------------

singularity run --cleanenv                                         \
  --bind ${export_dir}:/data                                       \
  --bind /oscar/scratch/$user:/scratch                             \
  --bind /oscar/data/bnc/licenses:/licenses                        \
  /oscar/data/bnc/simgs/nipreps/fmriprep-${fmriprep_version}.sif   \
  /data/bids /data/bids/derivatives/fmriprep-${fmriprep_version}   \
  participant --participant-label ${participant_label}             \
  --output-spaces T1w MNI152NLin2009cAsym                          \
  --fs-license-file /licenses/freesurfer-license.txt               \
  -w /scratch/fmriprep                                             \
  --me-output-echos                                                \
  --omp-nthreads 16 --nthreads 16 --stop-on-first-crash

```

#### Combine echos using tedana

{% hint style="info" %}
Tip: When you input data from fmriprep into other programs that mask it, the masking is not always accurate. This issue can be avoided by providing a mask in the tedana command.&#x20;
{% endhint %}

A note on multi-run data: tedana does not accept multiple runs of data in one command. Individual tedana commands are used for every run, and the preprocessed runs can then be combined in the regression

Run tedana with basic defaults using this script:

```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH --time 1:00:00
#SBATCH -J tedana_run01_masked
#SBATCH --output tedana-run01_masked-log-%J.txt
#SBATCH --mail-user example_user@brown.edu          # <- change to your email
#SBATCH --mail-type ALL

tedana -d /path/to/fmriprepped/data \
-e 12.2 30.66 49.1 \                                # <- change to your TEs 
--mask /path/to/fmriprep/mask \
--out-dir /path/to/output/directory \
--verbose \
```

<details>

<summary>More Information about this command</summary>

* The `-d` flag is followed by the multi-echo dataset. Only one run can be input per command, but you can include all the separate echos by using a wildcard. For example, the file we used in our testing was: `sub-xxx_ses-xx_task-xxx_acq-me_run-01_echo-*_desc-preproc_bold.nii.gz`. The files ending in `desc-preproc_bold.nii.gz` are the individual echos from fmriprep that have been slice time and motion corrected.&#x20;
* The `-e` flag is followed by the three echo times we chose for our ME sequence. You must change this to correspond to your scan. If you are unsure what the TEs are, you can look in the JSON sidecar associated with the ME NIFTIs. It is important to write these TEs in the correct ascending order- they will be used with the data files respectively.&#x20;
* While it is not necessary to provide a mask, we chose to in this instance because we observed improper masking in subsequent steps. Specifically, when we input data from fmriprep into other programs that then mask it (tedana, afni), the masking was not accurate. This issue is avoided by providing a mask in the tedana command.&#x20;
* The `--out-dir` output directory will not be created by tedana- ensure it exists before launching this script. I recommend creating a tedana folder within the bids/derivatives directory.&#x20;
* If you would like to use a decision tree other than the default (tedana\_orig), you can specify one using the `--tree` flag.&#x20;

For further detail on all possible tedana flags, please refer to [tedana's documentation](https://tedana.readthedocs.io/en/stable/usage.html).&#x20;

</details>

Information on the outputs of tedana can be found on the [tedana website](https://tedana.readthedocs.io/en/stable/outputs.html). tedana does not have its own GUI- to visually inspect the data, you can open the viewer of your choice (afni, fsleyes, etc).&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2025-12-18 at 3.48.11 PM.png" alt=""><figcaption><p>Left: The middle echo after preprocessing via fmriprep. Right: The same transverse slice of the brain, after multi-echo denoising/ tedana. Notably, there is recovery from dropout in the temporal and frontal lobes. </p></figcaption></figure>

#### Run a regression for task data using afni

{% hint style="info" %}
Tip: The individual echos from fmriprep will always be output in their own native space, regardless of if you specify a different output space. If you want to standardize your data (for example, to compute voxel-wise comparisons across different datasets), I recommend using antsApplyTransforms before running afniproc.&#x20;
{% endhint %}

1. Use antsApplyTransforms to warp all runs into the same space.&#x20;
   1. This section of code is based on [this example provided by the tedana team](https://tedana.readthedocs.io/en/stable/faq.html#warping-scanner-space-fmriprep-outputs-to-standard-space)
   2. In the fmriprep output, there are corresponding transformation files for each space you specify in your fmriprep command. In this guide, we are not warping the data into standard space (MNI, tlrc), but instead warping all ME functional runs to the anatomical dataset. If you are doing group-level analysis in standard space, then change the antsApplyTransforms flags  `-r` and `-t` to your desired space. The instructions on the tedana site (provided above) do this- please refer to that for more information about warping to standard space.&#x20;
2. Run afniproc
   1. **Input:**&#x20;
      1. Fmriprepped T1 anatomical scan
      2. Fmriprepped individual echos (after transforming to the same space)
      3. Stimulus timing files (already converted to afni 1D files)
   2. **Output:** statistical files (from 3dDeconvolve and/or 3dREML)&#x20;

```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH --time 3:00:00
#SBATCH -J afniproc_medenoised
#SBATCH --output afniproc_medenoised-log-%J.txt
#SBATCH --mail-user example_user@brown.edu                 # <- change to your email
#SBATCH --mail-type ALL

bids_dir=/path/to/bids

module load afni
module load ants

# Warp to T1w space using antsApplyTransforms
## Change paths/filenames before running this script
antsApplyTransforms \
        -e 3 \
        -i ${bids_dir}/derivatives/tedana/desc-denoised_bold.nii.gz \
        -r ${bids_dir}/derivatives/fmriprep-24.1.0/sub-xxx/ses-xx/func/sub-xxx_ses-xx_task-xxx_acq-me_run-01_space-T1w_boldref.nii.gz \
        -o ${bids_dir}/derivatives/tedana/desc-denoised_bold-T1wspace.nii.gz \
        -n LanczosWindowedSinc \
        -t ${bids_dir}/derivatives/fmriprep-24.1.0/sub-xxx/ses-xx/func/sub-xxx_ses-xx_task-xx_acq-me_run-01_from-boldref_to-T1w_mode-image_desc-coreg_xfm.txt

# Run afniproc 
### This is an example, and must be edited to fit your task
afni_proc.py                                                         \
    -subj_id                  me_denoised                                 \
    -copy_anat                ${bids_dir}/derivatives/fmriprep-24.1.0/sub-xxx/ses-xx/anat/sub-xxx_ses-xx_acq-mprage_desc-preproc_T1w.nii.gz     \
    -anat_has_skull           yes                                     \
    -dsets                    ${bids_dir}/derivatives/tedana/desc-denoised_bold-T1wspace.nii.gz \
    -blocks                   blur mask scale regress \
    -blur_size                4.0                                    \
    -regress_stim_times       ${bids_dir}/derivatives/afni/sub-xxx/ses-xx/stimtimes/sub-xxx_acq-me_task-xxx_run-01_left_stimtimes.1D     \
                              ${bids_dir}/derivatives/afni/sub-xxx/ses-xx/stimtimes/sub-xxx_acq-me_task-xxx_run-01_right_stimtimes.1D   \
    -regress_stim_labels      left right                                \
    -regress_basis            'BLOCK(12,1)'                          \
    -regress_opts_3dD         -jobs 2                                \
                                -gltsym 'SYM: left -right'                \
                                -glt_label 1 left_vs_right                       \
    -mask_apply                epi \
    -regress_motion_per_run                                          \
    -regress_censor_outliers  0.05                                   \
    -regress_reml_exec                                               \
    -regress_compute_fitts                                           \
    -regress_make_ideal_sum   sum_ideal.1D                           \
    -regress_est_blur_epits                                          \
    -regress_est_blur_errts                                          \
    -regress_run_clustsim     yes                                    \
    -html_review_style        pythonic                               \
    -execute

```

<details>

<summary>More information on the antsApplyTransforms command</summary>

`antsApplyTransforms` allows researchers to transform one image/dataset into the same coordinate space as a another (reference) dataset

* `-e`: the number of echos in the ME dataset&#x20;
* `-i`: input image; in our case, the denoised dataset from tedana&#x20;
* `-r`: the reference image, which defines the space that the input image will be transformed into. This is automatically output from fmriprep
* `-o`: the filename of the output/warped dataset
* `-n`: interpolation method
* `-t`: the transform file, also output from fmriprep

</details>

### Helpful Resources

{% embed url="https://me-ica.github.io/multi-echo-data-analysis/content/Course_Overview.html" %}

{% embed url="https://tedana.readthedocs.io/en/stable/multi-echo.html" %}

[Video: CMN Core Presentation Series: Advantages of multi-echo fMRI, 2019](https://www.youtube.com/watch?v=G1Ftd2IwF14)

Posse S. Multi-echo acquisition. Neuroimage. 2012

Poser et al., BOLD contrast sensitivity enhancement and artifact reduction with multiecho EPI: parallel-acquired inhomogeneity-desensitized fMRI. Magn Reson Med. 2006&#x20;

Kundu et al., Differentiating BOLD and non-BOLD signals in fMRI time series using multi-echo EPI. Neuroimage, 2012

Posse S. Multi-echo acquisition. Neuroimage. 2012

Kundu et al., Multi-echo fMRI: A review of applications in fMRI denoising and analysis of BOLD signals. Neuroimage. 2017&#x20;

Lynch et al., Rapid Precision Functional Mapping of Individuals Using Multi-Echo fMRI. Cell Rep. 2020
