---
description: >-
  We are continuing to develop run_xnat2bids.py and xnat-tools, so please get in
  touch with any new feature suggestions!
---

# Extra tools & features

### Correct DICOM headers during XNAT export

{% hint style="warning" %}
Use this tool responsibly! Modifying DICOM headers can create corrupt or invalid DICOM data if not done correctly. (Although your data on XNAT will not be modified, so you can always re-export if necessary)
{% endhint %}

If you have any corrections you need to make to your DICOMs, you can create a .json file that lists the scan(s) to be modified, DICOM field(s) to be changed, and the new value(s) you'd like to change it/them to. This can be useful, for example if your participant was registered with their actual birthdate but you'd like to change it to a pseudo birthdate (e.g. Jan 1st, birth year) before further analyzing and/or sharing the data.&#x20;

For example, say that I am exporting the data from demodat subject 004, and I would like to 1) correct the birth date to 19880101 and 2) change the Patient ID to "Anonymous".&#x20;

<details>

<summary>This is how I would set up my json file</summary>

```json
{
    "mappings": [
        {
            "scans_to_correct": [
                "anat-scout_acq-localizer",
                "anat-scout_acq-aascout",
                "anat-scout_acq-aascoutMPRsag",
                "anat-scout_acq-aascoutMPRcor",
                "anat-scout_acq-aascoutMPRtra",
                "anat-T1w_acq-memprage",
                "anat-T1w_acq-memprageRMS",
                "fmap_acq-boldGRE",
                "func-bold_task-checks_run-01",
                "func-bold_task-checks_run-02",
                "func-bold_task-motionloc",
                "func-bold_task-resting",
                "dwi_acq-b1500_dir-ap_SBRef",
                "dwi_acq-b1500_dir-ap",
                "dwi_acq-b1500_dir-apTENSOR",
                "fmap_acq-diffSE_dir-ap",
                "dwi_acq-b1500_dir-pa_SBRef",
                "dwi_acq-b1500_dir-pa",
                "dwi_acq-b1500_dir-paTENSOR",
                "fmap_acq-diffSE_dir-pa"
            ],
            "dicom_field": "PatientBirthDate",
            "new_value": "19880101"
        },
        {
            "scans_to_correct": [
                "anat-scout_acq-localizer",
                "anat-scout_acq-aascout",
                "anat-scout_acq-aascoutMPRsag",
                "anat-scout_acq-aascoutMPRcor",
                "anat-scout_acq-aascoutMPRtra",
                "anat-T1w_acq-memprage",
                "anat-T1w_acq-memprageRMS",
                "fmap_acq-boldGRE",
                "func-bold_task-checks_run-01",
                "func-bold_task-checks_run-02",
                "func-bold_task-motionloc",
                "func-bold_task-resting",
                "dwi_acq-b1500_dir-ap_SBRef",
                "dwi_acq-b1500_dir-ap",
                "dwi_acq-b1500_dir-apTENSOR",
                "fmap_acq-diffSE_dir-ap",
                "dwi_acq-b1500_dir-pa_SBRef",
                "dwi_acq-b1500_dir-pa",
                "dwi_acq-b1500_dir-paTENSOR",
                "fmap_acq-diffSE_dir-pa"
            ],
            "dicom_field": "PatientID",
            "new_value": "Anonymous"
        }
    ]
}
```

</details>

After saving it as "x2b\_demodat\_dicomfix\_config.json" on Oscar, I just need to add one line to the \[xnat2bids-args] section of my [configuration file](running-xnat2bids-with-a-custom-configuration.md#id-2.-configure-xnat2bids-parameters):

```
dicomfix-config="/oscar/home/elorenc1/scripts/demodat/x2b_demodat_dicomfix_config.json"
```

Then, launch run\_xnat2bids.py as usual. Be sure to check your output log file when your job completes - it will print INFO messages as it makes changes to DICOMs:

`INFO Modified PatientBirthDate in /users/elorenc1/bids-export/bnc/study-demodat/xnat-export/sub-004/ses-01/anat-scout_acq-localizer/1.3.12.2.1107.5.2.43.67050.30000022051915365316000000043-1-1-n8iroc.dcm: 19880101`

and WARNING messages if it runs into any trouble:

`WARNING PatientsBirthDate field is not present in /users/elorenc1/bids-export/bnc/study-demodat/xnat-export/sub-004/ses-01/fmap_acq-boldGRE/1.3.12.2.1107.5.2.43.67050.30000022051915365316000000043-8-11-178dtrw.dcm.`

