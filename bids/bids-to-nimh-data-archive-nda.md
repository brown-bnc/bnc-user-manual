# BIDS to NIMH Data Archive (NDA)

To help users comply with data sharing requirements from the NIMH, we are extending [a tool from the BIDS folks](https://github.com/bids-standard/bids2nda) that automatically converts BIDS-formatted MR data into the format required by the NIMH.  This tool is a work in progress, so please get in touch with any issues or suggested features!

***

## Preparing your data

### Step 1: Get MR data into valid [BIDS format](https://bids-specification.readthedocs.io/en/stable/)

If you are using XNAT and have worked with us to set up your protocol to be [BIDS-friendly](../xnat/bids-compliant-protocols.md), follow [these steps](../xnat-to-bids-intro/using-oscar/oscar-utility-script/) to pull your data from XNAT to Oscar and automatically convert it into BIDS format.&#x20;

### Step 2: Convert behavioral data into BIDS format

If you are converting fMRI task data, you will need to do some additional work to also convert your behavioral data into the [\_events.tsv files required by BIDS](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/task-events.html). You can find an example using our demodat dataset [here](../analysis-pipelines/task-based-fmri-analysis-using-afni/single-subject-analysis-visual-motor-activation.md#step-2-extract-stimulus-timing-information-from-stimulus-presentation-output-files).&#x20;

### Step 3: Add stimulus information and stimulus files

If you have stimulus files that you would also like to include in your upload to the NDA, make sure to include stimulus information in the stim\_file column of your \_events.tsv files like this:

<figure><img src="../.gitbook/assets/Screenshot 2024-04-03 at 3.33.53 PM.png" alt=""><figcaption></figcaption></figure>

The BIDS spec assumes that these files live in a "stimuli" folder at the top level of your BIDS directory like this:&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2024-04-03 at 3.38.36 PM.png" alt=""><figcaption><p>Including stimuli in your BIDS structure</p></figcaption></figure>

If you want to organize the stimuli further, you can have subfolders within your "stimuli" folder, and then include the subfolder in the stim\_file field. For example, if you want to put all the stimuli sub-001 saw in a folder called "001" within the "stimuli" folder, your events.tsv file would have 001/001\_stim1.png, etc. in the stim\_file column.

### Step 4: Create GUIDs and BIDS ID-to-GUID mapping file

NIMH requires that each participant be assigned a ["Global Unique Identifier" or GUID, created with their tool](https://nda.nih.gov/nda/nda-tools). Once you have done this for each participant, you need to create a text file that contains each of your BIDS subject IDs and the associated GUIDs. If my BIDS directory has folders for sub-001 and sub-002, my GUID mapping file would look like this:

> 001 - LJFOIJWEL\
> 002 - LKJSFIJLW

Save this file (i.e. guids.txt) in the same folder as your BIDS directory, but not inside the BIDS directory.

### Step 5: (optional) Create NDA Experiment IDs and BIDS task name - to NDA Experiment ID mapping file

The NDA requires that every experiment be [defined](https://nda.nih.gov/nda/tutorials/data-submission?chapter=experiment-id), and when approved, it will be assigned an ID number. Each task that your participants complete will need its own approved experiment ID (including resting state). Once you have received your experiment ID(s), you will need to create another mapping text file - this one providing the mapping between the task names in your fMRI BIDS filenames (i.e. sub-001\_ses-01\_task-**checks**\_run-01\_bold.nii.gz) and your approved experiment ID numbers. For example, if my participants completed a "checks" task that was assigned an ID of 9990, and a "rest" resting state scan that was assigned an ID of 9991, my experiment ID mapping file would look like this:

> checks - 9990\
> rest - 9991

Save this file (i.e. expIDs.txt) in the same folder as your BIDS directory, but not inside the BIDS directory. If you don't provide this file in the BIDS2NDA conversion, the experiment\_id column in the output image03.csv file will be left blank and you will need to fill it in manually for any fMRI rows.

### Step 6: (optional) Create or copy a csv with additional data

Sometimes there is information that is missing or incorrect from the automatic BIDS conversion, that you may have available from another source. For example, the BIDS conversion approximates the interview\_age in months from the age in years in the BIDS data. This age needs to exactly match any other data uploaded for the same participant (i.e. ndar\_subject01.csv), so our bids2nda conversion tool allows you to specify a csv with additional data you would like to use to modify the image03.csv file.

Save this csv in the same folder as your BIDS directory, but not inside the BIDS directory.

***

## Installing BIDS2NDA and the NDA validator

To install in a [Python virtual environment on Oscar](https://docs.ccv.brown.edu/oscar/software/python-installs#using-python-enviroments-venv):

1. Change to your home directory\
   `cd ~`&#x20;
2. Create a new python environment called "bids2nda"\
   `python -m venv bids2nda`&#x20;
3. Activate the new environment\
   `source ~/bids2nda/bin/activate`&#x20;
4. Install our version of the BIDS to NDA conversion tool\
   `pip install https://github.com/brown-bnc/bids2nda/archive/master.zip`&#x20;
5. Install the [NDA validator](https://github.com/NDAR/nda-tools/tree/main) that will let us test whether the data is NDA-compliant\
   `pip install nda-tools`

***

## Running the BIDS to NDA conversion

1. First, make sure that you are in your bids2nda environment. It should say `(bids2nda)` in front of your terminal command prompt. If it does not, activate the environment with  \
   `source ~/bids2nda/bin/activate`
2. Change to your directory that contains your BIDS directory, GUID mapping file, and experiment ID mapping file.
3.  Make a new directory for your NDA-formatted data

    `mkdir nda_output`
4.  Launch the [BIDS to NDA converter](https://github.com/brown-bnc/bids2nda?tab=readme-ov-file#bids2nda)

    `bids2nda bids guids.txt nda_output -e expIDs.txt --lookup_csv ndar_subject01.csv --lookup_fields interview_age`\
    \
    The -e, --lookup\_csv, and --lookup\_fields are optional. In this example, we are grabbing the interview age in months from the ndar\_subject01.csv file and using it to fill in the interview\_age column in the image03.csv file.
5. If successful, you should see the message "Metadata extraction complete.", and the nda\_output folder should contain one image03.csv file and a series of .metadata.zip files. These zip files are referenced in the data\_file2 column of the image03.csv and will ultimately be uploaded with your data. \
   \
   They contain:&#x20;
   1. The BIDS json sidecars that go along with each of your NIFTIs
   2. the \_events.tsv behavioral files
   3. any stimulus files you supplied
   4. physio tsv and json files, if present in the BIDS directory

{% hint style="warning" %}
We are working on a fix, but for now the photomet\_interpret field of the image03.csv file will need to be filled in manually if you are converting any "enhanced" DICOM files (i.e. data collected post- scanner upgrade to XA30). The correct value is likely MONOCHROME2, but double-check your DICOM header for the **(0028,0004) | Photometric Interpretation** field to make sure this is true for your data.
{% endhint %}

***

## Validating the NDA-formatted data

To run the validator tool supplied by the NDA:

1. Change directory to your new NDA output folder\
   `cd nda_output`
2. Run the validator, passing in the new image03.csv file\
   `vtcmd image03.csv`
3. The tool will print information about whether or not your data passed validation. If it failed, open the validation report and address any identified issues.&#x20;

***

## Tips

1. Make sure your dataset is BIDS-valid. The conversion tool will attempt to add any files in your BIDS directory that follow the `sub-*.nii.gz`  pattern, so any extra files in your BIDS directory (from analyses, etc.) may cause errors.
2. If you are uploading data to the NDA in batches, you'll need to temporarily copy just the data for the current upload into a separate BIDS directory, so that the tool doesn't attempt to parse any previously uploaded data. When you do that, make sure to also copy over the participants.tsv file and edit it to only contain the participants for the current upload.
3. If you manually modify the participants.tsv file (in MATLAB especially), be careful that it retains its tab-delimited format. Otherwise, it will not be read in properly.
