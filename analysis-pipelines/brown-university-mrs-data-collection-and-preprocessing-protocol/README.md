---
description: >-
  This documentation is adapted from a tutorial by Meghan A. Gonsalves, PhD on
  2/21/2024. It is continuously updated by the BNC as changes to the software
  are released.
---

# Brown University MRS Data Collection and Preprocessing Protocol

{% hint style="info" %}
A note on terminology:&#x20;

In MR Spectroscopy, there are two types of sequences that are acquired for every voxel at the scanner. Those two scans are both used in preprocessing to construct a single metabolite spectrum. Since the signal from various metabolites are significantly smaller (\~10,000x) than that of water, one run is collected with suppressed water signal. Additionally, a non water suppressed run is collected to provide a signal intensity baseline. This scan is also used for various corrections such as eddy-current distortion correction. There are multiple ways to refer to these two scan types, and many of the terms are interchangeable . Here are lists of the various terms used to refer to the same type of sequences:

_**Water-suppressed data:**_**&#x20;"standard", "metabolite", "wsat on" (water saturation on), "glx", "svs" (single voxel spectroscopy)**

_**Water un-suppressed data:**_**&#x20;"reference", "lineshape", "wsat off" (water saturation off), "wat", "mrsref" (mrs reference)**&#x20;

When organizing your MRS data according to BIDS, the suffix of the file name will indicate the sequence type. It will either be named "filename\_svs.nii" or "filename\_mrsref.nii".&#x20;

For the sake of clarity in this tutorial, we will refer to the data as "water reference" and "metabolite".&#x20;
{% endhint %}

