# Using Docker

## Installation

```text
version=v0.1.0
docker pull brownbnc/xnat_tools:${version}
```

**✨Versions**_:_

* `latest`: Is the build of master
* `vX.X.X`: Latest tagged stable release

{% hint style="info" %}
To support scientific reproducibility, it is recommeded to use a specifc tag e.g., `v0.1.2` instead of `latest`
{% endhint %}

You can confirm the tags [here](https://hub.docker.com/repository/docker/brownbnc/xnat-tools/tags?page=1)

## Running XNAT2BIDS

The xnat\_tools package provides a convinience `xnat2bids` script to facilitate data export and conversion to BIDS. In general, the script inside the container is invoked as follows:

```text
xnat_user=<user>
session=<xnat_accession_number>
bids_root_dir="~/data/bids-export"
session_suffix="01"

docker run --rm -it -v ${bids_root_dir}:/data/xnat/bids-export   \
brownbnc/xnat-tools:${version} xnat2bids --user ${xnat_user}       \
--session ${session} --session_suffix ${session_suffix} --bids_root_dir /data/xnat/bids-export
```

The previous command starts the `brownnbnc/xnat-tools` container. `-it` indicates that the container is interactive `--rm` tells docker to remove the container once it is done. `v` tells docker to map the local \(in your computer\) directory `bids_root_dir` to `/data/xnat/bids-export` inside of the container. We are also telling docker to launch the `xnat2bids` executable and we are passing the inputs to that executable.

⚠️ **bids\_root\_dir:** The value that we pass to this input, corresponds to the value of the bids root directory as mapped inside of the container, which in our examble is `/data/xnat/bids-export`

⚠️ **Correcting for misslabeled sequences at the scanner: `xnat2bids`** can take a `json` file with a dictionary of sequence names to correct/change. It is important to remember that the path passed is the pass **inside** of the container. In our previous example, the only shared location between the host and the container is:

* The value of `bids_root_dir` as specified by `-v ${bids_root_dir}:/data/xnat/bids-export`

Therefor the simpliest approach would be to place your `json` somewhere inside `bids_root_dir` and pass the argument `--bidsmap_file /data/xnat/bids-export/bidsmaps/${session}.json` assuming that is the name and location of your file.

⚠️ **Familiarize yourself with the inputs to xnat2bids**

For a full list of the inputs, you can run:

```text
docker run --rm -it -v ${bids_root_dir}:/data/xnat/bids-export   \
brownbnc/xnat-tools:${version} xnat2bids --help
```

