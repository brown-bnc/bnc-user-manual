# Introduction to BIDS

The Brain Imaging Data Structure \(BIDS\) provides a simple and intuitive way to organize and describe your neuroimaging and behavioral data. It has been widely adopted as a standard that many processing pipelines understand. 

## BIDS Specification

The main specification lives here [https://bids-specification.readthedocs.io/en/stable/](https://bids-specification.readthedocs.io/en/stable/)

### Organization Principles

BIDS principles can be summarized as:

* NIFTI files are the chosen imaging format
* Key data is accompanied by `json` file providing parameters and descriptions
* Folder structure and files are named in a consistant manner as prescribed by the specification

### Directory Structure

Overall directories hierarchy is as foolows \(\[\] indicates optional fields\):

* sub-&lt;participant\_label&gt;\[/ses-&lt;session\_label&gt;\]/&lt;data\_type&gt;/ 
* \[code/\] 
* \[derivatives/\] 
* \[stimuli/\]
* \[sourcedata/\]

#### Single Session Example

*  **sub-control01** 
  * **anat**
    * sub-control01\_T1w.nii.gz sub-control01\_T1w.json 
    * sub-control01\_T2w.nii.gz sub-control01\_T2w.json
  * **func**
    * sub-control01\_task-nback\_bold.nii.gz 
    * sub-control01\_task-nback\_bold.json 
    * sub-control01\_task-nback\_events.tsv 
    * sub-control01\_task-nback\_physio.tsv.gz 
    * sub-control01\_task-nback\_physio.json 
    * sub-control01\_task-nback\_sbref.nii.gz
  * **dwi**
    * sub-control01\_dwi.nii.gz 
    * sub-control01\_dwi.bval 
    * sub-control01\_dwi.bvec
  * **fmap**
    * sub-control01\_phasediff.nii.gz 
    * sub-control01\_phasediff.json 
    * sub-control01\_magnitude1.nii.gz
    * sub-control01\_scans.tsv

Additional files and folders containing raw data may be added as needed for special cases. They should be named using all lowercase with a name that reflects the nature of the scan \(e.g., “calibration”\). Naming of files within the directory should follow the same scheme as above \(e.g., “sub-control01\_calibration\_Xcalibration.nii.gz”\)

#### BIDS Entity Table

The names of the file depends on modality, aquisition parameters and other considerations. The[ BIDS Entity Table](https://bids-specification.readthedocs.io/en/stable/99-appendices/04-entity-table.html) table compiles the entities \(key-value pairs\) described throughout the specification, and establishes a common order within a filename. For example, if a file has an acquisition and reconstruction label, the acquisition entity must precede the reconstruction entity. 

#### Format considerations

* Filenames are case sensitive
* Recommended: Zero-padding for subjects i.e sub\_01
* NOT Recommended: Zero-padding for runs and echo \(and they MUST be integers\)
* Units: SI
* Time: YYYY-MM-DDThh:mm:ss

