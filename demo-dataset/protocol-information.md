---
description: Explanation of BNC's Demo Dataset Protocol
---

# Protocol Information

## Protocol Design at the Scanner

This image shows the protocol as it appears on the scanner under the protocol tree.  The order in which the scans are listed corresponds to the order in which they are run during scanning.  Additional description for each scan can be found below.&#x20;

## ![](<../.gitbook/assets/demodat cropped.jpeg>)

## Details on scans and series&#x20;

{% hint style="warning" %}
This section is still under development
{% endhint %}

### Anatomical Scans

#### Localizer

* **Name at the scanner:** anat-scout\_acq-localizer
* **Description:** The scan session begins with a three-axis localizer that gives views of the participant's head in the three cardinal orientations (sagittal, coronal, axial).&#x20;
* **Scan time:** 1 minute

#### Scout

* **Name at the scanner:** anat-scout\_acq-aascout
* **Description:** This series makes a low resolution whole-head scan and compares the result to a brain atlas on the scanner. It generates new scout images where the orientation is determined with reference to skull landmarks and with reference to the built-in atlas. The resulting images can be used to increase consistency of slice positioning between participants and across scan sessions. &#x20;
* **Scan time:** 1 minute

#### **Multi-Echo MPRAGE**

* **Name at the scanner:** anat-T1w\_acq-memprage
* **Description:** This is a multi-echo T1 weighted (anatomical) structural series. For more information see; [A. J. W. van der Kouwe, T. Benner, D. H. Salat, B. Fischl, Brain morphometry with multi-echo MPRAGE, NeuroImage, 40, 559–569 (2008)](https://pubmed.ncbi.nlm.nih.gov/18242102/). We collect the individual echoes and the RMS images are calculated by combining the individual echos. Compared to a single-echo MPRAGE, the multi-echo MPRAGE provides enhanced tissue contrast and reduced geometric distortion.
* **Scan Time:** 6 minutes

### Field Maps

Field maps are useful for correcting geometric distortions that result from inhomogeneities in the scanner environment. Different field maps can be used to correct different types of scans (i.e functional or diffusion). In this dataset, gradient-echo field maps were collected to correct for geometric distortion in the functional scans and spin-echo field maps were collected for use with the diffusion images. In general, the geometry of the field maps (voxel dimensions and slice placement) should match those images that they will be used to correct.

#### Gradient Echo Field Map

* **Name at the scanner:** fmap\_acq-boldGRE
* **Description:** This is the "standard" Siemens field map, with the same phase encoding direction as the EPI images. This method calculates a field map based on the difference in phase between two different echos in a double echo sequence. This scan produces 2 DICOM series. The first series contains two sets of magnitude images, one for each echo time. The second series is a phase difference image, which is a subtraction of the two individual echos.&#x20;
* **Scanner Note:** On the scanner, it is necessary that the "difference image" checkbox is enabled in the contrast tab to get the difference image**.**&#x20;
* **Scan Time:** 2 minutes

#### Spin Echo Field Map

This method calculates a field map based on the differences between two acquisitions with opposite phase encoding directions. You collect two series, each of which contains a single magnitude volume with opposite phase encoding directions. The actual field map is derived from the differences between these two volumes described below.

#### Anterior-Posterior (AP)

* **Name at the scanner:** fmap-diff\_acq-diffSE\_dir-ap
* **Description:** This map is collected in the anterior-posterior direction.
* **Scan Time:** 2 minutes

#### Posterior-Anterior (PA)

* **Name at the scanner:** fmap-diff\_acq-diffSE\_dir-pa
* **Description:** This map is collected in the posterior-anterior direction.
* **Scan Time:** 2 minutes

### Functional Scans

The dataset includes functional MRI scans for two simple tasks and a resting state condition.  Each of the tasks employed a simple block design. All functional data were collected using multiband (SMS) echoplanar imaging and identical resolution and slice placement.

#### Flashing Checkerboard

* **Name at the scanner:** func-bold\_task-checks\_run+
* **Description:** This is a simple visual activation protocol in which a half-field flashing checkerboard pattern is presented alternately to the left and the right visual hemifields in 12-second blocks while the participant fixates on a small central cross. It is common in many studies to repeat the same functional scan multiple times. For this protocol, this sequence was run twice.  Notice that the sequence name ends with run+.  The bids exporter will automatically convert identically named sequential scans ending with run+ to Run01, Run02, Run03, etc. A link to the PsychoPy files used to run this task can be found below (LRChx.zip).&#x20;
* **Scan Time:** 3 minutes (each)

{% file src="../.gitbook/assets/LRChx.zip" %}
Compressed directory containing PsychoPy experiment for flashing checkerboard task
{% endfile %}

#### Motion Localizer

* **Name at the scanner:** func-bold\_task-motionloc
* **Description:** This task contrasts static and moving dot fields to localize motion sensitive areas of the visual cortex (e.g., area MT+). Three different types of stimuli are presented randomly in blocks **** of 15 seconds each.  The three types of blocks consist of a field of static dots, a field of dots coherently moving in a single direction that changes each second, and a field of "scintillating" dots with no coherent motion.  A 15 second period of fixation only is presented at the start and end of the scan. A link to the PsychoPy files used to run this task can be found below (motionloc.zip).&#x20;
* **Scan Time:** 5 minutes

{% file src="../.gitbook/assets/motionloc.zip" %}
Compressed directory containing PsychoPy experiment for the motion localizer task
{% endfile %}

#### Resting State

* **Name at the scanner:** func-bold\_task-resting
* **Description:** During this scan, there are no tasks involved. The subject is “resting”. The baseline brain activity is observed. Resting state scans are typically used to characterize functional connectivity between brain areas and to characterize the default mode network.
* **Scan Time:** 8 minutes

### Diffusion

Diffusion weighted images are collected in multiple gradient directions. There are many protocols utilizing this type of scan. This example dataset collects a reasonable (basic) 90 direction gradient, and uses one bval level of 1500. Scans are acquired with phase encoding in both the A->P and P->A directions

#### Anterior-Posterior (AP)

* **Name at the scanner:** dwi\_acq-b1500\_dir-ap
* **Description:** A basic diffusion weighted scan with 90 directions and a b-value of 1500.  Phase encoding is in the anterior-to-posterior direction.
* **Scan Time:** 5 minutes

#### Posterior-Anterior (PA)

* **Name at the scanner:** dwi\_acq-b1500\_dir-pa
* **Description:** A basic diffusion weighted scan with 90 directions and a b-value of 1500.  Phase encoding is in the posterior-to-anterior direction.
* **Scan Time:** 5 minutes
