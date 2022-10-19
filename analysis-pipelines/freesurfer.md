---
description: >-
  FreeSurfer is a software package for the analysis and visualization of
  structural neuroimaging data.
---

# Freesurfer

It is developed by the [Laboratory for Computational Neuroimaging](https://www.martinos.org/lab/lcn) at the [Martinos Center for Biomedical Imaging](https://www.nmr.mgh.harvard.edu/).

FreeSurfer provides full processing streams for structural and functional MRI and includes tools for linear and nonlinear registration, cortical and subcortical segmentation, cortical surface reconstruction, statistical analysis of group morphometry, diffusion MRI, PET analysis, and _much more_. It is also the structural MRI analysis software of choice for the [Human Connectome Project](http://www.humanconnectomeproject.org/about).

For expansive documentation on using and understanding FreeSurfer tools, please visit the [FS Wiki](https://surfer.nmr.mgh.harvard.edu/fswiki).&#x20;

To run recon-all on a  t1w.nii or t1w.nii.gz dataset

```
module load freesurfer/6.0.0
recon-all -s t1w.nii.gz -all -sd /gpfs/>path to your folder<//recon-all -s t1w.nii.gz -all -sd /gpfs/>path to your folder</
```

This processing takes 6-8 hours to run.

These are the output files you will see:

![](<../.gitbook/assets/Screen Shot 2020-10-22 at 8.23.29 AM.png>)

There is wealth of information produced here. For connectivity analysis the output in the mri folder contains the structural segmentation.

To visualize the output:&#x20;

if not already: log into Oscar:

&#x20;Launch the GUI via VNC session.&#x20;

(if not already loaded)&#x20;

module load freesurfer/6.0.0

```
module load freesurfer/6.0.0
freeview
```

{% embed url="https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/OutputData_freeview" %}



![](<../.gitbook/assets/Screen Shot 2020-10-22 at 8.35.03 AM.png>)

\>File

\>load volume  (navigate to where the mri output is)

load "orig' >grayscale

then load aparc.a2009s+aseg

![](<../.gitbook/assets/Screen Shot 2020-10-22 at 9.16.35 AM.png>)







