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

## Region-Based Fiber Tracking: Seed Regions

Select "color" under the Slice dropdown menu:

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 11.27.41 AM.png>)

Load the following "Tracking Parameters into dsi studio

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 11.29.53 AM.png>)

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 11.32.21 AM.png>)

The tracking parameters settings should be:

```
termination index =nqa
Threshold = 0.1
Angular Threshold = 0
Stepsize(mm) = 0.0
Smoothing = 1.0
Min length (mm) =30.0
Max length (mm) = 300.0
Seed orientation = primary
Seed position = subvoxel
Randomize Seeding = off
Check ending = off
Direction Interpolation= trilinear
Tracking algorithm = streamline(euler)
Terminate if= 100,000 tracts
Thread Count =2
Output format= trk.gz
```



For each brain slice create a new region. In general you should have about 1-2 seed regions per tract and 0-2 ROI regions per tract.  Under "type" select "seed" for seed regions or "ROI" for ROI regions.

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 11.48.10 AM.png>)

REVIEW this diagram to acquaint yourself with the toolbar.

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 11.50.51 AM.png>)

RECONSTRUCTING the corticospinal tract (cst):

Move the axial slide bar until you reach a slice that looks similar to one of the boxes.Then using the freeform option, make a circle around the region that the arrow is pointing to.  Follow these steps for the remaining three boxes.  Be sure to make a new region with each slice/box.

&#x20;

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 11.57.37 AM.png>)

Make sure all four ROI regions are checked and then select "Fiber Tracking"

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 12.00.07 PM.png>)

If the resulting tract does not look like the track in #4 box above, create exclusion regions to remove erroneous streamline fibers.  To do this select "ROA".  Then using the square or the freeform option enclose the area where the erroneous fiber is located.

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 12.09.25 PM.png>)

All exclusion regions should be created using the same ROA region. For example in the image below three exclusion regions (two on a coronal slice and one on an axial slice were drawn but only one ROA region was created.

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 12.13.42 PM.png>)

FINAL STEP: save all of the files: tract image, regions and density image.make sure the file names are unique. Example:

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 12.18.02 PM.png>)

Save the regions by selection "Save all regions as multiple files" then open when the appropriate folder location is created

![](../.gitbook/assets/screen-shot-2020-09-14-at-12.19.28-pm.png)

Save the tract image then select the save button

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 12.20.50 PM.png>)

Save the density map by selecting "tract density image" then "diffusion space", select "no" in response to whether to export directional color, then select "yes" in response to selecting the whole tract.

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 12.24.10 PM.png>)

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 12.24.15 PM.png>)

![](<../.gitbook/assets/Screen Shot 2020-09-14 at 12.24.21 PM.png>)

NOTE: There are many other white matter fiber tracts of interest. I can provide  details on how to reconstruct other tracts if you send a request.
