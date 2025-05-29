---
description: Voxalign runs on a separate computer, not the scanner console
---

# Installation

{% hint style="info" %}
Voxalign is available on github at [https://github.com/brown-bnc/voxalign](https://github.com/brown-bnc/voxalign) (currently set to private - contact Elizabeth at cobre-bnc@brown.edu for access)
{% endhint %}

### Use voxalign on Tess (mac mini behind scanner operator)  \<RECOMMENDED>&#x20;

\*Make sure you log in as mrfuser\*

A voxalign environment is already created, so all you have to do is open a terminal window and type \
`source ~/Desktop/voxalign/bin/activate`

***

### Set up on your own computer:

I recommend installing in a python virtual environment:

1. create an environment named voxalign: `python3 -m venv voxalign`
2. activate it: `source /path/to/env/voxalign/bin/activate`
3. install voxalign: \
   `pip install` [`https://github.com/brown-bnc/voxalign/archive/master.zip`](https://github.com/brown-bnc/voxalign/archive/master.zip)

You'll also need to [install FSL](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/install/index) on your computer.

***

### Now that your environment is activated, you can:

* Calculate a voxel prescription that exactly matches a prescription from an earlier scan session on the same participant: [**run-voxalign**](multi-session-alignment.md)&#x20;
* Calculate a voxel position(s) that matches an MNI coordinate(s) of your choice: [**mni-lookup**](center-on-mni-coordinate.md)&#x20;
* Calculate the dice coefficient (a measure of overlap) to assess how well-aligned your session 1 and session 2 voxels ended up: [**dice-coef**](quantify-voxel-overlap.md)&#x20;
