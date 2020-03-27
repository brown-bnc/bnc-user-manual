# fmriprep

## Running fmriprep

{% tabs %}
{% tab title="Oscar" %}
## 1. Write a batch script

We keep up-to-date Singularity images for `fmriprep` for the community. In order to run `fmriprep` in Oscar, you'll need to write a batch script. We provide an example below

{% code title="~/src/fmriprep\_shenhav\_example.sh -- Filename and not part of the script!" %}
```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -c 8
#SBATCH --mem=24G
#SBATCH --time 18:00:00
#SBATCH -J fmriprep
#SBATCH --output fmriprep-log-%J.txt

#---------CONFIGURE THESE VARIABLES--------------
root_dir=/gpfs/data/bnc/mrestrep/bids-export
participant_label=tcb2002
investigator=shenhav
study_label=201226
fmriprep_version=20.0.1
#---------END OF VARIABLES------------------------


singularity run --cleanenv                                         \
  --bind ${root_dir}/${investigator}/study-${study_label}:/data    \
  --bind /gpfs/scratch/${USER}:/scratch                            \
  --bind /gpfs/data/bnc/licenses:/licenses                         \
  /gpfs/data/bnc/simgs/fmriprep/fmriprep-${fmriprep_version}.sif   \
  /data/bids /data/bids/derivatives/fmriprep-${fmriprep-version}   \
  participant --participant-label ${participant_label}             \
  --fs-license-file /licenses/freesurfer-license.txt               \
  -w /scratch/fmriprep                                             \
  --omp-nthreads 16 --nthreads 16 --stop-on-first-crash


```
{% endcode %}

### ✋Understanding the batch script

* The first path ot the script configures the variables \(e.g., number of cores, memory, etc\) for your JOB
* The second part invokes `fmirprep` singularity image. Keep in mind the following considerations:
  * Singularity containers run as your user, and therefore should have the same read/write permissions as your local user in the cluster
  * Singularity containers only share  `$HOME` with the Oscar file system. Therefore, any other location that we want to read and write to/from, needs to be specified using the `--bind hostfolder:containerfolder` input. **This includes any directory in your home directory that is a symbolic link.** For instance `$HOME/data` usually points to  `/gpfs/data/<group>` in that case we must **bind `/gpfs/data/<group>`**
  * You must specify the location **inside the container** of the Free Surfer license.

✋ **Troubleshooting:**

`fmriprep` may fail for many reasons. Here are few tips:

* Freesurfer is often difficult to get to completion, if it helps troubleshooting, you can turn FreeSurfer reconstruction foo by adding the flag `--fs-no-reconall`
* Familiarize yourself with the inputs and don't hesitate to ask the developers for questions. Good places to look/ask for help are their GitHub issues and the [Neurostars forum](https://neurostars.org)

## 2. Run the batch script

```text
cd ~/src
sbatch fmriprep_shenhav_example.sh
```

For more information about managing your job, see the [Oscar documentation](https://docs.ccv.brown.edu/oscar/submitting-jobs/managing-jobs)
{% endtab %}

{% tab title="Docker" %}
Let us know if you are interested in this documentation!
{% endtab %}
{% endtabs %}



## Getting a different version than what is installed in Oscar.

If you wish to use version not available under `/gpfs/data/bnc/simg` you'll need to build the image. Singularity images can be large, therefore consider using a place with suffiecient quota and changing the default location singularity uses to cache these files. Please see Oscar dosumentation.

To build the image, you can run:

```
version=1.5.8
singularity build /my_images/fmriprep-${version}.sif docker://poldracklab/fmriprep:${version}
```

Replace `version` in the command above with the desired docker tag. You can find, the latest tags of fmriprep [here](https://hub.docker.com/r/poldracklab/fmriprep/tags)

{% hint style="info" %}
 To support scientific reproducibility, it is recommeded to use a specifc tag e.g., `1.5.8` instead of `latest` 
{% endhint %}

