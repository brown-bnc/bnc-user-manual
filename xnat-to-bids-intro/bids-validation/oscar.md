---
description: Running the BIDS validator in Oscar
---

# Oscar

### 0. Summary of commands

```
interact -n 2 -t 01:00:00 -m 8g
version=v1.8.0
bids_root_dir=${HOME}/xnat-exports/bnc/study-demodat/bids
simg=/gpfs/data/bnc/simgs/bids/validator-${version}.sif
singularity exec --bind ${bids_root_dir} ${simg} \bids-validator ${bids_root_dir}
```

### 1. Start interactive session

If you are not already inside an interactive session please start one. Here we start an **interactive** job of one hour. If you are using VNC, then you are already inside an interactive session and you just need to open the terminal

#### Login into oscar and start an interactive section by typing

```
interact -n 2 -t 01:00:00 -m 8g
```

### 2. Define variables

#### Specify the version of validator to

```
version=v1.8.0
```

#### &#x20;Set up paths

Indicate the **bids directory.** This is where `dataset_description.json` file lives

```
bids_directory=${HOME}/xnat-exports/bnc/study-demodat/bids
```

Path to Singularity Image for the bids-validator (maintained by bnc)

```
simg=/gpfs/data/bnc/simgs/bids/validator-${version}.sif
```

####

#### Run the main executable via singularity

The following command runs the `bids-validator` executable (via singularity)  to test if a directory is BIDS compliant. The command tells singularity to launch `validator-${version}.sif` image and execute the `bids-validator` command. The bids validator expects the a directory as an input, which in this case corresponds to `${bids_directory}`. The `--bind ${bids_directory}:${bids_directory}:ro` makes the `${HOME}/xnat-exports/bnc/study-demodat/bids` available read-only inside the container at the same path.&#x20;

{% tabs %}
{% tab title="Oscar" %}
```
singularity exec -B ${data_dir}:ro ${simg} \
bids-validator ${bids_directory}
```
{% endtab %}
{% endtabs %}

```
singularity exec --bind ${bids_directory}:${bids_directory}:ro ${simg} \bids-validator ${bids_directory}
```

