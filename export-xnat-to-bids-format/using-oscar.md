# Using Oscar

## Installation

**🎉 Skip -** We keep a Singularity image of the most recent tagged release of [`xnat-tools`](https://github.com/brown-bnc/xnat-tools)in Oscar.

## Running XNAT2BIDS

The xnat-tools package provides a convenience `xnat2bids` script to facilitate data export and conversion to BIDS.

{% hint style="info" %}
In Oscar we need to wrap our commands in a batch file or use an interactive or VNC session. Please **remember to not run processing on the login nodes**
{% endhint %}

### Interactive session

Here we start the software as an **interactive** job of one hour. At the end of this section we show an equivalent **batch** script

Login into oscar and start an interactive section by typing

```text
interact -n 2 -t 01:00:00 -m 8g
```

```text
version=<write version here>
xnat_user=<write username>
session=<xnat_accession_number>
local_bids_dir=<local_directory_for_exporting e.g /gpfs/data/PI/bids>
simg_dir=/gpfs/data/bnc/simgs/brownbnc

singularity exec -B ${local_bids_dir}:/data/xnat/bids-export \
${simg_dir}/xnat-tools-${version}.sif xnat2bids --user ${xnat_user}       \
--session ${session} --session_suffix "01" --bids_root_dir "/data/xnat/bids-export"
```

**✨Versions**_:_

* `latest`: Is the build of master
* `vX.X.X`: Latest tagged stable release

{% hint style="info" %}
To support scientific reproducibility, it is recommended to use a specific tag e.g., `v0.1.2` instead of `latest`
{% endhint %}

You can confirm the tags [here](https://hub.docker.com/repository/docker/brownbnc/xnat-tools/tags?page=1). Also inside Oscar you can run `ls /gpfs/data/bnc/simgs/brownbnc | grep xnat-tools` to verify which versions are currently installed in Oscar.

⚠️ **bids\_root\_dir:** The value that we pass to this input, corresponds to the value of the bids root directory as mapped inside of the container, which in our example is `/data/xnat/bids-export`

⚠️ **Correcting for mislabeled sequences at the scanner: `xnat2bids`** can take a `json` file with a dictionary of sequence names to correct/change. It is important to remember that the path passed is the pass **inside** of the container. In our previous example, the only shared location between the host and the container are:

* The value of `local_bids_dir` as specified by `-B ${local_bids_dir}:/data/xnat/bids-export`
* `home` singularity does that by default

So the simplest approach would be to place your `json` somewhere inside `bids_root_dir` and pass the argument `--bidsmap_file /data/xnat/bids-export/bidsmaps/${session}.json` assuming that is the name of your file. An **example**\(s\) of a bidsmap file\(s\) lives [here](https://github.com/brown-bnc/xnat-tools/tree/master/bidsmaps)

⚠️ **Familiarize yourself with the inputs to xnat2bids**

For a full list of the inputs, you can run:

```text
singularity exec -B ${local_bids_dir}:/data/xnat/bids-export \
/gpfs/data/bnc/simgs/xnat-tools-${version}.sif xnat2bids --help
```

#### Batch Script

{% code title="~/src/xnat2bids.sh -- Filename and not part of the script!" %}
```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -c 2
#SBATCH --mem=18G
#SBATCH --time 2:00:00
#SBATCH -J xnat2bids
#SBATCH --output xnat2bids-log-%J.txt

#---------CONFIGURE THESE VARIABLES--------------
version=<write version here e.g v0.1.2>
xnat_user=<write username>
session=<xnat_accession_number>
session_sufix="01"
local_bids_dir=<local_directory_for_exporting e.g /gpfs/data/PI/bids>
simg_dir=/gpfs/data/bnc/simgs/brownbnc
#---------END OF VARIABLES--------------

singularity exec -B ${local_bids_dir}:/data/xnat/bids-export \
${simg_dir}/xnat-tools-${version}.sif xnat2bids --user ${xnat_user}       \
--session ${session} --session_suffix ${session_suffix}  --bids_root_dir "/data/xnat/bids-export"
```
{% endcode %}

#### Run the batch script

```text
cd ~/src
sbatch xnat2bids.sh
```

For more information about managing your jobs, see the [Oscar documentation](https://docs.ccv.brown.edu/oscar/submitting-jobs/managing-jobs)

