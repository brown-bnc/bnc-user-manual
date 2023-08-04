---
description: >-
  a BIDS app that automates comprehensive quality assessment of structural and
  functional MRI data
---

# mriqc

It is good practice to inspect the quality of your data _before_ running any further processing (like [fmriprep](fmriprep.md)). [mriqc](https://mriqc.readthedocs.io/en/latest/index.html) is a BIDS app that makes it easy to get both visual and quantitative assessments of your data quality. Here are simple instructions for running mriqc on Oscar - all you need to start is a valid BIDS dataset.

### 1. write a batch script

We keep up-to-date Singularity images for mriqc for the community. (Look in `/oscar/data/bnc/simgs/nipreps/` to see which versions we currently have available.) In order to run mriqc on Oscar, you'll need to write a batch script. Here is an example that runs mriqc on the anatomical and functional data from the entire demodat dataset (which I have already exported from xnat and converted to BIDS format using the [Oscar utility script](../xnat-to-bids-intro/using-oscar/oscar-utility-script.md) for this example).

{% code title="demodat_mriqc_example.sh -- Filename and not part of the script!" %}
```bash
#!/bin/sh
#SBATCH -t 04:00:00
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --mem-per-cpu=4G
#SBATCH -J mriqc 
#SBATCH --output mriqc-%J.txt
#SBATCH --mail-user example-user@brown.edu
#SBATCH --mail-type ALL

#---------CONFIGURE THESE VARIABLES--------------
mriqc_version=23.1.0
bids_dir=/oscar/path/to/bids
#---------END OF VARIABLES------------------------

simg=/oscar/data/bnc/simgs/nipreps/mriqc-${mriqc_version}.sif
qc_dir=${bids_dir}/derivatives/mriqc-${mriqc_version}/
echo $qc_dir
mkdir -p -m 775 ${qc_dir} || echo "Output directory already exists"

singularity exec --cleanenv                                         \
    --bind ${bids_dir}                                              \
    --bind /oscar/scratch/${USER}:/scratch                          \
    ${simg} mriqc ${bids_dir} ${qc_dir} participant group           \
    --modalities {T1w,bold} --mem_gb 4 --verbose-reports            \
    --omp-nthreads 16 --nprocs 16 --work-dir /scratch/mriqc 
```
{% endcode %}

#### ✳️ Understanding the batch script

* The first part of the script configures the variables (e.g., number of cores, memory, etc) for your job. Make sure to update the email address if you'd like to get email updates.
* The second part invokes the `mriqc` singularity image. Keep in mind the following:
  * Singularity containers run as your user, and therefore should have the same read/write permissions as your local user in the cluster
  * Singularity containers only share  `$HOME` with the Oscar file system. Therefore, any other location that we want to read and write to/from, needs to be specified using the `--bind hostfolder:containerfolder` input. **This includes any directory in your home directory that is a symbolic link.** For instance `$HOME/data` usually points to  `/oscar/data/<group>`, so we bind the full bids\_dir path rather than using the `$HOME/data` symbolic link.
  * See the [mriqc documentation](https://mriqc.readthedocs.io/en/latest/running.html) for additional options, including running only on specific participants within a BIDS dataset, or changing the data modalities you'd like to process (it looks like dwi is a work in progress that may be functional soon).&#x20;

### 2. Run the batch script

```
cd /path/to/sbatch/script
sbatch demodat_mriqc_example.sh
```

For more information about managing your job, see the [Oscar documentation](https://docs.ccv.brown.edu/oscar/submitting-jobs/managing-jobs).

### 3. Examine the outputs

mriqc will produce an html report for each scan, for each participant, with many visualizations of different aspects of data quality. At the bottom of each report, you can click on "Extracted Image quality metrics (IQMs)" to see the values of [many different metrics](https://mriqc.readthedocs.io/en/latest/measures.html), depending on the scan type.

If you ran mriqc at both the "participant" and "group" level, as we did in the example, you will also get group-level reports for each scan type. These are extremely useful for identifying individual scans and/or participants that may have data quality issues that require a closer look. You can hover your cursor over any point in the html report plots to see which individual subject and scan it represents, and click it to open the associated html report.
