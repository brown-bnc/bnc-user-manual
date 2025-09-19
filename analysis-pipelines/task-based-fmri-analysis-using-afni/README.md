# Task-Based fMRI Analysis Using AFNI

Here, we provide a processing pipeline for functional MRI data using the [AFNI](https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/index.html) software package.&#x20;

The tutorial is split into two sections:&#x20;

1. A single subject walkthrough of how to download data from xnat and preprocess using afni.
2. A group analysis pipeline, including first level preprocessing of all subjects/sessions of demodat2, and continuing on to second level analysis.&#x20;

To enable both block and event related analyses, we designed a single functional sequence that includes two different concurrent tasks. These are 1) the visual hemifield localizer task (also called the checkerboard, or checks, task) and 2) a button pressing task for motor cortex activation.&#x20;

## Block Design: The Visual Hemifield Localizer Task

This is a very simple visual task, with alternating 12s blocks of flashing checkerboard stimuli in the left and right visual hemifields. Because of the contralateral organization of visual cortex, we can identify the right visual cortex by selecting voxels that prefer stimulation on the left side of visual space, and vice versa.&#x20;

## Event-Related Design: Button Pressing Task

To activate areas of the motor cortex, we included a button press task which occurs throughout the alternating flashing checkerboards. At random and variable inter-trial intervals (4, 6, or 8), the white fixation cross in the center of the screen flashes to either red or blue for 300ms (0.3 seconds). Once the participant sees the color change, they press the corresponding button (right index finger for red, left index finger for blue).&#x20;

Below is a figure depicting these two concurrent tasks.&#x20;

<figure><img src="../../.gitbook/assets/Demodat2 Documentation (1).jpg" alt=""><figcaption></figcaption></figure>

The psychopy script and all necessary files can be downloaded here:&#x20;

{% file src="../../.gitbook/assets/Demodat2_Psychopy_Files.zip" %}
