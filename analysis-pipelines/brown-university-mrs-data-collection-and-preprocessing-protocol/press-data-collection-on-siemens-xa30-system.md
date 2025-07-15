# PRESS Data Collection on Siemens XA30 System

### Placing the Reference and Metabolite Voxels

* After collecting your anatomical scan (MPRAGE), drag the small gray head icon from the scan to the viewing windows. All three planes should show up automatically. If not, go to the MR View & GO tab and drag over the axial and coronal images.

<figure><img src="../../.gitbook/assets/image (33).png" alt=""><figcaption><p>Drag the MPRAGE into the left viewing window. Watch to see if the middle and right windows autofill with the reconstructed axial and coronal MPRAGE images. </p></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (34).png" alt=""><figcaption><p>If the axial and coronal reconstructions do not autofill, go to the MR View &#x26; Go tab and find the images on the right panel. Drag the coronal reconstruction from the right panel up to the Patient Window (the other available tab). That tab should open and you can then drag the run to the middle viewing window. Repeat those steps to drag the axial (Tra) reconstruction to the right window. </p></figcaption></figure>

* Drag over the water reference scan to be executed by the scanner and open the sequence.
* A red dot will appear on your sagittal image. This dot is NOT your voxel. It is used to convert the images to non-distortion-corrected images. On the sagittal image, place the dot in the general area your voxel will be. Then click “Convert images.”

<figure><img src="../../.gitbook/assets/image (35).png" alt=""><figcaption><p>In this example, we placed the voxel in the ACC. Because of that, we placed the red dot in the same area, then selected "Convert Images" </p></figcaption></figure>

{% hint style="info" %}
Tips on voxel placement:&#x20;

* Unlike the previous versions of Siemen's console software, XA30 does not have a "scroll nearest" function. It simultaneously updates the position in the other two planes as you move it in one plane.
* The dotted lines on your voxel mean it is not in view.
* You will need to manually move the crosshairs on the screen to ensure your voxel is placed correctly. To see the crosshairs, press the “H” key.
* You can scroll through your slices by right clicking the mouse and scrolling up and down.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (36).png" alt=""><figcaption><p>Voxel placement in the ACC. The red box highlights the routine tab (where to find the parameters)</p></figcaption></figure>

* Once you are satisfied with the placement, click the orange “Go” button.
* The full width half maximum (FWHM) measurement will pop up after the scanner shims. The goal is to have a FWHM measurement <20.&#x20;

<figure><img src="../../.gitbook/assets/image (37).png" alt=""><figcaption><p>The FWHM can be found in the upper right of the pop up window, depicted here in the red box. Since the FWHM is below 20, the window can be closed by hitting "Continue"</p></figcaption></figure>

<details>

<summary>How to manually adjust the FWHM if it is higher than 20</summary>

* If you are unhappy with the FWHM value (>20) during your water reference scan, you can manually adjust it by clicking “cancel” rather than “continue” on the pop-up screen.

<figure><img src="../../.gitbook/assets/image (40).png" alt=""><figcaption><p>A high FWHM, measured here at 22.1. Rather than clicking 'Continue", select "Cancel" and complete the following steps. </p></figcaption></figure>

* Double click the water reference sequence to open it and go into the “Details View” tab.
* Click “System”, “Adjustments", and then click “Manual Adjustments”.

<figure><img src="../../.gitbook/assets/image (41).png" alt=""><figcaption></figcaption></figure>

* Go to the left hand side and click “Interactive Shim” then follow the same process as the one used on the prior version of the scanner.
  * For this system, A11 is X, B11 is Y, and A10 is Z. When you have adjusted the system to a FWHM you like, click “Stop”, "Load Best", and then “Apply.”
  * It is important to remember that the FWHM number presented on the screen won’t update after you do this step, so be sure to write it down once you get your value.

<figure><img src="../../.gitbook/assets/image (42).png" alt=""><figcaption><p>The Interactive Shim Page</p></figcaption></figure>

</details>

* Next, drag over the metabolite scan to be executed by the scanner and open the sequence. While the metabolite scan is open, right click on the water reference scan and select “copy parameters”, then “measurement parameters”, and then “apply.” Now, your voxel should be in the same position as that of the reference scan. Press the orange “Go” button to initiate the sequence.

<figure><img src="../../.gitbook/assets/image (38).png" alt=""><figcaption></figcaption></figure>

* Drag and drop over the “Auto Start MR Spectro” sequence after collecting your metabolite data. Be sure to press the “Go” button. This step is necessary for extracting your RDA files! Only do it after ALL spectroscopy sequences are run.

<figure><img src="../../.gitbook/assets/image (39).png" alt=""><figcaption><p>Running "Auto Start MR Spectro" is a necessary step to create RDA files. Run this sequence at the end of your MRS acquisition.</p></figcaption></figure>

### Exporting the Data (RDA and twix files)

* To export the RDA files, go into the files tab and select both the water reference file and metabolite file. Right click on them and select the “MR Spectro” option.

{% hint style="info" %}
If you are having issues exporting the data in MR Spectro, try reopening it by first selecting "View as Read-Only with".
{% endhint %}

<figure><img src="../../.gitbook/assets/image (43).png" alt=""><figcaption></figcaption></figure>

* Go under the MR Spectro Analysis gray box on the left hand side of the screen and click “Export Selected Raw” and click “Export All.”
* Select your drive ([scannershare](../../mrf-guides/exporting-data-via-scannershare.md)) and both files will be saved there.
  * You can no longer name the RDA files. They will be manually named by the MRI console and can be identified by both timestamp and sequence number.

<figure><img src="../../.gitbook/assets/image (44).png" alt=""><figcaption></figcaption></figure>

* To export the twix files, you need to be in Med Admin mode. Click Med Admin in the upper righthand corner and enter in the username and password.
* Now, press the “Windows” key on the keyboard for the start menu. If the Windows key doesn’t work, press “tab,” “delete,” and "\[->".
* Go to the command prompt option on the start menu and type in “twix”.

<figure><img src="../../.gitbook/assets/image (45).png" alt=""><figcaption><p>This terminal can be found by pressing the Windows key, and selecting "Command Prompt". The twix command will open a popup and allow you to select your files. </p></figcaption></figure>

* A window should pop up. Select your water reference and metabolite files and export them to [scannershare](../../mrf-guides/exporting-data-via-scannershare.md) by right clicking and selecting "Copy total raid file".&#x20;
* IMPORTANT: XNAT does NOT transfer your RDA or twix files! You need to manually put them on an external drive and upload them to Oscar.

<figure><img src="../../.gitbook/assets/image (46).png" alt=""><figcaption><p>Select the files, right click, and export to drive via "Copy total raid file". </p></figcaption></figure>
