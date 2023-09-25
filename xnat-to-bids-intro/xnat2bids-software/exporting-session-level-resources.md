# Exporting Session Level Resources 🆕

The `xnat2bids` pipeline now supports exporting EEG resource data as well as converting that data into the BIDS standard format.  To upload your EEG data onto XNAT, see the instruction steps in the second section below.  Once your resource data have been successfully uploaded, you can run `xnat2bids` by the methods specified in our [documentation](https://brown-bnc.github.io/xnat-tools/), or [here](../using-oscar/oscar-utility-script.md) if you're exporting your data onto Oscar.

### Naming Convention: How to Label Your EEG Data (TBD!)

We are currently designing the best protocol strategies for naming EEG data.  For now, we encourage you to label your data as you see fit! &#x20;

### Uploading EEG Data to XNAT&#x20;

1. Open the session page of the experiment where you would like to append EEG resource data.
2. Select "Manage Files" from the Actions Panel.
3. Select "Add Folder", then create a folder named "eeg" at level "resources."
4. Select "Upload Files."  Add each file, one by one, to your new folder.&#x20;
5. Finally, select "Upload." Repeat for every EEG file associated with the session.



<figure><img src="../../.gitbook/assets/Screenshot 2023-09-25 at 4.34.24 PM.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screenshot 2023-09-25 at 4.38.07 PM.png" alt=""><figcaption></figcaption></figure>





###

