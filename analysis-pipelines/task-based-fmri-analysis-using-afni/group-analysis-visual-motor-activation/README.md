---
description: >-
  This tutorial covers group analysis via batch scripting, sswarper2 (for
  converting data to standard space), afniproc.py (for preprocessing), and
  afni's 3dMEMA (for group statistical analysis).
---

# Group Analysis: Visual/Motor Activation

## Workflow Overview

<figure><img src="../../../.gitbook/assets/Screenshot 2025-09-15 at 2.38.38 PM.png" alt=""><figcaption></figcaption></figure>

The basic flow of this pipeline is as follows:&#x20;

**Single-Subject Preprocessing/Analysis:**&#x20;

1. Download data from XNAT and automatically convert it to BIDS format using xnat2bids
2. Convert psychopy timing files to be used by AFNI
3. Prepare fMRI data for preprocessing by warping to standard space (using sswarper2)
4. Use afni\_proc.py to create a preprocessing stream and run the general linear model per subject

**Group Analysis:**&#x20;

1. Use gen\_group\_command.py to build your statistical tests and run the second-level analysis
