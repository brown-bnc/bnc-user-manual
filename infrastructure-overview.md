---
description: Overview of BNC's Infrastructure
---

# Infrastructure Overview

DICOM data are sent from the scanner to a local machine with an XNAT instance, referenced below as the XNAT-RELAY.  The relay's purpose is twofold: 1) providing data encryption before sensitive files are passed over the network,  and 2) utilizes XNAT's Xsync plugin to enable automatic synchronization of data to the appropriate existing project.  After the data have been successfully uploaded and synced, researchers can view their experiment data through the XNAT portal or export session data programmatically via BNC's suite of processing tools.  The following diagram illustrates our complete infrastructure setup:

![Overview of BNC's Infrastructure as it relates to SCANNER and XNAT](<.gitbook/assets/Public DICOM Listener with Relay - Page 1-2.png>)
