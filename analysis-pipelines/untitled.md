---
description: >-
  DSI studio is a tractography software tool that maps white matter tracts using
  diffusion weighted images. This tutorial will guide you in using DSI Studio to
  perform whole brain tractography analysis.
---

# Tractography: DSI Studio

## Using DSI Studio on Your Local Machine:

Download [DSI Studio](http://dsi-studio.labsolver.org/dsi-studio-download) to your local machine and open the program.&#x20;

## Using DSI Studio on Oscar:&#x20;

Copy this text into a terminal on Oscar Open Demand to load DSI Studio:

`module load dsi-studio`

Then enter this text to open the DSI GUI as a singularity container, bound to `/oscar/data`:&#x20;

`singularity exec -B /oscar/data /oscar/runtime/opt/dsi/chen-march2023/dsistudio_chen-2023-03-07.sif dsi_studio`



{% hint style="info" %}
<mark style="color:blue;">`singularity exec`</mark> executes dsi-studio as a singularity.<mark style="color:blue;">`-B /oscar/data`</mark> binds the singularity to oscar. <mark style="color:blue;">`/oscar/runtime/opt/dsi/chen-march2023/dsistudio_chen-2023-03-07.sif dsi_studio`</mark> is where the DSI singularity is located on oscar.&#x20;
{% endhint %}

## Perform Whole Brain Tractography:&#x20;

Select “_Step T1: Open Source Images_” to load diffusion MR images and create a SRC file. It is recommended to use diffusion images that have already been corrected for motion and susceptibility distortion (for example, via FSL TOPUP and Eddy).&#x20;

![Select Step T1 to open a diffusion image of your choice. ](<../.gitbook/assets/Screen Shot 2024-02-21 at 2.04.40 PM.png>)

If there are existing .bvec and .bval files in the same directory you entered the diffusion images from, a b-table will be generated automatically. Otherwise, you may manually create a b-table by loading the files into the pop up window via the file tab in the top left corner. Once that is saved, the SRC file will be created and stored in the main window.&#x20;

<figure><img src="../.gitbook/assets/Screen Shot 2024-02-21 at 2.06.14 PM.png" alt=""><figcaption><p>To manually create a b-table, enter the file tab, manually select the bval and bvec files, and hit OK. This will save the b-table as part of the SRC file. </p></figcaption></figure>

Select "_Step T2: Reconstruction_" and choose the SRC file. This step converts the SRC file into an FIB file, which will be used for fiber reconstruction.&#x20;

![Select Step T2 to use the SRC to begin reconstruction of the white matter tracts. ](<../.gitbook/assets/Screen Shot 2024-02-21 at 2.16.14 PM.png>)



A new window will appear. Confirm the appearance of the mask and select your preferred reconstruction method. Typically, QSDR is chosen for images in MNI space. Otherwise, GQI is recommended. DTI metrics will be generated even if the DTI button is not selected.&#x20;

You may then press "Run Reconstruction". This may take a few minutes, and when it is complete the reconstructed image will appear in the lower section of the main window with a filename ending in ".fib.gz".

![](<../.gitbook/assets/Screen Shot 2024-02-21 at 2.19.00 PM.png>)

Select "Step T3: Fiber Tracking" and open the FIB file to begin generating a tractography map.&#x20;

![](<../.gitbook/assets/Screen Shot 2024-02-21 at 2.46.05 PM.png>)

The following screen will appear. This is the "Tracking Window". By selecting the "Fiber Tracking" button, a whole brain reconstruction of fiber tracts will be created.&#x20;

![DSI Studio's Tracking Window, opened after selecting Step T3 and entering the FIB file. ](<../.gitbook/assets/Screen Shot 2024-02-21 at 2.48.30 PM.png>)

After fiber tracking is complete, the tracking window will show the whole brain tractography map. For more information on quality assessment and troubleshooting, refer to [DSI Studio's documentation](https://dsi-studio.labsolver.org/doc/gui\_t3\_whole\_brain.html).&#x20;

<figure><img src="../.gitbook/assets/Screen Shot 2024-02-21 at 3.40.25 PM.png" alt=""><figcaption><p>The whole brain tractography can be viewed in the center of the Tracking Window after selecting the "Fiber Tracking" button. </p></figcaption></figure>

##
