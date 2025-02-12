# Multi-session spectroscopy with voxalign

We have developed a python package that takes in spectroscopy DICOM(s) and a T1 anatomical scan from a first MR session, and a T1 from an in-progress MR session, and provides the prescription to enter on the console to match the exact spectroscopy position and orientation from the first session.

Voxalign is available on github at [https://github.com/brown-bnc/voxalign](https://github.com/brown-bnc/voxalign) (currently set to private - contact Elizabeth for access)

### Use voxalign on Tess (mac mini behind scanner operator) \<RECOMMENDED>

\*Make sure you log in as mrfuser\*

A voxalign environment is already created, so all you have to do is open a terminal window and type \
`source ~/Desktop/voxalign/bin/activate`

### Set up on your own computer:

I recommend installing in a python virtual environment:

1. create an environment named voxalign: `python3 -m venv voxalign`
2. activate it: `source /path/to/env/voxalign/bin/activate`
3. install voxalign: \
   `pip install` [`https://github.com/brown-bnc/voxalign/archive/master.zip`](https://github.com/brown-bnc/voxalign/archive/master.zip)

You'll also need to [install FSL](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/install/index) on your computer.

### Prepare in advance

You can organize your data however you like, but it is helpful to collect the session 1 DICOMs in advance of the scan session and make sure that they are named and organized in a way that will make running voxalign quick and simple. For example, I like to make a new folder for each participant, with  sess1 and sess2 subdirectories. You can put the T1 and spectroscopy DICOMs in the sess1 directory in advance, and the sess2 directory you'll copy the T1 DICOM into as soon as it is collected.

<figure><img src="../.gitbook/assets/Screenshot 2024-11-22 at 9.10.45 PM.png" alt="" width="281"><figcaption></figcaption></figure>

### Running voxalign

1. After activating the virtual environment (it should say (voxalign) before the command prompt), you can start voxalign by typing `run-voxalign`
2. Use the voxalign file selector to select your output directory. I usually just create a folder called "output" in the participant's directory.&#x20;
3. Select your T1 and spectroscopy DICOMs. You can set up everything but the session 2 T1, which will arrive via scannershare.

<figure><img src="../.gitbook/assets/Screenshot 2024-11-22 at 9.22.03 PM.png" alt="" width="563"><figcaption></figcaption></figure>

5. Once the session 2 T1 has been collected, [export it to scannershare](../mrf-guides/exporting-data-via-scannershare.md) and copy it to your participant/sess2 folder on Tess. Then select it in the voxalign GUI.
6. Click **Run VoxAlign**

**Your new spectroscopy voxel prescriptions will be printed to the terminal like this, and also automatically opened in a fsleyes window.**&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2024-11-22 at 9.28.07 PM.png" alt="" width="563"><figcaption></figcaption></figure>

***

#### TIPS

* Your two T1 scans need to have the same resolution for voxalign to work properly (at the moment).
* When you are typing your prescription in on the scanner, if the field says 'R' enter a negative number to switch it to L, and vice versa. This applies to all three directions.
