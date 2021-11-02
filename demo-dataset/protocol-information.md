---
description: Explanation of BNC's Demo Dataset Protocol
---

# Protocol Information

## Protocol Design at the Scanner

{% hint style="warning" %}
Coming soon
{% endhint %}

## Details on scans and series&#x20;

{% hint style="warning" %}
This section is still under development
{% endhint %}

### Anatomical Scans

#### Localizer

* **Name at the scanner:** anat-scout\_acq-localizer
* **Description: **The scan session begins with a three-axis localizer that gives views of the participant's head in the three cardinal orientations (sagittal, coronal, axial).&#x20;
* **Scan time:** 1 minute

#### Scout

* **Name at the scanner: **anat-scout\_acq-aascout
* **Description: **This series makes a low resolution whole-head scan and compares the result to a brain atlas on the scanner. It generates new scout images where the orientation is determined with reference to skull landmarks and with reference to the built-in atlas. The resulting images can be used to increase consistancy of slice positionning between participants and across scan sessions. &#x20;
* **Scan time: **1 minute

#### **Multi-Echo MPRAGE**

* **Name at the scanner: **anat-T1w\_acq-memprage
* **Description: **This is a multi-echo T1 weighted (anatomical) structural series. For more information see; [A. J. W. van der Kouwe, T. Benner, D. H. Salat, B. Fischl, Brain morphometry with multi-echo MPRAGE, NeuroImage, 40, 559–569 (2008)](https://pubmed.ncbi.nlm.nih.gov/18242102/). We collect the echoes and the RMS images. Compared to a single-echo MPRAGE, the multi-echo MPRAGE provides enhanced tissue contrast and reduced geometric distortion.
* **Scan Time:** 6 minutes

### Field Maps

Field maps are useful for correcting geometric distortions that result from inhomogeneities in the scanner environment. Different field maps can be used to correct different types of scans (i.e functional or diffusion). In these data gradient-echo field maps were collected to correct for geometric distortion in the functional scans and spin-echo field maps were collected for use with the diffusion images.  In general, the geometry of the field maps (voxel dimensions and slice placement) should match those images that they will be used to correct.

#### Gradient Echo Field Map

* **Name at the scanner: **fmap-acq-boldGRE
* **Description: **This is the "standard" Siemens field map, with the same phase encoding direction as the EPI images. This method calculates a field map based on the difference in phase between two different echos in a double echo sequence. This scan produces 2 DICOM series. The first series contains two sets of magnitude images, one for each echo time.  The second series is a phase difference image, which is a subtraction of the two individual echos.&#x20;
* **Scanner Note: **On the scanner, it is necessary that the "difference image" checkbox is enabled in the contrast tab to get the difference image**. **
* **Scan Time: **2 minutes

#### Spin Echo Field Map (optional)

* **Name at the scanner: **fmap-acq-boldSE
* **Description: **These field maps are based on geometrical distortions in SE magnitude images. This method calculates a field map based on the differences between two  acquisitions with opposite phase encoding directions. You get 2 series: Each which contains a single magnitude volume with opposite phase encoding direction.
* **Scan Time: **1 minute

#### Anterior-Posterior (AP)

* **Name at the scanner: **fmap-diff\_acq-diffSE\_dir-ap
* **Description: **This map is collected in the anterior-posterior direction
* **Scan Time: **2 minutes

#### Posterior-Anterior (PA)

* **Name at the scanner: **fmap-diff\_acq-diffSE\_dir-pa
* **Description: **This map is collected in the posterior-anterior direction
* **Scan Time: **2 minutes

### Functional&#x20;

For the functional runs, we collected Echo Planar Image (EPI) for 4 Motion Localizer, a Flashing Checkerboard Task, A Stop Signal Reaction Time and a Resting State task

#### Motion Localizer

* **Name at the scanner: **func-bold\_task-motionloc\_run+
* **Description: **
* **Scan Time: **5 minutes

#### Flashing Checkerboard

* **Name at the scanner: **func-bold\_task-checks\_run+
* **Description: **
* **Scan Time: 3** minutes

#### Stop Signal Reaction Time (SSRT)

* **Name at the scanner: **func-bold\_task-ssrt
* **Description: **
* **Scan Time: **6 minutes

#### Resting State

* **Name at the scanner: **func-bold\_task-restring
* **Description: **During this scan, there are no tasks involved. The subject is “resting”. The baseline brain activity is observed
* **Scan Time: **8 minutes

### Diffusion

Diffusion weighted images are collected in multiple gradient directions. There are many protocols utilizing this type of scan. This example dataset collects a reasonable (basic) 90 direction gradient, and uses one bval level of 1500.

#### Anterior-Posterior (AP)

* **Name at the scanner: **dwi\_acq-b1500\_dir-ap
* **Description: **McLaughlin protocol
* **Scan Time: **6 minutes

#### Posterior-Anterior (PA)

* **Name at the scanner: **dwi\_acq-b1500\_dir-pa
* **Description: **McLaughlin protocol
* **Scan Time: **2 minutes
