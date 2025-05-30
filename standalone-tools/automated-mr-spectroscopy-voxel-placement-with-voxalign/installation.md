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

***

<details>

<summary>Use of voxalign is governed by the following license</summary>

Copyright 2025, Brown University, Providence, RI.

All Rights Reserved

Permission to use, copy, modify, and distribute this software and\
its documentation for any purpose other than its incorporation into a\
commercial product or service is hereby granted without fee, provided\
that the above copyright notice appear in all copies and that both\
that copyright notice and this permission notice appear in supporting\
documentation, and that the name of Brown University not be used in\
advertising or publicity pertaining to distribution of the software\
without specific, written prior permission.

BROWN UNIVERSITY DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,\
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ANY\
PARTICULAR PURPOSE. IN NO EVENT SHALL BROWN UNIVERSITY BE LIABLE FOR\
ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES\
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN\
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF\
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

</details>
