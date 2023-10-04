# Exporting Session Level Resources 🆕

The `xnat2bids` pipeline now supports exporting EEG resource data as well as converting that data into the BIDS standard format.  To upload your EEG data onto XNAT, see the instruction steps in the second section below.  Once your resource data have been successfully uploaded, you can run `xnat2bids` by the methods specified in our [documentation](https://brown-bnc.github.io/xnat-tools/), or [here](../using-oscar/oscar-utility-script.md) if you're exporting your data onto Oscar.

If you only intend to upload EEG data, we recommend storing your data in an EEG Session.

### Naming Convention: How to Label Your EEG Data (TBD!)

We are currently designing the best protocol strategies for naming EEG data.  For now, we encourage you to label your data as you see fit! &#x20;

### Create a Custom Resource Uploader For Image Session

1. Open the "Manage" tab on your Project home page, and go to "Project Resource Settings"
2. Click "Start" to open a configuration console.
3. Select "Image Sessions" as the context for your resource uploader.
4. Select data-type dropdown for the session type you prefer (MR / EEG).
5. Set the "Resource Folder" name to be "eeg"
6. Add the resource uploader to your project

<figure><img src="../../.gitbook/assets/Screenshot 2023-09-29 at 2.22.10 PM.png" alt=""><figcaption></figcaption></figure>

You should now be able to utilize the resource uploader at the session level for all sessions in your project of the data-type specified.  On the session page, "Upload Additional Files" will be available to use from the Actions Panel.



<figure><img src="../../.gitbook/assets/Screenshot 2023-10-04 at 8.09.00 AM.png" alt=""><figcaption></figcaption></figure>









###

