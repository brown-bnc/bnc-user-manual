# Organizing Your Data and Preprocessing Using Osprey

## Getting Started with Preprocessing

### Download the data using xnat2bids

For this tutorial, we will use data from demodat2 subject 101 session 1. If you have not downloaded the demo dataset already, you can download this single subject and session data with this custom xnat2bids configuration file.&#x20;

```toml
# Configuring arguments here will override default parameters.
[slurm-args]
mail-user = "example-user@brown.edu"
mail-type = "ALL"

[xnat2bids-args]
sessions = [
    "XNAT_E01849"
    ]
# Skip scanner-derived multi-planar reconstructions & non-distortion-corrected images 
# These are used for MRS voxel placement on the scanner and will cause xnat2bids to fail. 
skipseq=["anat-t1w_acq-memprage_MPR_Cor","anat-t1w_acq-memprage_MPR_Tra","anat-t1w_acq-memprage_MPR_Tra_ND","anat-t1w_acq-memprage RMS_ND","anat-t1w_acq-memprage_MPR_Cor_ND"]
overwrite=true
verbose=1
```

The script will default to placing the BIDS-converted data in a folder called "bids-export" in your home directory; if you'd like to change this location, add a new line at the bottom with your desired path, i.e.: `bids_root="/oscar/home/<example-user>/projectname"` . **For the rest of this tutorial, we will call this path the "$bidsroot".**&#x20;

#### Launch the xnat2bids script

* To use this configuration file and launch this xnat2bids job, open a terminal on the Oscar Open On Demand (OOD) virtual desktop.&#x20;
* Install python and its necessary packages by typing `module load anaconda` .&#x20;
* Copy and paste this configuration file into a text editor and save it wherever you would like (for example, in a scripts folder in your home directory). The file suffix MUST be .toml
* The python script for xnat2bids is located in `/oscar/data/bnc/scripts` . To run xnat2bids from the directory where you saved your .toml configuration file, type the command `python /oscar/data/bnc/scripts/run_xnat2bids.py --config <your_config_filename>` . If you run this command from a different directory than where you saved your config file, make sure to give the full path to it.&#x20;
* You will receive an email when both xnat2bids and the bids-validator launch and are completed.
* Once the job is complete, you will see three output directories created at your bids root. &#x20;
  * `xnat-export` contains the dicoms placed in folders named after the sequences at the scanner. This is where you will find your spectroscopy dicoms.&#x20;
  * `bids` contains all subdirectories required in the BIDS specification. Here you will find your converted anatomical NIFTIs. This is also where the output of your preprocessing will go (in derivatives).&#x20;
  * `logs` contains the log files from the xnat2bids job.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-27 at 1.39.07 PM.png" alt=""><figcaption><p>The structure of output directories after running xnat2bids for sub-101 ses-01 of demodat2. In this case, the bids root is "Demodat2_documentation".  </p></figcaption></figure>

### Organizing the Spectroscopy Data According to the BIDS Specification&#x20;

Unlike other types of MRI sequences (functional, diffusion, anatomical, etc), xnat2bids does not currently convert MRS dicoms into NIFTIs or move them into the `sourcedata` or `bids` directories. It also cannot upload the RDA or twix files to Oscar. These steps will need to be completed manually before beginning preprocessing. Osprey only requires a few files to successfully run (T1 anatomical NIFTI and the water reference/metabolite RDAs), but it is good practice to organize all of your data in accordance with the [BIDS Specification](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/magnetic-resonance-spectroscopy.html).&#x20;

#### Place all necessary files into sourcedata&#x20;

