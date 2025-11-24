# Group Analysis: Visual/Motor Activation

This tutorial covers group analysis via batch scripting and various AFNI functions: sswarper2 (for converting data to standard space), afniproc.py (for individual subject preprocessing), and gen\_group\_command.py (for group-level statistics with 3dttest++ or 3dMEMA).&#x20;

## Workflow Overview

<figure><img src="../../../.gitbook/assets/Screenshot 2025-11-24 at 10.01.25 AM.png" alt=""><figcaption></figcaption></figure>

The basic flow of this pipeline is as follows:&#x20;

**First-Level Analysis:**&#x20;

1. Download data from XNAT and automatically convert it to BIDS format using xnat2bids
2. Convert psychopy timing files to be used by AFNI
3. Prepare fMRI data for preprocessing by warping to standard space (using sswarper2)
4. Use afni\_proc.py to create a preprocessing stream and run the general linear model per subject

**Second-Level Analysis:**&#x20;

1. Use gen\_group\_command.py to build and run your statistical tests
2. Compute a group intersection mask
3. Calculate the average smoothness across participants
4. Use 3dClustSim to simulate noise and determines what cluster sizes are needed to control false positives
5. Use 3dClusterize to apply the thresholds to your group-level statistical maps from 3dMEMA. It outputs final significant clusters and effect estimate maps
