---
description: Running the BIDS validator on Oscar
---

# Oscar

### 0. Summary of commands

{% code overflow="wrap" %}
```bash
version=v2.3.0
bids_directory=${HOME}/xnat-exports/bnc/study-demodat2/bids
simg=/oscar/data/bnc/simgs/brownbnc/xnat-tools-${version}.sif
apptainer exec \
  --no-home \
  -B ${bids_directory}:/bids:ro \
  -B /oscar/scratch/${USER}:/scratch \
  ${simg} \
  env DENO_DIR=/scratch/deno deno run -A -qr jsr:@bids/validator /bids
```
{% endcode %}

### 1. Log into oscar and start an interactive section

If you are using the [Desktop app on Open OnDemand](../using-oscar/oscar-utility-script/#id-1.-start-an-interactive-session), then you are already inside an interactive session and you just need to open the terminal. Otherwise, you can start an interactive job of 1 hour with&#x20;

```bash
interact -n 2 -t 01:00:00 -m 8g
```

### 2. Define variables

#### Specify the version of xnat-tools you want to use. Any version from [v2.1.0](https://github.com/brown-bnc/xnat-tools/releases/tag/v2.1.0) onward will automatically run the most recent version of the BIDS validator.

```bash
version=v2.3.0
```

You can run `ls /oscar/data/bnc/simgs/brownbnc/xnat-tools*` to print all available versions&#x20;

#### Set up paths

Specify your **bids directory.** This is where `dataset_description.json` file lives

```bash
bids_directory=${HOME}/xnat-exports/bnc/study-demodat2/bids
```

Path to Apptainer/Singularity Image for xnat-tools, which contains the BIDS validator&#x20;

```bash
simg=/oscar/data/bnc/simgs/brownbnc/xnat-tools-${version}.sif
```

### 3. Run the main executable via apptainer \[formerly singularity]

The following command runs the BIDS validator (via our xnat-tools apptainer image) to test if a directory is BIDS compliant. The command tells apptainer to launch the `xnat-tools-${version}.sif` image and run the `@bids/validator` with a program called deno. The bids validator expects a directory as an input, which in this case corresponds to `${bids_directory}`. The `--bind ${bids_directory}:${bids_directory}:ro` makes the `${HOME}/xnat-exports/bnc/study-demodat2/bids` available read-only inside the container at the same path.&#x20;

```bash
apptainer exec \
  --no-home \
  -B ${bids_directory}:/bids:ro \
  -B /oscar/scratch/${USER}:/scratch \
  ${simg} \
  env DENO_DIR=/scratch/deno deno run -A -qr jsr:@bids/validator /bids
```

