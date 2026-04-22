---
description: >-
  Using the QSMxT toolbox to create whole-brain quantitative magnetic
  susceptibility maps
---

# Quantitative Susceptibility Mapping (QSM)

Quantitative susceptibility mapping is a computational method that uses the magnitude and phase information from a T2\*-weighted gradient recalled echo (GRE) MR sequence to quantify magnetic susceptibility across the brain. This method is useful for distinguishing between different tissue types and quantifying properties like tissue iron deposition.&#x20;

A recent [QSM consensus paper](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.30006) provides extremely helpful guidance for MR protocol design and QSM analysis methods. Here, we'll highlight one analysis method using the [QSMxT toolbox](https://qsmxt.github.io/QSMxT/) on Oscar.

## QSM scanner protocol

Our protocol is a multi-echo (5 echoes) GRE protocol, with both the magnitude and phase data saved. Parameter choices directly follow the recommendations of the [consensus paper](https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fmrm.29048\&file=mrm29048-sup-0001-Supinfo.pdf), but further tweaks might be needed depending on your specific regions of interest, etc. &#x20;

{% file src="../.gitbook/assets/anat-MEGRE_acq-qsmconsensus.pdf" %}

For the data to automatically be converted into BIDS format with [xnat2bids](../xnat-to-bids-intro/xnat2bids-software/), the protocol name needs to be "[BIDS-ready](../xnat/bids-compliant-protocols.md)" and begin with "anat-MEGRE".&#x20;

## Installing QSMxT on Oscar

We largely follow [the QSMxT installation instructions for HPCs](https://qsmxt.github.io/QSMxT/installation#hpc-installation):

1. In a terminal on Oscar, change to whichever directory you would like to install the QSMxT image and scripts into (I have a "scripts" directory in my home directory, but you can put it wherever you'd like).
2.  Clone the toolbox into this directory

    ```bash
    git clone https://github.com/astewartau/transparent-apptainer qsmxt_8.2.2_20260105
    ```
3.  Change directory into this new downloaded folder and run their "transparent singularity/apptainer" script, which sets up your environment in a way that lets you use their tools from the command line, even though they're in a Singularity/Apptainer container

    ```bash
    cd qsmxt_8.2.2_20260105
    ./run_transparent_apptainer.sh --container qsmxt_8.2.2_20260105.simg
    source activate_qsmxt_8.2.2_20260105.simg.sh
    ```
4.  Load the miniforge3 module on Oscar

    ```bash
    module load miniforge3
    source $MAMBA_ROOT_PREFIX/etc/profile.d/conda.sh
    ```
5.  Create a conda environment in which the QSMxT toolbox is installed

    ```bash
    conda create -n qsmxt python=3.8
    conda activate qsmxt
    pip install qsmxt==8.2.2
    ```

Now, any time you want to use the QSMxT toolbox, you'll need to&#x20;

```bash
module load miniforge3
source $MAMBA_ROOT_PREFIX/etc/profile.d/conda.sh
conda activate qsmxt
```



## Using QSMxT on Oscar

Visit the [QSMxT documentation](https://qsmxt.github.io/QSMxT/using-qsmxt/qsmxt) for more details on each of these steps and possible settings, and take a look at [their paper - Stewart et al., 2021 -](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.29048) for more information.

1. Get your data into valid BIDS format ([xnat2bids](../xnat-to-bids-intro/using-oscar/oscar-utility-script/) can help you with this!).
2. Edit your \~/.bashrc file to:
   1. Comment out as many `module load` lines as possible. `module load r/4.4.0-c4wv` causes conflicts via `py-setuptools`, and other modules may as well.
   2. Add a line that says `export APPTAINER_BINDPATH="/path/to/data/directory"` This needs to be a full path to wherever your BIDS data directory is. For example, if my BIDS directory is in `/oscar/data/myusername/xnat-exports/bnc/study-qsm`, I can use `export APPTAINER_BINDPATH="/oscar/data/myusername"` , which will give the QSM apptainer container access to any files in my data directory.
3.  _Open a new terminal_ and activate your qsmxt environment

    ```bash
    module load miniforge3
    source $MAMBA_ROOT_PREFIX/etc/profile.d/conda.sh
    conda activate qsmxt
    ```
4.  Launch qsmxt and give it your bids directory

    ```bash
    qsmxt bids
    ```
5.  Follow the interactive prompts to specify your desired outputs

    <figure><img src="../.gitbook/assets/Screenshot 2024-12-10 at 12.14.59 PM.png" alt="A terminal window where the command “qsmxt bids” was ran. After an automated description of the output options is listed, the user is prompted to type their desired images (space-separated). The default is qsm”. In this example, the user typed: “qsm swi t2s r2s seg analysis”. "><figcaption></figcaption></figure>
6.  Choose your desired pipeline

    <figure><img src="../.gitbook/assets/Screenshot 2024-12-10 at 12.15.15 PM.png" alt="A terminal window where users select a premade QSM pipeline. The default is “default”. In this example, the user typed “default” on the command line. "><figcaption></figcaption></figure>
7.  Take a look at the resulting settings; make any changes necessary, or type `run` to launch the analysis

    <figure><img src="../.gitbook/assets/Screenshot 2024-12-10 at 12.15.59 PM (1).png" alt="The selected QSM settings are printed to the command line. "><figcaption></figcaption></figure>
8. This will automatically create an output directory within your bids directory under /derivatives. If requested, you'll get a QSM map labeled \_Chimap that looks like this!

<figure><img src="../.gitbook/assets/Screenshot 2024-12-10 at 1.31.15 PM copy.png" alt="An example chimap of the brain, output from qsmxt. This chimpa is overlaid onto the anatomical scan and is viewed from the three planes (coronal, transverse, and sagittal). "><figcaption><p>example chimap</p></figcaption></figure>

