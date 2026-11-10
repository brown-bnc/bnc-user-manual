# Calculating SNR and TSNR using AFNI

The Signal-to-Noise Ratio of an MRI scan offers important information on data quality and signal strength. Researchers often measure it with the goal of assessing quality of the hardware (the MRI itself, head coils, etc). It is also helpful when optimizing MRI sequences. In its simplest definition, the SNR tells you how much of your raw MRI signal can be attributed to the brain versus other sources of variability (e.g, thermal noise). Higher SNR values indicate higher sensitivity to the desired signal. You can calculate SNR on a single frame such as an anatomical scan, and you can also calculate it over time for fMRI scans.&#x20;

A common metaphor for SNR is the sound of a busy party. If you imagine that you are speaking to your friend, you'll notice that you do not only hear your friend's voice- you also hear other people, music, footsteps, glassware, doors opening, and much more. In this example, your friend's voice is the signal that you wish to separate from the noise. If you took a recording of the sound of the party, there are processing methods you could use to separate the various sources of sound. However, it is also ideal to make recording itself as high quality as possible. This is done by neuroimagers by fine-tuning the MRI sequence so that it it is more sensitive to signal that you are interested in. For anatomical T1-weighted MRI, the sequence is optimized to be sensitive to brain matter. In a functional MRI (fMRI), it is sensitive to the BOLD response.&#x20;

## SNR

As previously defined, SNR is a number that describes the ratio of structured signal to random noise. In T1-weighted anatomical MRI, spatial SNR is calculated with this equation:

<figure><img src="../.gitbook/assets/Screenshot 2026-03-11 at 1.43.40 PM.png" alt="The equation for SNR is the mean of the brain tissue signal, divided by the standard deviation of the background signal. "><figcaption></figcaption></figure>

Here we provide a bash script to measure SNR using AFNI commands:

```bash
fname= <insert T1w file name here>

echo "Calculating SNR for anatomical scan: $fname"

# Create an eroded mask of the brain (signal)
3dAutomask -q -erode 4 -clfrac 0.1 -prefix snr.$fname.obj.nii $fname.nii

# Create a dilated mask of the brain (used to make a background mask)
3dAutomask -q -dilate 4 -clfrac 0.1 -prefix snr.$fname.objplus.nii $fname.nii

# Create a mask of the background of the image (noise)
3dcalc -a snr.$fname.objplus.nii -expr "abs(a-1)" -prefix snr.$fname.bkgnd.nii

# Calculate the mean of the brain signal
signal=$(3dmaskave -mask snr.$fname.obj.nii -quiet $fname.nii)
# Calculate the standard deviation of the background
noise=$(3dmaskave -mask snr.$fname.bkgnd.nii -sigma -quiet $fname.nii | awk '{print $2}')
# Calculate SNR
snr=$(echo "scale=2; $signal / $noise" | bc)

echo "$fname snr = $snr"
```

If you run this script on Demodat2 subject 101 session 1, scan `sub-101_ses-01_acq-memprageRMS_T1w.nii`, this text prints at the very end of processing:

```console
+++ 6736247 voxels survive the mask
sub-101_ses-01_acq-memprageRMS_T1w snr = 96.97
```

If you then use the AFNI GUI to overlay the signal mask (\*.obj.nii) and the noise mask (\*.bkgd.nii) on top of the anatomical scan, they will look like this:&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2026-03-11 at 4.50.55 PM.png" alt="On the left: A midsagittal slice of the T1 anatomical scan, with the “signal” mask overlaid in red. The signal mask covers the brain as well as the head, with a slightly eroded perimeter. On the right: The same T1 anatomical scan with the “noise” mask overlaid in red. This mask covers all the background around the head, with a slight buffer so as not to touch the border of the head and background. "><figcaption><p>A single slice/frame from the T1w anatomical scan of Demodat2 subject 101 session 01. The left image shows the mask used to measure the signal in the SNR equation. The right image shows the mask used to measure the background/noise. </p></figcaption></figure>

You will notice that the mask used to measure signal does not cover just the brain: it also includes sinuses, CSF, bone, and muscle. It is also common to measure signal using a brain/ROI mask, and then measure the background by masking one or multiple ROIs away from the head. There is no one universal method to calculate SNR, and the resources at the end of this tutorial offer various methods.&#x20;

## TSNR

The Temporal Signal-to-Noise Ratio, or TSNR, is very similar to SNR except that the values are measured across time (in a multi-frame 3D+Time dataset). This means that the TSNR value for each voxel is the mean signal intensity over time, divided by the standard deviation of that voxel's time course.&#x20;

With AFNI, you can calculate TSNR using a single command! However, in order to capture the TSNR of just the brain, we additionally create a brain mask and then take the average of all TSNR values within that mask. You could also use a ROI mask to measure the TSNR of a specific brain area.&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2026-03-11 at 3.24.08 PM.png" alt="The equation for TSNR is the mean of the brain tissue signal across time, divided by the standard deviation of the background signal across time. "><figcaption></figcaption></figure>

Here is a simple script to calculate TSNR:

```bash
fname= <insert fMRI file name here>

echo "Calculating whole brain TSNR for functional scan: $fname"

# Calculate TSNR
3dTstat -tsnr -prefix tsnr.$fname.nii $fname.nii

# Extract TSNR values from a whole brain mask
3dAutomask -prefix tsnr.$fname.obj.nii tsnr.$fname.nii
tsnr=$(3dmaskave -mask tsnr.$fname.obj.nii -quiet tsnr.$fname.nii)
echo "$fname tsnr = $tsnr"

```

If you run this script on Demodat2 subject 101, session 1, scan `sub-101_ses-01_task-resting_run-01_bold.nii`, this text prints at the very end of processing:

```console
+++ 80151 voxels survive the mask
sub-101_ses-01_task-resting_run-01_bold tsnr = 56.82
```

Open these files in the AFNI GUI to see how the resting state scan is transformed from a 3D+Time fMRI scan, to a single frame TSNR map. Additionally, you can overlay any masks used to extract TSNR values.&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2026-03-12 at 10.15.59 AM.png" alt="From right to left: A single slice/frame from the resting state scan of Demodat2 subject 101 session 01; That same slice after calculating TSNR; The TSNR map with the brain mask overlaid."><figcaption><p>From right to left: A single slice/frame from the resting state scan of Demodat2 subject 101 session 01; That same slice after calculating TSNR; The TSNR map with the brain mask overlaid. </p></figcaption></figure>

Both the SNR and TSNR scripts can be run individually, or they can be adapted to loop through multiple subjects/scans and print the values to a summary file.&#x20;

## Additional background on SNR and TSNR:

[The mriquestions.com section titled: "MR Quality Control: SNR"](https://mriquestions.com/signal-to-noise.html)

[MRI Master's webpage offering a detailed description of factors that influence SNR](https://mrimaster.com/snr/)

[Newbi 4 fMRI's tutorial/walkthrough of SNR calculations ](https://www.newbi4fmri.com/mini-tutorial-signal-to-noise)
