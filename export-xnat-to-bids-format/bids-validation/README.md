# BIDS Validation

## BIDS Validation

After running the `xnat2bids` software, it is recommended to run the [BIDS Validator](https://github.com/bids-standard/bids-validator#docker-image) in your data. We provide instructions to do it programmatically, but there is also a website where you can do it interactively.

{% tabs %}
{% tab title="Docker" %}
To run the validator using Docker simply pass the bids directory as shown below. The bids directory is the parent directory of the `dataset_description.json` file

```text
bids_directory=<your bids directory>
docker run -ti --rm -v ${bids_directory}:/data:ro bids/validator /data
```
{% endtab %}

{% tab title="Oscar" %}
To run the validator using Singularity in Oscar you simply pass the bids directory as shown below. The bids directory is the parent directory of the `dataset_description.json` file

```text
version=v1.4.3 #check latest available version
bids_directory=<bids directory>
simgs_dir=/gpfs/data/bnc/simgs/bids/

singularity exec -B ${bids_directory}:/data:ro \
${simgs_dir}/validator-${version}.sif bids-validator /data
```
{% endtab %}
{% endtabs %}



