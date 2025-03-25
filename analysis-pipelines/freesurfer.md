---
description: >-
  FreeSurfer is a software package for the analysis and visualization of
  structural neuroimaging data.
---

# Freesurfer

It is developed by the [Laboratory for Computational Neuroimaging](https://www.martinos.org/lab/lcn) at the [Martinos Center for Biomedical Imaging](https://www.nmr.mgh.harvard.edu/).

FreeSurfer provides full processing streams for structural and functional MRI and includes tools for linear and nonlinear registration, cortical and subcortical segmentation, cortical surface reconstruction, statistical analysis of group morphometry, diffusion MRI, PET analysis, and _much more_. It is also the structural MRI analysis software of choice for the [Human Connectome Project](http://www.humanconnectomeproject.org/about).

For expansive documentation on using and understanding FreeSurfer tools, please visit the [FS Wiki](https://surfer.nmr.mgh.harvard.edu/fswiki).&#x20;

### Running the recon-all command

Recon-all (recon = reconstruction) is a command that takes an anatomical dataset (T1-weighted image) and performs many common preprocessing steps on it, with the goal of converting the 3D brain image (.nii or .dcm) into a 2D surface. It is helpful to imagine the reconstruction as taking a crumpled balloon (T1w) and blowing it up (inflated surface).  This inflated surface is particularly helpful when analyzing regions of the cortex where some voxels may contain signal from two separate gyri. It is also helpful when analyzing signal found in the sulci.  &#x20;

To run recon-all on Oscar:&#x20;

```
module load freesurfer/7.3.2
recon-all -i t1w.nii.gz -s <subject_name> -sd <path_to_your_folder> -all 
```

{% hint style="info" %}
The `-i` flag points to the T1-weighted anatomical file. If you are running recon-all from the directory containing that file, you can simply put the file name. Otherwise, you must include the full path.&#x20;

`-s` describes the subject name, which will be attached to the output files. This can be anything. &#x20;

`-sd` points to the subjects directory, where all output will be stored. This is a particularly important option to include when using Oscar, since the default subjects directory is within the Freesurfer module and lacks write privileges. With this flag, you can create your own output directory and it will be named what you specified with the `-s` flag.&#x20;

`-all`tells recon-all to perform all preprocessing steps. For the full list of steps, please refer to Freesurfer's documentation found here: [https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all](https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all).&#x20;
{% endhint %}

This processing takes 6-8 hours to run.

### Recon-all Output&#x20;

These are the output directories you will see, located in the specified `-sd` path:

<figure><img src="../.gitbook/assets/Screenshot 2024-04-18 at 11.05.50 AM.png" alt=""><figcaption><p>Output directories of recon-all.</p></figcaption></figure>

{% hint style="info" %}
`label` contains text files which hold spatial information on different regions of the brain, along with those regions' atlas annotations.&#x20;

`mri` contains many different brain volumes with various levels of preprocessing. Importantly, this is where volumes such as the skull-stripped brain, the subcortical segmentations of the brain, and the brain mask are saved.&#x20;

`scripts` contains the log files for the recon-all command. Notably, recon-all.log is where a full history of the workflow can be found.&#x20;

`stats` contains files with information on the thickness and volume for each segmentation and cortical parcellation.

`surf` contains the recon-all generated brain surfaces. This is where both the inflated and non-inflated surfaces are stored.&#x20;

`touch` contains files which are created each time a step of recon-all step is executed. These are used by Freesurfer to determine where to begin if the script is paused and restarted.&#x20;

The temporary directory `(tmp)` and `trash` should both be empty at the end of processing.&#x20;
{% endhint %}

Output from recon-all can be viewed with Freesurfer's image viewer (freeview). To view a surface from the `surf` directory, use the `-f` flag followed by the file name. To view a volume from the `mri` directory, use the `-v` flag. Volume files have the .mgh or .mgz extension, which are unique to Freesurfer and stand for Massachusetts General Hospital, and Massachusetts General Zipped, respectively.&#x20;

```
freeview -f lh.pial rh.pial 
```

<figure><img src="../.gitbook/assets/Screenshot 2024-04-18 at 12.52.18 PM.png" alt=""><figcaption><p>The left and right pial surfaces viewed using freeview. </p></figcaption></figure>

```
freeview -f lh.inflated rh.inflated 
```

<figure><img src="../.gitbook/assets/Screenshot 2024-04-18 at 1.02.28 PM.png" alt=""><figcaption><p>The left and right inflated brain surfaces viewed using freeview. In this image, red represents the sulci and green represents the gyri. </p></figcaption></figure>



### Segmentation and Parcellation

Included in recon-all's workflow is segmentation of the subcortical white and grey matter structures (hippocampus, amygdala, caudate, putamen, thalamus, etc) and parcellation of the cortex. Parcellation is conducted with respect to two different atlases, the Desikan-Killiany atlas (/mri/aparc.DKTatlas+aseg.mgz) and the Destrieux atlas (/mri/aparc.a2009s+aseg.mgz). The main difference between the two is that the Destrieux atlas contains more parcellations and is used in more fine-tuned analyses.&#x20;

```
freeview -v orig.mgz aparc.a2009s+aseg.mgz
```

<figure><img src="../.gitbook/assets/Screenshot 2024-04-18 at 1.20.37 PM.png" alt=""><figcaption><p>T1w image with the Destrieux Atlas segmentation/parcellation overlayed. </p></figcaption></figure>

Volumes/surfaces can also be opened within the freeview window via the file tab.&#x20;

The tutorial below is helpful in becoming more familiar with the output of recon-all:

{% embed url="https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/OutputData_freeview" %}
