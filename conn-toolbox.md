---
description: >-
  CONN is a matlab based cross platform software for the computation, display
  and analysis of functional connectivity in fMRI.It is available for  restng
  state data as well as task-related designs.
---

# CONN Toolbox

Install the software on your local machine or use Oscar matlab and conn toolbox modules.

![](.gitbook/assets/screen-shot-2020-09-14-at-4.28.01-pm.png)

 QUICK Start: Step 1 : Click on the SETUP tab

               Click on Project.New \(the wizard will allow a gui setup tp import functional, anatomical data and optionally preprocess your data using standard settings \(segmentation, realignment, slice timing correction, co-registration, normalization, smoothing, and outlier detection.scrubbing\) using either defaultMNI for analyses in MNI space or default SS for analyses in subject-space or surface based analysis.If you have already done SPM preprocessing you can skip the preprocessing steps and import the SPM.mat file for each subject.

Structural files Setup;

load structural Images

![](.gitbook/assets/screen-shot-2020-09-14-at-5.45.21-pm.png)

Functional Files setup

load functional files

![](.gitbook/assets/screen-shot-2020-09-14-at-5.48.28-pm.png)

If the functional images are not preprocessed; you select "functional tools: individual preprocessing step or Preprocessing"

![](.gitbook/assets/screen-shot-2020-09-14-at-5.53.24-pm.png)

ROI files setup

Click on ROI's button on the left side to load ROI masks files  \(.img or .nii volumes\), MNI coordinates \(.tal files\), or atlas files \(.nii files with multiple labels\)

![](.gitbook/assets/screen-shot-2020-09-14-at-5.57.26-pm.png)

Rest or Task conditions setup

Click on conditions button to enter onsets and durations \(in seconds\) of each experimental condition \(blocks/events\). enter 0 and inf in the onset and duration fields respectively to indicate that the selected condition\(s\) encompass the entire scan time. Leave empty in the onset and duration fields to indicate that the selected condition\(s\) was not present during the selected session.

![](.gitbook/assets/screen-shot-2020-09-14-at-6.07.36-pm.png)

First-level \(within subjects\) covariates setup

Click on covariates: first level button to define covariates such as realignment parameters to be used in the first level BOLD model. For each covariate select a .txt of .mat file containing the covariate time series \(ie select the realignment parameters file rp\_\*.txt to include movement parameters as covariates.\)

![](.gitbook/assets/screen-shot-2020-09-14-at-6.07.36-pm%20%281%29.png)

