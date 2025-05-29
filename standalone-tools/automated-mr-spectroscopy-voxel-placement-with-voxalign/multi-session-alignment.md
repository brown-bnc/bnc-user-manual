---
description: >-
  For exact replication of voxel placement(s) within a single participant across
  multiple scan sessions
---

# Multi-session alignment

### Prepare in advance

You can organize your data however you like, but it is helpful to collect the session 1 DICOMs in advance of the scan session and make sure that they are named and organized in a way that will make running voxalign quick and simple. For example, I like to make a new folder for each participant, with sess1 and sess2 subdirectories. You can put the T1 and spectroscopy DICOMs in the sess1 directory in advance, and the sess2 directory you'll copy the T1 DICOM into as soon as it is collected.

<figure><img src="../../.gitbook/assets/Screenshot 2024-11-22 at 9.10.45 PM.png" alt="" width="281"><figcaption><p>A simple and clear way to organize your DICOMs</p></figcaption></figure>

### Running voxalign

1. Activate the virtual environment with `source /path/to/env/voxalign/bin/activate` (on Tess, this will be `source ~/Desktop/voxalign/bin/activate`. You can tell that the environment is activated when it says `(voxalign)` before the command prompt.&#x20;
2. Start voxalign by typing `run-voxalign`.
3. Use the voxalign file selector to select your output directory. I usually just create a folder called "output" in the participant's directory.&#x20;
4. Select your T1 and spectroscopy DICOMs. You can set up everything but the session 2 T1, which will arrive via scannershare.

<figure><img src="../../.gitbook/assets/Screenshot 2024-11-22 at 9.22.03 PM.png" alt="" width="563"><figcaption></figcaption></figure>

5. Once the session 2 T1 has been collected, [export it to scannershare](../../mrf-guides/exporting-data-via-scannershare.md) and copy it to your participant/sess2 folder on Tess. Then select it in the voxalign GUI.
6. Click **Run VoxAlign**

**Your new spectroscopy voxel prescriptions will be printed to the terminal, saved out in a text file, and also automatically opened in a fsleyes window.**&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2024-11-22 at 9.28.07 PM.png" alt="" width="563"><figcaption></figcaption></figure>

***

#### TIPS

* Your two T1 scans need to have the same resolution for voxalign to work properly (at the moment).
* When you are typing your prescription in on the scanner, if the field says 'R' enter a negative number to switch it to L, and vice versa. This applies to all three directions.
* The tools voxalign uses to convert DICOMs to NIFTIs do not play well with spaces in file paths, so - for example - running voxalign on data stored in a "Google Drive" folder will not work.
