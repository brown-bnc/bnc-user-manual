---
description: >-
  Using the QSMxT toolbox to create whole-brain quantitative magnetic
  susceptibility maps
---

# Quantitative Susceptibility Mapping (QSM)

Quantitative susceptibility mapping is a computational method that uses the magnitude and phase information from a T2\*-weighted gradient recalled echo (GRE) MR sequence to quantify magnetic susceptibility across the brain. This method is useful for distinguishing between different tissue types and quantifying properties like tissue iron deposition.

A recent [QSM consensus paper](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.30006) provides extremely helpful guidance for MR protocol design and QSM analysis methods. Here, we'll highlight one analysis method using the [QSMxT toolbox](https://qsmxt.github.io/QSMxT/) on Oscar.

## QSM scanner protocol

Our protocol is a multi-echo (5 echoes) GRE protocol, with both the magnitude and phase data saved. Parameter choices directly follow the recommendations of the [consensus paper](https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fmrm.29048\&file=mrm29048-sup-0001-Supinfo.pdf), but further tweaks might be needed depending on your specific regions of interest, etc.

{% file src="../.gitbook/assets/anat-MEGRE_acq-qsmconsensus.pdf" %}

For the data to automatically be converted into BIDS format with [xnat2bids](../xnat-to-bids-intro/xnat2bids-software.md), the protocol name needs to be "[BIDS-ready](../xnat/bids-compliant-protocols.md)" and begin with "anat-MEGRE".

## Installing QSMxT on Oscar

The QSMxT toolbox has [recently been fully re-written](https://qsmxt.github.io/QSMxT/getting-started/coming-from-8x/) and is now much easier to install on Oscar:

1. In a terminal on Oscar, download and run the qsmxt installation script\
   `curl -fsSL https://raw.githubusercontent.com/QSMxT/QSMxT/main/install.sh | sh`
2. Close the terminal and open a new one, so that the toolbox is added to your path and ready to use
3.  Check that the toolbox is installed correctly

    ```bash
    qsmxt --version
    qsmxt --help
    ```

## Using QSMxT on Oscar

Visit the [QSMxT documentation](https://qsmxt.github.io/QSMxT/getting-started/quick-start/) for more details on each of these steps and possible settings, and take a look at [their paper - Stewart et al., 2021 -](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.29048) for more information.

1. Get your data into valid BIDS format ([xnat2bids](../xnat-to-bids-intro/using-oscar/oscar-utility-script/) can help you with this!).&#x20;
2. For this first participant, we'll be running the analysis locally on Oscar, so open an OOD Desktop session with at least 15GB of memory.
3.  Open a terminal and launch the qsmxt [interactive terminal user interface](https://qsmxt.github.io/QSMxT/guides/running-interactively/) (TUI)

    ```bash
    qsmxt tui
    ```
4.  Follow the interactive prompts in the Input tab to specify your BIDS directory. By default, the output directory will be in bids/derivatives/qsmxt, but you can specify a different output directory if you'd like. If you only want to analyze a subset of the data in your BIDS directory, you can set "Include" and/or "Exclude" filters to limit the data that is selected.

    <figure><img src="../.gitbook/assets/qsmxt_bids (1).png" alt="enter the full path to the bids directory under &#x22;BIDS directory&#x22;"><figcaption></figcaption></figure>
5. The defaults in the Preprocessing, QSM, and χ-separation tabs are reasonable, so we'll leave them. In the future, you can tailor these further to your analysis needs if you'd like.
6.  Choose any additional outputs you'd like the toolbox to create. Our MEGRE protocol is sufficient for the creation of SWI, SMWI, T2\*, and R2\* maps, segmentation, and the calculation of per-structure statistics. Take a look at the [toolbox documentation](https://qsmxt.github.io/QSMxT/getting-started/quick-start/) for more information on each of these outputs.

    <figure><img src="../.gitbook/assets/Screenshot 2026-11-10 at 11.55.35 AM.png" alt=""><figcaption><p>selecting the SWI/SMWI output options</p></figcaption></figure>



    <figure><img src="../.gitbook/assets/Screenshot 2026-11-10 at 11.56.04 AM.png" alt=""><figcaption><p>selecting the relaxometry output options</p></figcaption></figure>



    <figure><img src="../.gitbook/assets/Screenshot 2026-11-10 at 11.56.25 AM.png" alt=""><figcaption><p>selecting the segmentation output options</p></figcaption></figure>


7. Select "Run" under the "Execution" tab. Keep an eye on your terminal window to monitor progress; you should see the message "All runs completed successfully" when it completes.
8.  Check out the outputs! Unless you specified otherwise, all output files will be in /bids/derivatives/qsmxt.&#x20;

    <figure><img src="../.gitbook/assets/Screenshot 2026-11-10 at 12.21.15 PM.png" alt=""><figcaption></figcaption></figure>
9. The outputs are [described in the qsmxt documentation here](https://qsmxt.github.io/QSMxT/reference/outputs/).&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2024-12-10 at 1.31.15 PM copy.png" alt="An example chimap of the brain, output from qsmxt. This chimpa is overlaid onto the anatomical scan and is viewed from the three planes (coronal, transverse, and sagittal)."><figcaption><p>example chimap</p></figcaption></figure>
