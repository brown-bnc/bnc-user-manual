# Getting Started

We provide custom code and sample data to export your XNAT imaging session to BIDS format. Our process relies on few basic principles:

* Naming of sequences in a BIDS friendly manner at the scanner as outined in the [BIDS Ready Protocols section.](../xnat/bids-compliant-protocols.md)
* DICOMS exported from XNAT using our software is converted to BIDS using [Heudiconv](https://github.com/nipy/heudiconv)
* We rely on the [ReproIn](https://github.com/repronim/reproin) specification and heuristic&#x20;
* Our code is available in the [xnat-tools repository](https://github.com/brown-bnc/xnat-tools)

## Requirements

Before exporting, you'll need to have available, XNAT authentication and session information as well as our software.

### 1. Familiarize with BNC's Demo Dataset

We will use the [BNC's Demo Dataset](getting-started.md#1.-xnat-login-information) in the following walk-through examples. It is helpful to be familiar with the general description and protocol details of the data

### 1. XNAT Login Information

If you have not registered to use our XNAT, please follow these [instructions to create a new XNAT account](../xnat/accessing-xnat.md#first-time-users).&#x20;

Then, log in with your XNAT username and password

### 2. Image Session Identifier

In order to export an imaging session, we need to find XNAT's ID for that session. You can do so as follows:

#### 2.1 Navigate to project of interest

<figure><img src="../.gitbook/assets/Screenshot 2026-03-23 at 2.19.54 PM.png" alt="BNC Demodat 2 is listed under projects on the XNAT portal&#x27;s home page. "><figcaption></figcaption></figure>

#### 2.2 Navigate to subject of interest

<figure><img src="../.gitbook/assets/Screenshot 2026-03-23 at 2.23.33 PM.png" alt="Subjects are listed in the BNC Demodat 2 project page on XNAT. "><figcaption><p>Participants associated with a project</p></figcaption></figure>

#### 2.3 Navigate to MR Session&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2026-03-23 at 2.27.00 PM.png" alt="Sessions are listed in the Subject Details page on XNAT. "><figcaption><p>MR Sessions associated with a participant</p></figcaption></figure>

2.4. Find Accession #

<figure><img src="../.gitbook/assets/Screenshot 2026-03-23 at 2.30.08 PM.png" alt="Accession # is listed under the Details tab for an individual session of data on XNAT. "><figcaption><p>Accession # for a session</p></figcaption></figure>
