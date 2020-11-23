# Docker

To run the validator using Docker simply pass the bids directory as shown below. The bids directory is the parent directory of the dataset\_description.json file

```text
bids_directory=<your bids directory>
docker run -ti --rm -v ${bids_directory}:/data:ro bids/validator /data
```

