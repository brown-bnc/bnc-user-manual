---
description: >-
  Using the QSMxT toolbox to create whole-brain quantitative magnetic
  susceptibility maps
---

# Quantitative Susceptibility Mapping (QSM)

Quantitative susceptibility mapping is a computational method that uses the magnitude and phase information from a T2\*-weighted gradient recalled echo (GRE) MR sequence to quantify magnetic susceptibility across the brain. This method is useful for distinguishing between different tissue types and quantifying properties like tissue iron deposition.&#x20;

A recent [QSM consensus paper](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.30006) provides extremely helpful guidance for MR protocol design and QSM analysis methods. Here, we'll highlight one analysis method using the [QSMxT toolbox](https://qsmxt.github.io/QSMxT/) on Oscar.

### QSM scanner protocol

Our protocol is a multi-echo (5 echoes) GRE protocol, with both the magnitude and phase data saved. Parameter choices directly follow the recommendations of the [consensus paper](https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fmrm.29048\&file=mrm29048-sup-0001-Supinfo.pdf), but further tweaks might be needed depending on your specific regions of interest, etc. &#x20;

{% file src="../.gitbook/assets/anat-MEGRE_acq-qsmconsensus.pdf" %}

For the data to automatically be converted into BIDS format with [xnat2bids](../xnat-to-bids-intro/xnat2bids-software/), the protocol name needs to be "[BIDS-ready](../xnat/bids-compliant-protocols.md)" and begin with "anat-MEGRE".&#x20;

### Installing QSMxT on Oscar

We largely follow [their installation instructions for HPCs](https://qsmxt.github.io/QSMxT/installation#hpc-installation):

1. In a terminal on Oscar, change to whichever directory you would like to install the QSMxT image and scripts into (I have a "scripts" directory in my home directory, but you can put it wherever you'd like).
2.  Clone the toolbox into this directory

    ```
    git clone https://github.com/astewartau/transparent-apptainer qsmxt_8.2.2_20251216
    ```
3.  Change directory into this new downloaded folder and run their "transparent singularity" script, which sets up your environment in a way that lets you use their tools from the command line, even though they're in a Singularity/Apptainer container

    <pre><code><strong>cd qsmxt_8.2.2_20251216
    </strong>./run_transparent_apptainer.sh --container qsmxt_8.2.2_20251216.simg
    source activate_qsmxt_8.2.2_20251216.simg.sh
    </code></pre>
4.  Load the miniforge3 module on Oscar

    ```
    module load miniforge3
    source $MAMBA_ROOT_PREFIX/etc/profile.d/conda.sh
    ```
5.  Create a conda environment in which the QSMxT toolbox is installed

    ```
    conda create -n qsmxt python=3.11
    conda activate qsmxt
    pip install qsmxt==8.2.2
    ```

Now, any time you want to use the QSMxT toolbox, you'll need to&#x20;

```
module load miniforge3
source $MAMBA_ROOT_PREFIX/etc/profile.d/conda.sh
conda activate qsmxt
```



### Using QSMxT on Oscar

Visit the [QSMxT documentation](https://qsmxt.github.io/QSMxT/using-qsmxt/qsmxt) for more details on each of these steps and possible settings, and take a look at [their paper - Stewart et al., 2021 -](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.29048) for more information.

1. Get your data into valid BIDS format ([xnat2bids](../xnat-to-bids-intro/using-oscar/oscar-utility-script/) can help you with this!).
2.  Activate your qsmxt environment

    ```
    module load miniforge3
    source $MAMBA_ROOT_PREFIX/etc/profile.d/conda.sh
    conda activate qsmxt
    ```
3.  Launch qsmxt and give it your bids directory

    ```
    qsmxt bids
    ```
4.  Follow the interactive prompts to specify your desired outputs

    <figure><img src="../.gitbook/assets/Screenshot 2024-12-10 at 12.14.59 PM.png" alt=""><figcaption></figcaption></figure>
5.  Choose your desired pipeline

    <figure><img src="../.gitbook/assets/Screenshot 2024-12-10 at 12.15.15 PM.png" alt=""><figcaption></figcaption></figure>
6.  Take a look at the resulting settings; make any changes necessary, or type `run` to launch the analysis

    <figure><img src="../.gitbook/assets/Screenshot 2024-12-10 at 12.15.59 PM (1).png" alt=""><figcaption></figcaption></figure>
7. This will automatically create an output directory within your bids directory under /derivatives. If requested, you'll get a QSM map labeled \_Chimap that looks like this!

<figure><img src="../.gitbook/assets/Screenshot 2024-12-10 at 1.31.15 PM copy.png" alt=""><figcaption><p>example chimap</p></figcaption></figure>

