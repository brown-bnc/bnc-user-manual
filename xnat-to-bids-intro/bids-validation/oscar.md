---
description: Running the BIDS validator on Oscar
---

# Oscar

### 0. Summary of commands

```bash
version=v1.14.6
bids_directory=${HOME}/xnat-exports/bnc/study-demodat/bids
simg=/oscar/data/bnc/simgs/bids/validator-${version}.sif
singularity exec --bind ${bids_directory}:${bids_directory}:ro ${simg} \bids-validator ${bids_directory}
```

### 1. Log into oscar and start an interactive section

If you are using the [Desktop app on Open OnDemand](../using-oscar/oscar-utility-script/#id-1.-start-an-interactive-session), then you are already inside an interactive session and you just need to open the terminal. Otherwise, you can start an interactive job of 1 hour with&#x20;

```bash
interact -n 2 -t 01:00:00 -m 8g
```

### 2. Define variables

#### Specify the version of the validator you want to use.&#x20;

```bash
version=v1.14.6
```

You can run `ls /oscar/data/bnc/simgs/bids/validator*` to print all available versions&#x20;

#### Set up paths

Specify your **bids directory.** This is where `dataset_description.json` file lives

```bash
bids_directory=${HOME}/xnat-exports/bnc/study-demodat/bids
```

Path to Singularity Image for the bids-validator (maintained by bnc)

```bash
simg=/oscar/data/bnc/simgs/bids/validator-${version}.sif
```

### 3. Run the main executable via singularity

The following command runs the `bids-validator` executable (via singularity) to test if a directory is BIDS compliant. The command tells singularity to launch the `validator-${version}.sif` image and execute the `bids-validator` command. The bids validator expects a directory as an input, which in this case corresponds to `${bids_directory}`. The `--bind ${bids_directory}:${bids_directory}:ro` makes the `${HOME}/xnat-exports/bnc/study-demodat/bids` available read-only inside the container at the same path.&#x20;

```bash
singularity exec --bind ${bids_directory}:${bids_directory}:ro ${simg} \bids-validator ${bids_directory}
```

