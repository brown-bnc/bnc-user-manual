---
description: Running the BIDS validator in Oscar
---

# Oscar

### Interactive session

Here we start the software as an **interactive** job of one hour.

#### Login into oscar and start an interactive section by typing

```text
interact -n 2 -t 01:00:00 -m 8g
```

#### Specify the version of validator to

```text
version=v1.7.2
```

####  Set up paths

Indicate the **bids directory.** This is where `dataset_description.json` file lives

```text
bids_directory=/gpfs/data/bnc/shared/bids-export/mrestrep/sanes/study-sadlum/bids
```

Path to Singularity Image for the bids-validator \(maintained by bnc\)

```text
simg=/gpfs/data/bnc/simgs/bids/validator-${version}.sif
```

#### 

#### Run the main executable via singularity

The following command runs the `bids-validator` executable \(via singularity\)  to test if a directory is BIDS compliant. The command tells singularity to launch `validator-${version}.sif` image and execute the `bids-validator` command. The bids validator expects the a directory as an input, which in this case corresponds to `${bids_directory}`. The `-B ${data_dir}` makes the `data_dir` directory available to the singularity container. 

{% tabs %}
{% tab title="Oscar" %}
```text
singularity exec -B ${bids_directory} ${simg} \
bids-validator ${bids_directory}
```
{% endtab %}
{% endtabs %}



