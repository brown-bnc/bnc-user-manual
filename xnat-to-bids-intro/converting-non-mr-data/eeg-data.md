# EEG data

The `xnat2bids` pipeline supports exporting EEG data from XNAT and converting it into the BIDS standard format, using tools from the[ MNE-BIDS python package](https://mne.tools/mne-bids/stable/index.html).&#x20;

To upload your EEG data onto XNAT, see the instruction steps below, which differ slightly depending on whether you are uploading concurrent EEG-fMRI data or stand-alone EEG data. Once your data have been successfully uploaded, you can run `xnat2bids` by the methods specified in our [xnat-tools documentation](https://brown-bnc.github.io/xnat-tools/), or in [the Oscar Utility Script](../using-oscar/oscar-utility-script/) if you're exporting your data onto Oscar.

On this page, learn:

[How to name your EEG data files for automatic BIDS conversion](eeg-data.md#naming-convention-how-to-name-your-eeg-data-files)

[How to upload and convert concurrent EEG-fMRI data](eeg-data.md#uploading-eeg-data-to-an-mr-session)

[How to upload and convert stand-alone EEG data](eeg-data.md#uploading-stand-alone-eeg-data)

***

### Naming Convention: How to Name Your EEG Data Files

[The BIDS format](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/03-electroencephalography.html) requires/allows specific information to be saved in data filenames. Specifically, "BIDS entities" are saved as key-value pairs (i.e. "sub-101") separated by underscores. For example, the filename "sub-101\_ses-01\_task-checks\_run-01" contains keys and associated values for subject, session, task, and run. For our automatic XNAT to BIDS conversion to appropriately include these pieces of information in the BIDS-format filenames, the EEG data you upload to XNAT should include all relevant key-value pairs in the filename, separated by underscores. "Subject" and "session" information will be gathered from XNAT, and you can use any of the following keys to provide additional information:

**task** - the experimental task **\[required]** (any string you want, excluding spaces or punctuation)

**acq** - the acquisition parameters (any string you want, excluding spaces or punctuation)

**run** - run number (integer)

**proc** - processing label (any string you want, excluding spaces or punctuation)

**rec** - recording name (any string you want, excluding spaces or punctuation)

**space** - coordinate space for anatomical and sensor location files (e.g., `*_electrodes.tsv`, `*_markers.mrk`) (valid values for `space` must come from a list of BIDS keywords [described in the BIDS specification](https://bids-specification.readthedocs.io/en/stable/appendices/coordinate-systems.html#eeg-specific-coordinate-systems))

**split** - split of the continuous recording file for `.fif` data (integer)

**desc** - description; provide additional information for derivative data (any string you want, excluding spaces or punctuation)



**For example, this EEG data uploaded to XNAT...**

<figure><img src="../../.gitbook/assets/Screenshot 2023-10-16 at 4.21.06 PM.png" alt="The XNAT portal shows EEG data saved in an EEG directory that is not structured or named according to BIDS formatting. "><figcaption></figcaption></figure>

**... will be converted to BIDS format like this:**

<figure><img src="../../.gitbook/assets/image (32).png" alt="This directory shows how ECG data is organized and named when it is following BIDS formatting. "><figcaption></figcaption></figure>

***

### Uploading concurrent EEG-fMRI data

#### One-time XNAT project configuration

For EEG data collected concurrently with fMRI data, we recommend following these setup steps to configure an EEG resource uploader for your XNAT project. These steps should be able to be completed by anyone with an "owner" status on your XNAT project, but please reach out if you would like BNC staff to set it up for you or walk you through it.

1. Open the "Manage" tab on your Project home page, and go to "Project Resource Settings"
2. Click "Start" to open a configuration page.
3. Select "Image Sessions" as the context for your resource uploader.
4. Select the MR Session data-type.
5. Set the "Resource Folder" name to be "eeg"
6. Add the resource uploader to your project

<figure><img src="../../.gitbook/assets/Screenshot 2023-10-05 at 2.34.00 PM.png" alt="Customizing the &#x22;Project Resource Settings&#x22; on XNAT for simultaneous EEG+MRI. Under the prompt: &#x22;Select data-type&#x22;, choose &#x22;MR Session&#x22;. Next to &#x22;Resource Folder&#x22;, type &#x22;eeg&#x22;. Then press &#x22;Add&#x22;. "><figcaption><p>Configuring an EEG resource uploader for concurrent EEG-fMRI data</p></figcaption></figure>

#### Uploading EEG data to an MR Session

Then, when you complete an EEG-fMRI session, first follow the usual procedure to [transfer your MR data from the scanner to XNAT](../../xnat/uploading-data.md). Once your data has appeared on XNAT (typically within an hour), you can navigate to the MR Session that was just created, and click "Upload Additional Files" to upload the associated EEG data:

<figure><img src="../../.gitbook/assets/add_EEG_to_MR_data.jpg" alt="To upload ECG data to a session on the XNAT portal, press &#x22;Upload Additional Files&#x22; under the Actions panel. " width="563"><figcaption><p>Add EEG data to an MR Session</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screenshot 2023-10-05 at 2.40.32 PM.png" alt="In the &#x22;Upload Additional Files&#x22; pop up, select your EEG files and press &#x22;Process Uploaded Data&#x22;. " width="563"><figcaption><p>Upload EEG data (.eeg, .vmrk, .vhrd, etc.)</p></figcaption></figure>

***

### Uploading stand-alone EEG data

#### One-time XNAT project configuration

If you only intend to upload EEG data, or if your EEG data was collected in a separate session(s) from any MRI data, we recommend storing your data in an "EEG Session", just as XNAT stores data transferred from the scanner in an "MR Session". You will need to complete these one-time setup steps to enable the creation of EEG Sessions for your XNAT project:

These steps should be able to be completed by anyone with an "owner" status on your XNAT project, but please reach out if you would like BNC staff to set it up for you or walk you through it.

1. Open the "Manage" tab on your Project home page, and go to "Project Resource Settings"
2. Click "Start" to open a configuration page.
3. Select "Image Sessions" as the context for your resource uploader.
4. Select the EEG Session data-type.
5. Set the "Resource Folder" name to be "eeg"
6. Add the resource uploader to your project

<figure><img src="../../.gitbook/assets/Screenshot 2023-10-05 at 2.34.49 PM.png" alt="When configuring an XNAT project to accept standalone EEG data, ensure that &#x22;Select data-type&#x22; is set to EEG Sessions (under &#x22;Project Resource Settings&#x22; -> &#x22;Image Sessions&#x22;). "><figcaption><p>Configuring an EEG resource uploader for your XNAT project</p></figcaption></figure>

#### Creating a new EEG Session and uploading data

After navigating to your project on XNAT, click Add -> EEG Session

<figure><img src="../../.gitbook/assets/Screenshot 2023-10-05 at 3.05.10 PM.png" alt="To add a new EEG session to a pre-existing XNAT project, select &#x22;EEG Session&#x22; under the &#x22;Add&#x22; dropdown menu. "><figcaption><p>Add a new EEG Session</p></figcaption></figure>

Then, if this subject already exists (usually because they've completed a previous session), you can select them from the dropdown menu; otherwise, click Add New Subject. If you are adding a new subject, the only field you need to fill in in the popup window is "Subject's ID within this project", and click "Submit".

<figure><img src="../../.gitbook/assets/Screenshot 2023-10-05 at 3.11.42 PM.png" alt="The &#x22;EEG Session&#x22; pop-up window gives XNAT users the ability to create a new EEG session for a specified subject. " width="269"><figcaption><p>Creating an EEG Session</p></figcaption></figure>

If this is a single-session experiment (just this one EEG session), you can put the same subject ID in the "Session" field. **IMPORTANT: If this is a multi-session study (multiple EEG sessions, or a mix of EEG and MR), you should name the session&#x20;**_**subject ID**_**&#x20;\*underscore\*&#x20;**_**session label**_**.** This session label is what will be used to label your sessions in the BIDS file structure. You could do "EEGDEMO\_01", "EEGDEMO\_02", etc., or something that describes the different phases of your study, like "EEGDEMO\_pretrainingEEG", "EEGDEMO\_trainingMR", "EEGDEMO\_posttrainingEEG".

Fill in the date, click the trashcan icons to delete the auto-populated list of scan fields, and click "Submit".

Finally, navigate to your newly created EEG session and upload the EEG data:

<figure><img src="../../.gitbook/assets/Add_EEG_data_to_EEGSession.jpg" alt="Once an EEG session is created on XNAT, you can add data to it by pressing the &#x22;Upload Additional Files&#x22; button. " width="563"><figcaption><p>Upload EEG data to an EEG Session</p></figcaption></figure>
