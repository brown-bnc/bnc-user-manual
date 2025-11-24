---
hidden: true
---

# MRtrix3 for Diffusion Imaging Analysis

## Introduction

MRtrix3 is a software package written in C++ that provides a large variety of DWI processing tools. It is a wrapper from many common FSL commands for DWI. It's uses can be grouped into 4 major categories:&#x20;

* DWI Preprocessing (denoising and distortion correction using [topup and eddy](https://docs.ccv.brown.edu/bnc-user-manual/analysis-pipelines/fsl-topup-and-eddy))
* Constrained Spherical Deconvolution&#x20;
* Fixel-Based Analysis (quantification of white matter fiber density per voxel)
* Quantitative Structural Connectivity (Probabilistic Tractography, Connectome Construction using [Freesurfer](https://docs.ccv.brown.edu/bnc-user-manual/analysis-pipelines/freesurfer))

### What is Constrained Spherical Deconvolution (CSD)?

* CSD is a method of tensor fitting that enables more accurate modeling of crossing fibers. It deconvolves the signal in every voxel to produce a fiber orientation density function (FOD).&#x20;

### What is unique about MRtrix Image Formats (.mih and .mif)?

In diffusion imaging, a gradient table details the b-values and corresponding b-vectors (directions) for a run. This information is typically saved as two separate files (.bvec and .bval) and is combined into a gradient table, or b-table, during preprocessing. MRtrix files store the gradient table within the file header, which will always be embedded within the data file (.mif). This automatic process is particularly helpful because it reduces the chance of user error when creating and editing b-tables. The b-table and it's corresponding data will not be separated at any point of the processing pipeline.&#x20;

The gradient table can also be stored within a separate header file (.mih). This file does not contain the binary data, but is another way to store metadata. More information about these two formats can be found in the [MRtrix3 documentation](https://mrtrix.readthedocs.io/en/latest/getting_started/image_data.html#mrtrix-image-formats).

## Installing MRtrix3&#x20;

MRtrix3 version 3.0.6 is now available as a module on Oscar. To access it, open a terminal in a virtual desktop and type:&#x20;

```
module load mrtrix3
```

If you would like to install MRtrix3 to your local computer, you can follow [these instructions. ](https://www.mrtrix.org/download/)

