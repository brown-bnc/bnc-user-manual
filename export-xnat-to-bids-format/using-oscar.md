# Using Oscar

## Installation

**🎉 Skip -** We keep a Singularity image of the most recent tagged release of [`xnat-tools`](https://github.com/brown-bnc/xnat-tools)in Oscar.

## Running XNAT2BIDS

The xnat-tools package provides a convenience `xnat2bids` script to facilitate data export and conversion to BIDS. The script is documented [here](https://brown-bnc.github.io/xnat-tools/1.0.0/xnat2bids/)

{% hint style="info" %}
In Oscar we need to wrap our commands in a batch file or use an interactive or VNC session. Please **remember to not run processing on the login nodes**
{% endhint %}

### Batch Script

We keep an up-to-date sample scripts and instructions in this repository [https://github.com/brown-bnc/xnat-tools-examples](https://github.com/brown-bnc/xnat-tools-examples). 

⚠️ Do not store your password directly in scripts. You could use temporary files or environment variables. However, if you prefert typing it interactively, then using an Interactive session is the only way.

### Interactive session

Here we start the software as an **interactive** job of one hour.

#### Login into oscar and start an interactive section by typing

```text
interact -n 2 -t 01:00:00 -m 8g
```

#### Specify the version of `xnat-tools` to

```text
version=v1.0.0
```

####  Set up paths

Set up the working directory in Oscar, usually `/gpfs/data/<your PI's group>`. We pass \(bind\) this path to singularity so that it can access/see it

```text
data_dir=/gpfs/data/bnc
```

Output directory. It has to be under the data\_dir, otherwise it won't be seen by singularity. It also needs to be created \(unless it already exists\)

```text
bids_root_dir=${data_dir}/shared/bids-export/${USER}
mkdir -m 775 ${bids_root_dir} || echo "Output directory already exists"
```

Path to Singularity Image for xnat-tools \(maintained by bnc\)

```text
simg=/gpfs/data/bnc/simgs/brownbnc/xnat-tools-${version}.sif
```

#### Define XNAT 

```text
XNAT_USER="youruser" #change to a valid user
XNAT_SESSION="XNAT3_E04441" #change to a valid session
```

#### Run the main executable via singularity

The following command runs xnat2bids \(via singularity\) command to extract DICOMs from xnat and export to BIDS. The command tells singularity to launch `xnat-tools-${version}.sif` image and execute the `xnat2bids` command with the given inputs. The `-B ${data_dir}` makes the `data_dir` directory available to the singularity container. The `-i` is asking to only process the first sequence. For a full list of inputs, please see the [xnat-tools documentation](https://brown-bnc.github.io/xnat-tools/1.0.0/xnat2bids/)

```text
singularity exec --contain -B ${data_dir} ${simg} \
    xnat2bids ${XNAT_SESSION} ${bids_root_dir} \
    -u ${XNAT_USER} \
    -i 1
```



