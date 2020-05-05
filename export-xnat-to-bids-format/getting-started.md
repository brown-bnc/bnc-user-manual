# Getting Started

We provide custom code to export your XNAT imaging session to BIDS format. Our process relies on few basic principles:

* Naming of sequences in a BIDS friendly manner at the scanner
* DICOMS exported from XNAT using our software is converted to BIDS using [Heudiconv](https://github.com/nipy/heudiconv)
* We rely on the [ReproIn](https://github.com/repronim/reproin) specification and heuristic 
* Our code is available in the [xnat-tools repository](https://github.com/brown-bnc/xnat-tools)

## Requirements

Before exorting, you'll need to have available, XNAT authentication and session information as well as our software.

### 1. XNAT Login Information

* XNAT Host
* XNAT Username
* XNAT Password

### 2. Image Session Identifier

In order to export an imaging session, we need to find XNAT's ID for that session. You can do so as follows:

#### 2.1 Navigate to project of interest

![](../.gitbook/assets/image%20%284%29.png)

#### 2.2 Navigate to subject of interest

![](../.gitbook/assets/image.png)

#### 2.3 Navigate to MR Session 

![](../.gitbook/assets/image%20%282%29.png)

#### 2.4. Find Accession \#

![](../.gitbook/assets/image%20%281%29.png)

### XNAT2BIDS Software

The BNC maintains a python package [xnat-tools](https://github.com/brown-bnc/xnat-tools) to make it simple to export and convert your data to BIDS. The optimal way to install and run the code depends on your computation environment. The next session outlines all possibilities

