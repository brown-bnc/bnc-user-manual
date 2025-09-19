# Table of contents

* [About](README.md)
* [Infrastructure Overview](infrastructure-overview.md)

## XNAT

* [Getting Started](xnat/getting-started.md)
* [Accessing XNAT](xnat/accessing-xnat.md)
* [BIDS Ready Protocols](xnat/bids-compliant-protocols.md)
* [New XNAT projects](xnat/project-creation-in-xnat.md)
* [Uploading Data](xnat/uploading-data.md)
* [Downloading Data](xnat/downloading-data.md)

## Demo Dataset

* [Introduction](demo-dataset/introduction.md)
* [How to access it](demo-dataset/how-to-access-it.md)
* [Protocol Information](demo-dataset/protocol-information.md)

## XNAT to BIDS <a href="#xnat-to-bids-intro" id="xnat-to-bids-intro"></a>

* [Getting Started](xnat-to-bids-intro/getting-started.md)
* [XNAT2BIDS Software](xnat-to-bids-intro/xnat2bids-software/README.md)
* [Exporting to BIDS using Oscar](xnat-to-bids-intro/using-oscar/README.md)
  * [Oscar Utility Script](xnat-to-bids-intro/using-oscar/oscar-utility-script/README.md)
    * [Running xnat2bids using default configuration](xnat-to-bids-intro/using-oscar/oscar-utility-script/running-xnat2bids-using-default-configuration.md)
    * [Running xnat2bids with a custom configuration](xnat-to-bids-intro/using-oscar/oscar-utility-script/running-xnat2bids-with-a-custom-configuration.md)
    * [Syncing your XNAT project & Oscar data directory](xnat-to-bids-intro/using-oscar/oscar-utility-script/syncing-your-xnat-project-and-oscar-data-directory.md)
    * [Extra tools & features](xnat-to-bids-intro/using-oscar/oscar-utility-script/extra-tools-and-features.md)
  * [Step-wise via Interact Session](xnat-to-bids-intro/using-oscar/using-oscar.md)
* [BIDS Validation](xnat-to-bids-intro/bids-validation/README.md)
  * [Oscar](xnat-to-bids-intro/bids-validation/oscar.md)
  * [Docker](xnat-to-bids-intro/bids-validation/docker.md)
* [Converting non-MR data ](xnat-to-bids-intro/converting-non-mr-data/README.md)
  * [Physiological data](xnat-to-bids-intro/converting-non-mr-data/physiological-data.md)
  * [EEG data](xnat-to-bids-intro/converting-non-mr-data/eeg-data.md)

## XNAT TO BIDS (Legacy)

* [Oscar SBATCH Scripts](xnat-to-bids-dive-in/oscar-sbatch-scripts.md)

## BIDS and BIDS Containers <a href="#bids" id="bids"></a>

* [Introduction to BIDS](bids/introduction-to-bids.md)
* [mriqc](bids/mriqc.md)
* [fmriprep](bids/fmriprep.md)
* [BIDS to NIMH Data Archive (NDA)](bids/bids-to-nimh-data-archive-nda.md)

## Analysis Pipelines

* [Task-Based fMRI Analysis Using AFNI](analysis-pipelines/task-based-fmri-analysis-using-afni/README.md)
  * [Single Subject Analysis: Visual/Motor Activation](analysis-pipelines/task-based-fmri-analysis-using-afni/single-subject-analysis-visual-motor-activation.md)
  * [Group Analysis: Visual/Motor Activation](analysis-pipelines/task-based-fmri-analysis-using-afni/group-analysis-visual-motor-activation/README.md)
    * [First-Level Analysis Using afniproc.py](analysis-pipelines/task-based-fmri-analysis-using-afni/group-analysis-visual-motor-activation/first-level-analysis-using-afniproc.py.md)
    * [WIP Second-Level Analysis using gen\_group\_command.py](analysis-pipelines/task-based-fmri-analysis-using-afni/group-analysis-visual-motor-activation/wip-second-level-analysis-using-gen_group_command.py.md)
    * [Second-Level Analysis using gen\_group\_command.py](analysis-pipelines/task-based-fmri-analysis-using-afni/group-analysis-visual-motor-activation/second-level-analysis-using-gen_group_command.py.md)
