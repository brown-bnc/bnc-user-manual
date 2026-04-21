---
description: How to use our custom webapp to upload your MRS data to XNAT
---

# Uploading raw spectroscopy data

When you collect MR spectroscopy data at the scanner and send your data to XNAT, the DICOM-formatted version gets automatically transferred along with the rest of your DICOMs.&#x20;

We have developed a simple webapp ([available on github](https://github.com/brown-bnc/XNAT-uploader-webapp)) that allows you to upload your raw spectroscopy data as well (.rda and .dat files), and it will automatically attach them to their matching DICOM(s). Then, when you run the [xnat2bids conversion](../../xnat-to-bids-intro/using-oscar/oscar-utility-script/), the raw spectroscopy data will be exported as well and placed in the sourcedata subdirectory of your BIDS directory.

{% hint style="warning" %}
Contact us at cobre-bnc@brown.edu if you would like to upload raw spectroscopy data to your project on XNAT. There is a one-time setup step we'll need to do for you first.
{% endhint %}

#### Follow these steps to get your raw MRS data to XNAT

1. When your scan is complete, [transfer all your data to XNAT](./) as usual, and then [send your .rda and .dat files to scannershare](../../mrf-guides/exporting-data-via-scannershare.md).
2. **On the transfer computer in the MRF waiting room**, log in to XNAT and verify that your new data has appeared in your project (this usually takes \~10 mins from the time the data was sent from the scanner, but it depends on the size of your dataset).
3. Once your DICOMs are on XNAT, launch the XNAT Spectroscopy Uploader from the desktop.

<figure><img src="../../.gitbook/assets/desktop (1).png" alt="XNAT spectroscopy uploader icon on the desktop of the transfer Mac. Icon has a blue-green gradient with a white spectroscopy trace and an arrow pointing up, with the text &#x22;XNAT Spectro Uploader&#x22;" width="80"><figcaption></figcaption></figure>

4. The uploader login page will open in a new Chrome window. Enter your XNAT login credentials and click Log In.

<figure><img src="../../.gitbook/assets/login.png" alt="Login page for the spectroscopy uploader. &#x22;Quit&#x22; button in upper right corner, with fields for &#x22;Username&#x22; and &#x22;Password&#x22; below. Blue Log In button below that." width="375"><figcaption></figcaption></figure>

5. After successful authentication, you'll see the uploader. Click the "Select .rda and/or .dat files" button to choose the raw data files you'd like to upload.

<figure><img src="../../.gitbook/assets/uploader.png" alt="Spectroscopy uploader without any data loaded. A &#x22;Select .rda and/or .dat files&#x22; button at the top says &#x22;No files loaded&#x22;. Below is a tip &#x22;RDA file headers are used to automatically determine Project, Subject, Session &#x26; Scan. TWIX (.dat) files inherit this information only when matching is unambiguous. If this fails, you will need to manually enter it prior to uploading.&#x22; Below is an empty table with column headers &#x22;Filename&#x22;, &#x22;Scan ID&#x22;, &#x22;Series Description&#x22;, &#x22;Project&#x22;, &#x22;Subject&#x22;, &#x22;Session&#x22;, &#x22;Remove&#x22;, &#x22;Upload Error&#x22;. At the bottom are &#x22;Preview XNAT Session(s)&#x22; and &#x22;Upload&#x22; buttons"><figcaption><p>Raw spectroscopy data XNAT uploader without any data loaded</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/fileselect.png" alt="Mac file selection dialogue, showing selection of 4 files from the &#x22;scannershare&#x22; drive, two .dat and two .rdas"><figcaption><p>Selecting raw .dat and .rda files from scannershare</p></figcaption></figure>

6. Your selected files will populate the table. RDA files contain all the information needed to determine where they belong on XNAT, but .dat files do not. If you upload your .rda and .dat files together, the uploader will try to match .dat files with their respective .rda(s) and, if successful, the .dat will inherit the same metadata. If necessary, you can fill in any missing information manually, or correct anything that is incorrect (i.e. your scan was mistakenly registered as a different study during scanning, so you need to correct the project name). If you want to double-check where your data will land, you can click the "Preview on XNAT" button.

<figure><img src="../../.gitbook/assets/loaded_data.png" alt="Raw data uploader with the two rda and two dat files now listed in the table, with &#x22;Scan ID&#x22;, &#x22;Series Description&#x22;, &#x22;Project&#x22;, &#x22;Subject&#x22;, and &#x22;Session&#x22; determined automatically. Red Xs are visible in the &#x22;remove&#x22; column."><figcaption><p>Raw data ready for upload, with metadata automatically determined from the files</p></figcaption></figure>

7. When you are satisfied that everything looks correct, click "Upload".

<figure><img src="../../.gitbook/assets/uploading.png" alt="View of the uploading screen, with a spinner and &#x22;Uploading...&#x22; in the center"><figcaption></figcaption></figure>

8. If successful, you will see the message "Upload complete: X file(s) uploaded", and XNAT will open in a new Chrome tab. Here, you can check that your raw data files have ended up where you expect. If you hover over the rightmost column, you can see that two raw data files were attached to our `mrs-mrsref_acq-PRESS_voi-Lacc` DICOM in an `MRS` folder (the DICOM is in a `secondary` folder).\
   \
   If you want to view the names of the files attached to each DICOM, you can click "Manage Files" in the Actions section at the top of the page.

<figure><img src="../../.gitbook/assets/mrs_folder.png" alt="View of the two spectroscopy DICOMs in XNAT, with a yellow box on the right that says MRS: 121.6MB in 2 files"><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screenshot 2026-04-21 at 12.22.57 PM.png" alt="XNAT actions menu on the left, with the File Manager view on the right. Series 16 - 24 are listed, with the MRS folder of series 24 expanded to show the two uploaded raw MRS files"><figcaption></figcaption></figure>

9. If your upload encounters errors (maybe you incorrectly changed the project name), you can hover over the "upload failed" message for more details, correct the metadata in the table, and click `Upload` to try again.

<figure><img src="../../.gitbook/assets/Screenshot 2026-04-21 at 12.51.32 PM.png" alt="View of the spectroscopy upload table with &#x22;upload failed&#x22; for each of the four data files. The message &#x22;XNAT could not find the specified project/subject/session scan. Please check the values in the table and try again.&#x22; is visible."><figcaption></figcaption></figure>

10. Click `Quit` when you are done.