{% hint style="info" %}
The [Osprey documentation](https://schorschinho.github.io/osprey/getting-started.html#how-to-organize-your-raw-data) notes that when performing MRS preprocessing on data acquired on a Siemens MRI, it is absolutely necessary to separate the dicoms/RDAs into separate folders based on scan.&#x20;
{% endhint %}

* In the `sourcedata` directory, create a new folder called `mrs`. Within `mrs`, subfolders must be created for each spectroscopy run (i.e., there should be separate folders for each VOI and for the water reference and metabolite runs). These can be named anything you want.&#x20;
* In this example there was only one VOI, the left anterior cingulate cortex (Lacc). The subfolders for the water reference and metabolite scans were manually created and named Lacc\_mrsref and Lacc\_svs, respectively.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-27 at 2.08.57 PM.png" alt=""><figcaption></figcaption></figure>

* Place the scan's dicoms inside the individual `mrs` subdirectories
  * You can find all of the session's dicoms at `<$bidsroot>/bnc/study-demodat2/xnat-export/sub-101/ses-01.` Once in that directory, find the spectroscopy water reference scan by typing `cd mrs-mrsref_acq-PRESS_voi-Lacc` .  The metabolite (svs) scan is located in `$bidsroot>/bnc/study-demodat2/xnat-export/sub-101/ses-01/mrs-svs_acq-PRESS_voi-Lacc` . Copy each dicom into its relevant directory that you just created in `$bidsroot/bnc/study-demodat2/bids/sourcedata/sub-101/ses-01/mrs/` .&#x20;
* Then copy the corresponding RDA and twix files (saved to your drive via scannershare).&#x20;
* You can download the RDA files for sub-101 ses-01 of demodat2 here:&#x20;

{% file src="../../.gitbook/assets/sub-101_ses-01_RDAs (1).zip" %}
RDA files for sub-101 ses-01 of demodat2. The file "mrsref/101.MR.BNC DEMODAT2.24.1.162615.rda" corresponds to the water reference scan, and "svs/101.MR.BNC DEMODAT2.25.1.162616.rda" corresponds to the metabolite/svs scan.&#x20;
{% endfile %}

* For the sake of this tutorial you do not need the twix files, but typically you should see three files in each sourcedata mrs subdirectory:  1) the dicom, 2) the RDA, and 3) the twix (.dat).&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-27 at 3.40.51 PM.png" alt=""><figcaption><p>Navigate into one of the <code>mrs</code> subdirectories (in <code>sourcedata</code>) and list the contents. </p></figcaption></figure>

#### Convert the Spectroscopy dicoms into NIFTIs

* spec2nii is a package that allows you to convert spectroscopy dicoms into NIFTIs, rename them, and move them to any desired directory. It is built into FSL, so you can access it by typing `module load fsl` in the OOD terminal. We will now use this command to convert the dicoms and ensure BIDS compatibility in our dataset.
  * From within the `mrs-mrsref_acq-PRESS_voi-Lacc`  directory, type:

```
spec2nii dicom -j -f sub-101_ses-01_acq-PRESS_voi-Lacc_mrsref -o <$bidsroot>/bnc/study-demodat2/bids/sub-101/ses-01/mrs/ 1.3.12.2.1107.5.2.43.67050.30000025030414003908900000017-24-1-zkc899.dcm
```

{% hint style="info" %}
**More information on the spec2nii command:**

