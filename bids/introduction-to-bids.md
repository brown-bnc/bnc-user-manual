# Introduction to BIDS

The Brain Imaging Data Structure (BIDS) provides a simple and intuitive way to organize and describe your neuroimaging and behavioral data. It has been widely adopted as a standard that many processing pipelines understand.&#x20;

## BIDS Specification

The main specification lives here [https://bids-specification.readthedocs.io/en/stable/](https://bids-specification.readthedocs.io/en/stable/)

### Organization Principles

BIDS principles can be summarized as:

* NIFTI files are the chosen imaging format
* Key data is accompanied by `json` file providing parameters and descriptions
* Folder structure and files are named in a consistant manner as prescribed by the specification

### Directory Structure

Overall directories hierarchy is as foolows (\[] indicates optional fields):

* sub-\<participant\_label>\[/ses-\<session\_label>]/\<data\_type>/&#x20;
* \[code/]&#x20;
* \[derivatives/]&#x20;
* \[stimuli/]
* \[sourcedata/]

#### Single Session Example

* ** sub-control01 **
  * **anat**
    * sub-control01\_T1w.nii.gz sub-control01\_T1w.json&#x20;
    * sub-control01\_T2w.nii.gz sub-control01\_T2w.json
  * **func**
    * sub-control01\_task-nback\_bold.nii.gz&#x20;
    * sub-control01\_task-nback\_bold.json&#x20;
    * sub-control01\_task-nback\_events.tsv&#x20;
    * sub-control01\_task-nback\_physio.tsv.gz&#x20;
    * sub-control01\_task-nback\_physio.json&#x20;
    * sub-control01\_task-nback\_sbref.nii.gz
  * **dwi**
    * sub-control01\_dwi.nii.gz&#x20;
    * sub-control01\_dwi.bval&#x20;
    * sub-control01\_dwi.bvec
  * **fmap**
    * sub-control01\_phasediff.nii.gz&#x20;
    * sub-control01\_phasediff.json&#x20;
    * sub-control01\_magnitude1.nii.gz
    * sub-control01\_scans.tsv

Additional files and folders containing raw data may be added as needed for special cases. They should be named using all lowercase with a name that reflects the nature of the scan (e.g., “calibration”). Naming of files within the directory should follow the same scheme as above (e.g., “sub-control01\_calibration\_Xcalibration.nii.gz”)

#### BIDS Entity Table

The names of the file depends on modality, aquisition parameters and other considerations. The[ BIDS Entity Table](https://bids-specification.readthedocs.io/en/stable/99-appendices/04-entity-table.html) table compiles the entities (key-value pairs) described throughout the specification, and establishes a common order within a filename. For example, if a file has an acquisition and reconstruction label, the acquisition entity must precede the reconstruction entity.&#x20;

#### Format considerations

* Filenames are case sensitive
* Recommended: Zero-padding for subjects i.e sub\_01
* NOT Recommended: Zero-padding for runs and echo (and they MUST be integers)
* Units: SI
* Time: YYYY-MM-DDThh:mm:ss