* [Freesurfer](analysis-pipelines/freesurfer.md)
* [🚧 CONN Toolbox](analysis-pipelines/conn-toolbox.md)
* [Diffusion Weighted Imaging (DWI) Analysis](analysis-pipelines/diffusion-weighted-imaging-dwi-analysis/README.md)
  * [FSL topup and eddy](analysis-pipelines/diffusion-weighted-imaging-dwi-analysis/fsl-topup-and-eddy.md)
  * [Tractography: DSI Studio](analysis-pipelines/diffusion-weighted-imaging-dwi-analysis/untitled.md)
  * [MRtrix3 for Diffusion Imaging Analysis](analysis-pipelines/diffusion-weighted-imaging-dwi-analysis/mrtrix3-for-diffusion-imaging-analysis/README.md)
    * [Step 1: Preprocessing](analysis-pipelines/diffusion-weighted-imaging-dwi-analysis/mrtrix3-for-diffusion-imaging-analysis/step-1-preprocessing.md)
    * [Step 2: Tractography](analysis-pipelines/diffusion-weighted-imaging-dwi-analysis/mrtrix3-for-diffusion-imaging-analysis/step-2-tractography.md)
    * [Step 3: Fixel-Based Analysis](analysis-pipelines/diffusion-weighted-imaging-dwi-analysis/mrtrix3-for-diffusion-imaging-analysis/step-3-fixel-based-analysis.md)
    * [Step 5: Building a Connectome](analysis-pipelines/diffusion-weighted-imaging-dwi-analysis/mrtrix3-for-diffusion-imaging-analysis/step-5-building-a-connectome.md)
* [Brown University MRS Data Collection and Preprocessing Protocol](analysis-pipelines/brown-university-mrs-data-collection-and-preprocessing-protocol/README.md)
  * [PRESS Data Collection on Siemens XA30 System](analysis-pipelines/brown-university-mrs-data-collection-and-preprocessing-protocol/press-data-collection-on-siemens-xa30-system.md)
  * [Organizing Your Data and Preprocessing Using Osprey](analysis-pipelines/brown-university-mrs-data-collection-and-preprocessing-protocol/organizing-your-data-and-preprocessing-using-osprey.md)
* [LC Model](analysis-pipelines/lc-model/README.md)
  * [Installation](analysis-pipelines/lc-model/lcmodel.md)
  * [Example Run](analysis-pipelines/lc-model/example-run.md)
  * [Running LCModel on your own data](analysis-pipelines/lc-model/running-lcmodel-on-your-own-data.md)
* [Quantitative Susceptibility Mapping (QSM)](analysis-pipelines/quantitative-susceptibility-mapping-qsm.md)

## Standalone Tools

* [voxalign: automated MR spectroscopy voxel placement](standalone-tools/voxalign-automated-mr-spectroscopy-voxel-placement/README.md)
  * [Installation](standalone-tools/voxalign-automated-mr-spectroscopy-voxel-placement/installation.md)
  * [Multi-session alignment](standalone-tools/voxalign-automated-mr-spectroscopy-voxel-placement/multi-session-alignment.md)
  * [Center on MNI coordinate](standalone-tools/voxalign-automated-mr-spectroscopy-voxel-placement/center-on-mni-coordinate.md)
  * [Quantify voxel overlap](standalone-tools/voxalign-automated-mr-spectroscopy-voxel-placement/quantify-voxel-overlap.md)
* [dicomsort: a tool to organize DICOM files](standalone-tools/dicomsort-a-tool-to-organize-dicom-files.md)
* [ironmap](standalone-tools/ironmap.md)
* [convert enhanced multi-frame DICOMs to legacy single-frame](standalone-tools/convert-enhanced-multi-frame-dicoms-to-legacy-single-frame.md)
* [DICOM anonymization](standalone-tools/dicom-anonymization.md)

## MRF GUIDES

* [MRI simulator room](mrf-guides/mri-simulator-room/README.md)
  * [Motion Trainer: Balloon Task](mrf-guides/mri-simulator-room/motion-trainer-balloon-task.md)
  * [Simulating scanner triggers](mrf-guides/mri-simulator-room/simulating-scanner-triggers.md)
* [Stimulus display & response collection](mrf-guides/stimulus-display-and-response-collection.md)
* [Eyetracking at the scanner](mrf-guides/eyetracking-at-the-scanner.md)
* [Exporting data via scannershare](mrf-guides/exporting-data-via-scannershare.md)
* [EEG in the scanner](mrf-guides/eeg-in-the-scanner.md)
* [Exporting spectroscopy RDA files](mrf-guides/exporting-spectroscopy-rda-files.md)

## Community

* [MRF/BNC user community meetings](community/mrf-bnc-user-community-meetings.md)

## Motion Trainer

* [Motion Trainer User Guide](motion-trainer/motion-trainer-user-guide/README.md)
  * [Getting Started](motion-trainer/motion-trainer-user-guide/getting-started.md)
  * [Customizing Your Settings](motion-trainer/motion-trainer-user-guide/customizing-your-settings.md)
  * [Advanced Settings](motion-trainer/motion-trainer-user-guide/advanced-settings.md)
  * [Adding Your Own Videos and Images](motion-trainer/motion-trainer-user-guide/adding-your-own-videos-and-images.md)
