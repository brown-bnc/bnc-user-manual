---
description: Details of the different options available to download your data from XNAT
---

# Downloading Data

## Summary of tools and methods to download your data

| Method/Tool                            | Recommended Usage                                                                                                               | Requirements                                                                                                                                                                 |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Download via UI                        | Downloading DICOM data that is not super large and when pausing, resuming is not needed.                                        | Browser (campus network)                                                                                                                                                     |
| Download via XNAT Desktop Client       | Download DICOM data with grater granularity and for large number of participants. Pausing, resumming and reporting is available | App installed. Doesn't work in OSCAR                                                                                                                                         |
| Download via xnat-tools python package | Programmatic download. Great for batch uploads and for combining with **BIDS conversion**                                       | Instalation of xnat-tools python package. This can be done from local computer or Oscar as explained in the [XNAT2BIDS section](../xnat-to-bids-intro/xnat2bids-software.md) |

## 1. Download via Web UI&#x20;

This is the **simplest but slowest** way to download data. If you'll only be downloading multiple imaging sessions, you may want to refer to other options below

### 1.1 Navigate to your MR Data Session

![MR session list for a given participant](<../.gitbook/assets/image (22).png>)

### 1.2 Download ONE sequence

If you only need to download one sequence, you can use the download button on the corresponding row

![Highlighting download button for a single sequence](<../.gitbook/assets/image (19).png>)

### 1.3 Download ALL sequences

You have multiple options here

#### 1.3.1 Select ALL and use the download bulk action

Depending on the size of your data, this may take a while

![Highlighting SELECT ALL and BULK DOWNLOD BUTTONS](<../.gitbook/assets/image (23).png>)

### 1.4 Download with granularity

If you wish to have greater granularity on the types of resources downloaded you can use the menu under **Actions -> Download -> Images.** We will dive a little more into the options on the next section, as this is gives a a great segway into talking about



![Highlighting the Actions -> Download menu to access detailed downloading options](<../.gitbook/assets/image (21).png>)

## 2. Downloading via XNAT Desktop Client

The [XNAT Desktop Client](https://wiki.xnat.org/xnat-tools/xnat-desktop-client-dxm) is a convenient way to upload and download data to XNAT. Unfortunately, at this time, the application doesn't work in Oscar, but if you are downloading data to your personal computer, you may want to give it a try.

The [documentation](https://wiki.xnat.org/xnat-tools/xnat-desktop-client-dxm) for the Desktop Client is quite detailed, so we won't repeat the steps here.

## 3. Download data programmatically

We maintain a python package [xnat-tools](https://github.com/brown-bnc/xnat-tools) that facilitates downlaoding your data and converting it to  BIDS. The optimal way to install and run the code depends on your computation environment. The package [documentation](https://brown-bnc.github.io/xnat-tools/) explains different installation and execution methods for a general user.&#x20;

If you do not need BIDS, you'll only need the [xnat-dicom-export](https://brown-bnc.github.io/xnat-tools/1.0.6/dicom\_export/) utility. If you will be downloading and converting to BIDS, then please follow the instactions on the [XNAT TO BIDS](broken-reference) section.

