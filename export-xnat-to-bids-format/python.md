# Python

## Prerequisites:

We first need to install the dcm2niix . This is a dependency of Heudiconv, that doesn't get installed by Heudiconv itself

```text
brew install dcm2niix
```

## Installation

### Poetry

This package is developed using [Poetry](https://python-poetry.org). If you are familiar with Poetry, you can add it to your project via

```text
poetry add git+https://github.com/brown-bnc/xnat-tools.git
```

or for a tagged release

```text
poetry add git+https://github.com/brown-bnc/xnat-tools.git@v0.1.0-beta
```

You can also install xnat\_tools using the python package manager of your choice. For instance:

### **PIP**

* A Tagged Release

```text
pip install git+https://github.com/brown-bnc/xnat-tools.git@v0.1.0-beta
```

* Development \(Master branch\)

```text
pip install git+https://github.com/brown-bnc/xnat-tools.git
```

### **PIPX**

If you are using this package in a stand-alone fashion, and you don't want to use Docker, we recommend using pipx. Please check their [installation instructions](https://github.com/pipxproject/pipx).

Once pipx is installed you install as follows:

A Tagged Release

```text
pipx install git+https://github.com/brown-bnc/xnat-tools.git@v0.1.0-beta
```

Development \(Master branch\)

```text
pipx install git+https://github.com/brown-bnc/xnat-tools.git
```

## XNAT2BIDS

In order to export data from XNAT and convert it in one step you can use the `xnat2bids` script part of this package.

After installation, the console script `xnat2bids` is available in your system. You can invoke it from the terminal as follows:

```text
xnat_user=<user>
session=<xnat_accession_number>
bids_root_dir="~/data/bids-export"

xnat2bids --user ${xnat_user}  --session ${session} \
--bids_root_dir ${bids_root_dir}
```

### 

