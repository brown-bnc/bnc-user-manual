---
description: https://fmriprep.org/en/stable/
---

# fmriprep

## Running fmriprep

{% tabs %}
{% tab title="Oscar" %}
## 1. Write a batch script

We keep up-to-date Singularity images for `fmriprep` for the community. (Look in `/oscar/data/bnc/simgs/nipreps/` to see which versions we currently have available.) In order to run `fmriprep` on Oscar, you'll need to write a batch script. Here is an example:

{% code title="demodat_fmriprep_example.sh -- Filename and not part of the script!" %}
```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH --time 18:00:00
#SBATCH -J fmriprep
#SBATCH --output fmriprep-log-%J.txt
#SBATCH --mail-user example-user@brown.edu
#SBATCH --mail-type ALL

#---------CONFIGURE THESE VARIABLES--------------
root_dir=/oscar/data/mworden/elorenc1/xnat-exports/bnc/
participant_label=005
study_label=demodat
fmriprep_version=23.1.3
#---------END OF VARIABLES------------------------

singularity run --cleanenv                                         \
  --bind ${root_dir}/study-${study_label}:/data                    \
  --bind /oscar/scratch/${USER}:/scratch                            \
  --bind /oscar/data/bnc/licenses:/licenses                         \
  /oscar/data/bnc/simgs/nipreps/fmriprep-${fmriprep_version}.sif    \
  /data/bids /data/bids/derivatives/fmriprep-${fmriprep_version}   \
  participant --participant-label ${participant_label}             \
  --output-spaces T1w MNI152NLin2009cAsym MNI152NLin6Asym:res-2    \
  --fs-license-file /licenses/freesurfer-license.txt               \
  -w /scratch/fmriprep                                             \
  --omp-nthreads 16 --nthreads 16 --stop-on-first-crash

```
{% endcode %}

### ✋Understanding the batch script

* The first part of the script configures the variables (e.g., number of cores, memory, etc) for your JOB. Make sure to update the email address if you'd like to get email updates about your job.
* The second part invokes `fmriprep` singularity image. Keep in mind the following considerations:
  * Singularity containers run as your user, and therefore should have the same read/write permissions as your local user in the cluster
  * Singularity containers only share  `$HOME` with the Oscar file system. Therefore, any other location that we want to read and write to/from, needs to be specified using the `--bind hostfolder:containerfolder` input. **This includes any directory in your home directory that is a symbolic link.** For instance `$HOME/data` usually points to  `/oscar/data/<group>` in that case we must **bind `/oscar/data/<group>`**
  * You must specify the location **inside the container** of the FreeSurfer license.

## 2. Run the batch script

```
cd /path/to/sbatch/script
sbatch demodat_fmriprep_example.sh
```

For more information about managing your job, see the [Oscar documentation](https://docs.ccv.brown.edu/oscar/submitting-jobs/managing-jobs)



✋ **Troubleshooting:**

`fmriprep` may fail for many reasons. Here are few tips:

* Freesurfer is often difficult to get to completion, if it helps troubleshooting, you can turn FreeSurfer reconstruction off by adding the flag `--fs-no-reconall`
* Familiarize yourself with the inputs and don't hesitate to ask the developers questions. Good places to look/ask for help are their GitHub issues and the [Neurostars forum](https://neurostars.org)

⚠️ At least as of fmriprep version 23.1.3, susceptibility distortion correction performs very poorly if you supply phase difference field maps like we have in the demodat dataset, actually making distortion _worse._ Distortion correction performance is much better with the 20.2.7 LTS version of fmriprep, which we also have available on Oscar.
{% endtab %}

{% tab title="Docker" %}
Let us know if you are interested in this documentation!
{% endtab %}
{% endtabs %}

## Getting a different version than what is installed in Oscar.

If you wish to use a version not available under `/oscar/data/bnc/simg/nipreps`, you'll need to build the image. Singularity images can be large, therefore consider using a place with sufficient quota and changing the default location singularity uses to cache these files. Please see [Oscar documentation](https://docs.ccv.brown.edu/oscar/singularity-containers/building-images).

To build the image, you can run:

```
version=22.0.0
singularity build fmriprep-${version}.sif docker://nipreps/fmriprep:${version}
```

Replace `version` in the command above with the desired docker tag. You can find the latest tags of fmriprep [here](https://hub.docker.com/r/nipreps/fmriprep/tags)

{% hint style="info" %}
&#x20;To support scientific reproducibility, it is recommended to use a specific tag e.g., `22.0.0` instead of `latest`&#x20;
{% endhint %}
