---
description: Overview of BNC's Infrastructure
---

# Infrastructure Overview

DICOM data are sent from the scanner to XNAT via an SSH tunnel for data encryption. After the data have been successfully uploaded, researchers can view their experiment data through the XNAT portal or export session data programmatically via BNC's suite of processing tools.  The following diagram illustrates our complete infrastructure setup:

<figure><img src=".gitbook/assets/xnat_data_flow.png" alt="Diagram illustrating the BNC’s data management infrastructure. Private MRI data is collected at the MRF, then encrypted and sent to XNAT. Researchers can access their data by downloading it from XNAT on the internet, or by using the BNC’s software to convert data to BIDS format and store it on their local computer, or onto an account on Brown’s supercomputer, Oscar. "><figcaption><p>Overview of BNC's Infrastructure as it relates to SCANNER and XNAT</p></figcaption></figure>
