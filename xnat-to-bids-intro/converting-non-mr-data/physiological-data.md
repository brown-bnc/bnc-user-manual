# Physiological data

Physiological data collected at the scanner is automatically exported as single DICOM files alongside each fMRI run. When you [transfer your data to XNAT](../../xnat/uploading-data.md), this data will come along, named the same as its associated functional run but with a \_WIP\_PMU suffix (or just \_PMU, before the XA30 scanner software upgrade).

<figure><img src="../../.gitbook/assets/Screenshot 2024-04-05 at 12.17.41 PM.png" alt=""><figcaption><p>Paired fMRI and physiological data on XNAT</p></figcaption></figure>

When you use xnat-tools to export your data and convert it to BIDS format, the physiological data should come along and be converted automatically. If you are exporting your data to Oscar, we recommend using our new [Oscar utility script](../using-oscar/oscar-utility-script.md).&#x20;

When the xnat2bids pipeline has finished, you can find your raw physiological data DICOM files in `export-dir/PI/study-XX/xnat-export/sub-XX/ses-XX/`, along with the DICOMs for your brain data. Xnat-tools will also automatically extract the pulse and respiration traces from the physiological DICOMs and create the cardiac and respiratory .tsv.gz and .json files associated with each functional run in `export-dir/PI/study-XX/bids/sub-XX/ses-XX/func`, as prescribed by the [BIDS specification](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/06-physiological-and-other-continuous-recordings.html).

`sub-XX_ses-XX_task-XX_acq-XX_run-01_bold.json`&#x20;

`sub-XX_ses-XX_task-XX_acq-XX_run-01_bold.nii.gz`&#x20;

`sub-XX_ses-XX_task-XX_acq-XX_run-01_events.tsv`&#x20;

`sub-XX_ses-XX_task-XX_acq-XX_run-01_recording-cardiac_physio.json`&#x20;

`sub-XX_ses-XX_task-XX_acq-XX_run-01_recording-cardiac_physio.tsv.gz`&#x20;

`sub-XX_ses-XX_task-XX_acq-XX_run-01_recording-respiratory_physio.json`&#x20;

`sub-XX_ses-XX_task-XX_acq-XX_run-01_recording-respiratory_physio.tsv.gz`