**spec2nii:** the name of the command used for MRS dicom to nifti conversion. This is built into FSL but can also be downloaded on [github](https://github.com/wtclarke/spec2nii).&#x20;

**dicom:** indicates that the file handed to spec2nii is a dicom.&#x20;

**-j:** specifies the creation of a .json sidecar along with the NIFTI. This is necessary for BIDS compatibility.&#x20;

**-f:** specifies the output file name. This file name was chosen based on the [BIDS recommendation](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/magnetic-resonance-spectroscopy.html). The "\*\_mrsref" suffix indicates that this is the water reference scan.&#x20;

Lastly, include the name of the dicom file which will be converted.
{% endhint %}

* Although this step is not necessary in order to run a preprocessing pipeline using Osprey, it is recommended so that your data is consistent with the BIDS specification.&#x20;

#### Unzip the T1w Anatomical Scans So They Can Be Read by Osprey

* Osprey requires an unzipped NIFTI file for your T1w anatomical input. xnat2bids outputs a zipped NIFTI which can be found here: `$bidsroot/bnc/study-demodat2/bids/sub-101/ses-01/anat/sub-101_ses-01_acq-memprageRMS_T1w.nii.gz` .
* Navigate to the directory containing this file and type this command:&#x20;

```
gunzip sub-101_ses-01_acq-memprageRMS_T1w.nii.gz
```

* You should now see an unzipped NIFTI in this directory (`sub-101_ses-01_acq-memprageRMS_T1w.nii)` .&#x20;

#### Prepare Your Output Directories

In your BIDS `derivatives` folder, make a new folder called `osprey` . Within that, make subdirectories for your subject (`sub-101`) and session (`ses-01`). You will save your Osprey outputs here.&#x20;

### Setting Up Osprey on Oscar

* In the OOD Virtual Desktop, download SPM12 (not 25) to your home directory from the [SPM github](https://github.com/spm/spm12) and unzip the file. Instructions on downloading SPM can be found [here](https://www.fil.ion.ucl.ac.uk/spm/software/download/).&#x20;

```
unzip spm12.zip
```

* Download Osprey to your home directory from github by opening a new terminal and enter the following command:

```
git clone https://github.com/schorschinho/osprey.git 
```

* It is important that both Osprey and SPM12 are located in the same directory (even if you choose to save them into something other than `/oscar/home/<example-username>` ).&#x20;
* To use Osprey, you need to open Matlab:

```
module load matlab/R2023a-xd6f7ph
matlab-threaded
```

* Osprey requires three additional packages that need to be installed in Matlab:
  * In the top right-hand corner of the Matlab GUI, click the “Add-Ons” button and select “Get Add-Ons”.
  * Once the Add-On Explorer pops up, sign into your Brown MathWorks account.
  * Search and install the three following toolboxes:
    * GUI Layout Toolbox
    * Widgets Toolbox
    * Widgets Toolbox - Compatibility Support
* Once the Matlab interface pops up, you will want to add SPM12, Osprey, and your project folder to your path. Do NOT add SPM12 subfolders to your Matlab path, this will cause Osprey to fail. Add only the top-level SPM12 directory. You can do this by copy and pasting the following commands into the matlab terminal (and filling in your username and $bidsroot).&#x20;

```matlab
addpath('/oscar/home/example-username/spm12')
addpath(genpath('/oscar/home/example-username/osprey'))
addpath(genpath('/oscar/home/example-username/$bidsroot'))
```

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 1.56.09 PM.png" alt=""><figcaption></figcaption></figure>

## Using Osprey to Preprocess your Data

### Creating a New Job in Osprey and Inputting your Data

• Launch the Osprey GUI from the Matlab command line (code is case sensitive).

```
Osprey
```

* Click “Create job” and the “Interactive Osprey job file generator” will pop up on your screen.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 1.57.58 PM.png" alt=""><figcaption><p>Type 'Osprey' into the command window of MATLAB to open the Osprey Startup window. Then press "Create Job" to open the jobfile generator. </p></figcaption></figure>

* How you specify information in the jobfile generator will depend on your sequence type and what files you want to extract. This example will walk you through an unedited PRESS acquisition.
  * In section 1, "Specify Sequence Information”:
    * &#x20;Do not change any of the input values.
  * In section 2, “Specify Data Handling and Modeling Options”:
    * Keep all input values the same.&#x20;
    * Check off the “Save PDF” box.&#x20;
    * Click “basis set folder” and select the appropriate basis set folder from the Osprey package: `/oscar/home/username/osprey/fit/basissets/3T/siemens/unedited/press/30`
    * Now, click “basis set file” and select the appropriate basis set file (.mat) from this folder: `/oscar/home/username/osprey/fit/basissets/3T/siemens/unedited/press/30/basis_siemen s_press30.mat`
      * Note: Do not use any basis sets provided by LCModel. The file type (.basisset) is not compatible with Osprey, as Osprey requires a matlab file input (.m).
  * In section 3, “Specify MRS and Anatomical Imaging Files":
    * Click “MRS data” and select the metabolite (svs) RDA file: `$bidsroot/bnc/study-demodat2/bids/sourcedata/sub-101/ses-01/mrs/Lacc_svs/*.RDA`
    * Click “H2O Reference” and select the water reference RDA file: `$bidsroot/bnc/study-demodat2/bids/sourcedata/sub-101/ses-01/mrs/Lacc_mrsref/*.RDA`
    * &#x20;Click “T1 Data (nifti \*.nii)” and select your T1-weighted image that has been converted to NIFTI and unzipped: `$bidsroot/bnc/study-demodat2/bids/sub-101/ses-01/anat/sub-101_ses-01_acq-memprageRMS_T1w.nii`
    * Do not input data for “H2O Short TE” or “Metabolite-Nulled” or select the “DICOM T1 data (GE only)” button.
  * In section 4, “Specify Output Folder":
    * Click “Output Folder” and select the subject/session folder that you created in the “derivatives” folder of your project: `$bidsroot/bnc/study-demodat2/bids/derivatives/osprey/sub-101/ses-01/`
    * Change the “Job Name” to your subject ID and the date: “sub101ses01mmddyyyy”.
      * You do not have to input anything for the “Stat csv File”.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 2.53.43 PM.png" alt=""><figcaption><p>The jobfile generator, with necessary fields underlined in red. After filling in each field with your specific folders/file information, press the "Create Job" button on the bottom left. </p></figcaption></figure>

* Click the “CREATE JOB” button at the bottom.
  * It will take a few seconds to load, but the Osprey window should then pop up.
* On the left hand side of the screen, click “Save MRS Cont". This allows you to save the container so you don’t have to re-do the job file inputs if you want to open this participant in Osprey again. It will save as a matlab script file (.m) with the name specified in the "Job Name" field: `$bidsroot/bnc/study-demodat2/bids/derivatives/osprey/sub-101/ses-01/sub101ses01mmddyyyy.m`

### Walking through the Osprey Preprocessing Pipeline&#x20;

#### Load Data

* Click the “Load data” button in the top left hand corner of the Osprey GUI. This will load in your RDA file.
  * This will output the subspectra from your RDA file. Because the data in the RDA file is already coil combined, there will only be one mean subspectrum that has already been preprocessed.
  * This output can be seen under the “Raw” tab at the top at any point when Osprey is running your container.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 2.57.42 PM.png" alt=""><figcaption><p>Output of the 'Load Data' Step can be viewed in the "Raw" tab.</p></figcaption></figure>

{% hint style="info" %}
Steps appearing in blue on the left hand panel are available to run. Once you have completed a step, it will turn gray. As you progress through the the pipeline, new steps will become available. For example, you cannot run segment until you have already run CoRegister.&#x20;
{% endhint %}

#### Process Data

* Click the “Process data” button (which should now be in blue letters because the Load data step ran correctly). This step is meant to show you how the data are preprocessed via alignment, averaging, and accounting for chemical shift drift.&#x20;
  * Again, because our data is already coil combined, you will only see one averaged spectrum under “Pre-alignment,” “Post-alignment,” and “Aligned and averaged”- they will all be the same original spectrum you saw on the “Raw” tab.
  * This output can be seen under the “Processed” tab at the top.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 2.59.25 PM.png" alt=""><figcaption><p>Output of the "Process Data" step, viewed in the "Processed" tab. </p></figcaption></figure>

#### Model data

* Click the “Model data” button. This step fits your metabolite data to the basis set provided by Osprey.
  * This provides a metabolite fit plot separated by each metabolite of interest. The “Raw Water Ratio” values on the left hand side are NOT your final usable values! They have not been corrected for water, CSF, or tissue values. This is similar to the output you would get from LCModel.
  * This data exists under the “LCmodel” tab at the top of the screen.
  * If you want to check that your water reference file looks correct, go to the bottom left hand corner and click the “ref” tab to see.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 3.01.42 PM.png" alt=""><figcaption><p>Out of the 'Model Data" step, viewed in the "LC Model" Tab. </p></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 3.01.51 PM.png" alt=""><figcaption><p>The LC Model "ref" tab, accessed via the bottom left of the graph. </p></figcaption></figure>

#### CoRegister

* Next, click the “CoRegister” button. This step allows you to coregister the MRS data to the anatomical data, to see where your voxel was placed on the T1-weighted image in the coronal, axial, and horizontal planes.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 3.03.49 PM.png" alt=""><figcaption><p>Output of the "Coregister" step, accessed via the "Cor/Seg" tab. Here you can view the MRS voxel placement (Lacc) overlaid on the T1w scan. </p></figcaption></figure>

#### Segment

* Click the “Segment” button. This step may take a few minutes so do not be alarmed if you don’t get an output right away. This step segments the tissue types within your voxel, providing a percentage of gray matter, white matter, and cerebrospinal fluid (CSF). These percentages are necessary for properly quantifying your metabolite levels, as you want to remove any CSF effects and only focus on metabolite levels in the gray matter.
  * Now the coregistration image and segmentation image will both appear on the screen.
  * This data will exist under the “Cor/Seg” tab at the top of the GUI.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 3.34.23 PM.png" alt=""><figcaption><p>Output of the "Segment" step. Again, this can be viewed in the same "Cor/Seg" tab as the previous step. </p></figcaption></figure>

{% hint style="info" %}
This step will fail if it is handed an unzipped NIFTI (\*.nii.gz) for the T1w anatomical scan. This may happen for two reasons: 1) You may have entered the zipped NIFTI in the job file generator by mistake, in which case you must remake the job file and start over. 2) There seems to be a bug in Osprey, where the T1 anatomical NIFTI is sometimes automatically deleted after the "CoRegistration" step. If you are seeing that your Segmentation step is failing, and you put the correct file in the job file generator, try looking inside your `anat` directory. If the \*.nii file is missing, you can unzip the \*.nii.gz file, go back into the Osprey GUI, and press "Segmentation" again.&#x20;
{% endhint %}

#### Quantify

Finally, click the “Quantify” button. This step provides your final metabolite values that are corrected for water, T1 & T2 relaxation constants, and CSF.

* Under the “Quantified” tab, you will see a table of your metabolite values with tCr referencing, raw water scaling, CSF and water scaling, and tissue correction and water scaling using the Gasparovic method. To choose which type of corrected metabolite values are best for you, see the Osprey paper by [Oeltzschner et al. (2020)](https://pubmed.ncbi.nlm.nih.gov/32603810/).&#x20;
  * These results are in individual tsv files in the `QuantifyResults` folder in `$bidsroot/bnc/study-demodat2/bids/derivatives/osprey/sub-101/ses-01/` .

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 3.54.34 PM.png" alt=""><figcaption><p>Table of metabolite values with various forms of scaling/correcting, viewed in the "Quantified" tab of the Osprey GUI.</p></figcaption></figure>

#### Overview

* Finally, in the “Overview” tab you can view the mean spectra across all datasets (if you have multiple rda files) and individual quantification tables.
* Save your MRS container by clicking “Save MRSCont” before you exit out of Osprey.
* If you did not select “Save PDF” in step 2 of the “Interactive Osprey jobfile generator,” and would like the images of your spectrum and your coregistered voxel, you can click the “Save PDF” button in the upper righthand corner to export it and it will be in the `Figures` folder under your subject/session folder in `derivatives`.
* Further tutorials of the GUI can be found on the [Osprey website.](https://schorschinho.github.io/osprey/)&#x20;
