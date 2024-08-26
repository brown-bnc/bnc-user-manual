---
description: >-
  This script copies a directory of DICOMs, making modifications to the DICOM
  headers as specified in a configuration .csv file
---

# DICOM anonymization

### Overview

This script reads a configuration csv file like this, and then makes the specified edits to the headers of all DICOMs in the input directory, writing the modified DICOMs to a separate output directory.

{% file src="../.gitbook/assets/demo_config.csv" %}

| Tag                 | Value     |
| ------------------- | --------- |
| PatientBirthDate    | CLEAR     |
| PerformingPhysician | DELETE    |
| PatientID           | Anonymous |

In this configuration file, you'll need a new row for any DICOM tag you want to change, and you can either:

1. specify CLEAR to keep the tag in your DICOM but set its value to empty (as we did here with the birthdate)
2. specify DELETE to delete the tag from the DICOM (although only some DICOM tags can be deleted and still yield a valid DICOM)
3. specify a new value to change it to (here, I changed the Patient ID to "Anonymous").

### Setup

1. First, we need to be in a python environment that contains the package pydicom. You can set up your own environment and `pip install pydicom`, or on Oscar you can simply open a terminal and activate an environment we have already created:\
   \
   `source /oscar/data/bnc/src/python_venvs/pydicom/bin/activate`\
   \
   You will be able to tell that this environment is activated because it will say `(pydicom)` at the beginning of your terminal command prompt. \

2. Create your configuration .csv file (and copy it to Oscar if running there).

### Execution

Finally, we can run the script with:

{% code overflow="wrap" %}
```
python anonymize_dicoms.py -input_dir orig_data -output_dir anonymized_data -config_path demo_config.csv
```
{% endcode %}

This will read all DICOMs in the folder "orig\_data", make the changes specified in the configuration file, and write them out to a new folder "anonymized\_data".\


When you are done, you can deactivate the python environment with `deactivate`.
