# Step-wise via Interact Session

🛑 We highly recommend using the [Oscar utility script](oscar-utility-script/) instead of this older approach.

## Running XNAT2BIDS

The xnat-tools package provides a convenient `xnat2bids` script to facilitate data export and conversion to BIDS. The script is documented on [the BNC github](https://brown-bnc.github.io/xnat-tools/1.0.0/xnat2bids/), and the package documentation is useful for knowing the full list of inputs and defaults. We will demonstrate how to call that script within Oscar using the BNC's demo dataset.&#x20;

### 0. Summary of commands

Before getting started, we have grouped all the commands executed in this page for your reference

```bash
interact -n 2 -t 01:00:00 -m 8g
version=v1.1.1
bids_root_dir=${HOME}/xnat-exports
mkdir -m 775 ${bids_root_dir} || echo "Output directory already exists"
simg=/oscar/data/bnc/simgs/brownbnc/xnat-tools-${version}.sif
XNAT_USER=${USER} 
XNAT_SESSION="XNAT_E01849"
singularity exec --no-home --bind ${bids_root_dir} \
    ${simg} \
    xnat2bids ${XNAT_SESSION} ${bids_root_dir} \
    -u ${XNAT_USER} \
    -i 6
```



### 1. Start an interactive session

#### 1.1 Desktop app on Open OnDemand&#x20;

Connecting via the Desktop app on Open OnDemand is a friendly way to request an graphical interactive session in Brown's supercomputer - Oscar. When you request a new Desktop session, you will be asked to specify the necessary resources. For this example, you can choose the basic job with `2 Cores and 7GB Memory`. Once logged in, you are already inside an interactive session.&#x20;

<figure><img src="../../.gitbook/assets/Screen Shot 2022-10-25 at 3.59.53 PM.png" alt="After logging in to Oscar Open On Demand, you can start a virtual desktop session by navigating to &#x22;Home/Interactive Sessions/Desktop&#x22;"><figcaption></figcaption></figure>

Once your requested session is running, you can launch it by clicking the Launch Desktop button.

<figure><img src="../../.gitbook/assets/Screen Shot 2022-10-25 at 4.37.12 PM.png" alt="Launch a virtual desktop on Oscar OOD by pressing the &#x22;Launch Desktop&#x22; button. "><figcaption></figcaption></figure>

At this point, simply open the terminal

<figure><img src="../../.gitbook/assets/Screen Shot 2022-10-25 at 4.02.19 PM.png" alt="In the OOD Desktop, you can open a terminal by pressing the icon on the bottom of the screen. "><figcaption><p>OOD Desktop app. Teal arrow points to Terminal icon to be launched</p></figcaption></figure>

#### 1.2 SSH&#x20;

To connect via SSH, you type `ssh username@ssh.ccv.brown.edu`. If this is your first time connecting via ssh, you will be asked to trust the remote computer (Oscar), your Brown credentials, and unless you are connected to VPN, you will be required to use DUO.

At this point you arrive at a login node. **We will need to start an interactive session/job** by typing

```bash
interact -n 2 -t 01:00:00 -m 8g
```

This starts an interactive job for one hour.

### 2. Define variables

We will now define a series of shell variables that will allow us to keep our commands more reusable. This will also be useful if you later decide to move to [batch scripts](../../xnat-to-bids-dive-in/oscar-sbatch-scripts.md), which provide a better way to run jobs simultaneously and without constant interaction.&#x20;

{% hint style="info" %}
When defining shell Variables, make sure to not have any spaces in the variable name, the assigned value or in between the equal sign

The variable will only be defined during the current shell session. If you close your terminal or interactive session, the variables will need to be redefined
{% endhint %}

{% hint style="info" %}
If you want to copy-paste from these docs to the terminal in the OOD Desktop, click on the Copy to Clipboard Icon on the right of the code snippets. To paste into the terminal you will need to use the right click of your mouse and choose "Paste", or press `Ctrl+Shift+V`.
{% endhint %}

#### 2.1 Define the version of `xnat-tools`

We recommend using the latest available version. We keep a list of the released versions on [our xnat-tools github](https://github.com/brown-bnc/xnat-tools/releases). The version specified here is likely the latest we have tested. If you test a newer version, we'd love your contributions to this documentation!

```bash
version=v2.3.0
```

#### &#x20;2.2 Set up paths

**BIDS Root directory**

This is the directory where data will be written. If the directory does not exist then it needs to be created.&#x20;

{% hint style="info" %}
For this sample walkthrough, you can use the path exactly as shown below. The `${USER}` variable is a systemwide variable and it is automatically interpreted as your OSCAR user. However, once you are using your own data, you should export to directories in your PI's data folder, which typically follows the pattern `/gpfs/data/<PI oscar user>`
{% endhint %}

```bash
bids_root_dir=${HOME}/xnat-exports
mkdir -m 775 ${bids_root_dir} || echo "Output directory already exists"
```

**Path to Singularity Image**&#x20;

This is maintained by bnc and we will be pointing to the version defined above

```bash
simg=/oscar/data/bnc/simgs/brownbnc/xnat-tools-${version}.sif
```

#### XNAT USER and SESSION&#x20;

Typically, your XNAT user is the same as your Brown user. Finding the session ID was explained in [our "Getting Started" section](../getting-started.md#requirements). In this example we leverage the `$USER` variable to set your XNAT user. This is possible because both oscar username and XNAT username are typically the same (i.e your Brown username). For the session, we are using the accession number for participant 101 of the demo dataset

```bash
XNAT_USER=${USER} #only change if oscar user doesn't match XNAT user (rare)
XNAT_SESSION="XNAT_E01849" #ACCESSION of participant 101 session 01 in sample data
```

### 3. Understanding Singularity Containers&#x20;

In the following section we will demonstrate how to run our software. Instead of directly installing the Python package `xnat-tools` we are going to run it from inside a **container**, which we have been referring to as "the singularity image/container". If you are new to containers, in a nutshell, a container allows for packaging all OS and package dependencies together so it can run in any computer. Docker containers have become very popular, you can learn a bit more about them [on Docker's resource site](https://www.docker.com/resources/what-container). Singularity is a type of container that has specialized on running on shared HPC clusters. You can learn little more about Singularity from this [Apptainer user manual](https://singularity.hpcng.org/user-docs/master/introduction.html#why-use-singularity). We refer to docker containers and singularity containers interchangeably, as they can easily be converted from one format to another.

In the specific case of `xnat-tools` , the wrapping container has `Python` , `dcm2niix` and `heudiconv` installed which are all needed by our software. The [BNC Dockerfile for xnat-tools](https://github.com/brown-bnc/xnat-tools/blob/master/Dockerfile) provides some insight into how containers are built.

#### Understanding the file system of a container

Containers have their own file system, which is completely independent and isolated from the host where the container is run

{% hint style="info" %}
Because a container does not have the same directory structure as the host, we have to remember that paths like `/oscar/data/<PI>` only exist in Oscar, but not inside the container
{% endhint %}

#### Sharing paths between a container and the host computer (OSCAR)

If we want a directory/file that exists in OSCAR to be available inside our container, we need to tell Singularity that. We do so, by **binding a volume. This achieved by passing the flag `--bind <oscar_path>:<container_path>`.** If we want the path inside the container to be exactly as the path in OSCAR, we can omit the destination path, that is `--bind <oscar_path>`.

{% hint style="info" %}
The `--bind` flag can also be passed as `-B`
{% endhint %}

#### Singularity default behavior when it comes to sharing paths and environment variables

While generally speaking, a container is mostly isolated from the host, there are few exceptions. And these exceptions and default behaviors are different for Singularity and Docker. We will focus on Singularity rules here. By default Singularity binds the following locations

```dockerfile
 $HOME
 /sys:/sys
 /proc:/proc
 /tmp:/tmp
 /var/tmp:/var/tmp
 /etc/resolv.conf:/etc/resolv.conf
 /etc/passwd:/etc/passwd
 $PWD. 
```

**(Pro-Tip):** Generally speaking, the default behavior of Singularity works great. Sometimes however, some of the configurations included in your `$HOME` or environment variables set in your `$HOME/.bashrc` may create conflicts. Singularity offers several flags that can be passed to further isolate the container from the local host. These include

```dockerfile
--no-home
--contain
--containall
--no-mount
```

If you see such flags in our examples and want to learn more about them visit [the apptainer page on flag options.](https://singularity.hpcng.org/user-docs/master/bind_paths_and_mounts.html)

### 4. Running the executable

#### Printing the help

Let's start by making sure that we can successfully run our `xnat2bids` executable inside the container.

```bash
singularity exec ${simg} xnat2bids --help
```

Let's expand on the above command:

`singularity`: invokes singularity

`exec`: tells singularity we will be executing a command, in this case the command is `xnat2bids`

`${simg}`: is the singularity image/container that we will be using. We are passing the value of the variable we defined in Step 2. In our case, this is interpreted/evaluated as `/oscar/data/bnc/simgs/brownbnc/xnat-tools-v1.1.1.sif`&#x20;

`xnat2bids`: is the command to be executed, and it is followed by any necessary inputs. In this case `--help`

If the above command is successful, you'll be seeing the following output in your terminal

```bash
Usage: xnat2bids [OPTIONS] SESSION BIDS_ROOT_DIR

  Export DICOM images from an XNAT experiment to a BIDS compliant directory

Arguments:
  SESSION        XNAT Session ID, that is the Accession # for an experiment.
                 [required]
  BIDS_ROOT_DIR  Root output directory for exporting the files  [required]

Options:
  -u, --user TEXT                 XNAT User
  -p, --pass TEXT                 XNAT Password
  -h, --host TEXT                 XNAT'sURL  [default:
                                  https://xnat.bnc.brown.edu]
  -S, --session-suffix TEXT       The session_suffix is initially set to -1.
                                  This will signify an unspecified
                                  session_suffix and default to sess-01.
                                  For multi-session studies, the session label
                                  will be pulled from XNAT  [default: -1]
  -f, --bidsmap-file TEXT         Bidsmap JSON file to correct sequence names
  -i, --includeseq INTEGER        Include this sequence only, this flag can
                                  specify multiple times
  -s, --skipseq INTEGER           Exclude this sequence, can be specified
                                  multiple times
  --log-id TEXT                   ID or suffix to append to logfile. If empty,
                                  current date is used  [default:
                                  04-07-2023-10-22-56]
  -v, --verbose                   Verbose level. This flag can be specified
                                  multiple times to increase verbosity
                                  [default: 0]
  --overwrite                     Remove directories where prior results for
                                  this session/participant
  --cleanup / --no-cleanup        Remove xnat-export folder and move logs to
                                  derivatives/xnat/logs  [default: no-cleanup]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.


```

#### Running XNAT2BIDS (test only on one series)

The following command will run the executable `xnat2bids` (via singularity) command to extract DICOMs from XNAT and export to BIDS.&#x20;

```bash
singularity exec --no-home --bind ${bids_root_dir} ${simg} \
    xnat2bids ${XNAT_SESSION} ${bids_root_dir} \
    -u ${XNAT_USER} \
    -i 6
```

Once again, let's expand on the command above:

`singularity`: invokes singularity

`exec`: tells singularity we will be executing a command, in this case the command is `xnat2bids`

`${simg}`: is the singularity image/container that we will be using. We are passing the value of the variable we defined in Step 2. In our case, this is interpreted/evaluated as `/oscar/data/bnc/simgs/brownbnc/xnat-tools-v1.1.1.sif`&#x20;

`xnat2bids`: is the command to be executed, and it is followed by any necessary inputs. In this case we are passing it the positional arguments `${XNAT_SESSION}` and `${bids_root_dir}` and we are also passing the arguments `-u ${XNAT_USER}` and `-i 6`. The `-i` is asking to only process the first sequence. For a full list of inputs, please see the [xnat-tools documentation](https://brown-bnc.github.io/xnat-tools/1.0.0/xnat2bids/)

After running the command, you'll be asked to interactively type your Brown/XNAT password.

A successful run will print out the following output:

```bash
------------------------------------------------
Get project and subject information
Project: BNC_DEMODAT2
Subject ID: XNAT_S01516
Subject label: 101
Session Suffix:  01
------------------------------------------------
2026-03-24 14:52:50 node1825.oscar.ccv.brown.edu xnat_tools.bids_utils[237987] INFO Making output xnat-export session directory /users/gleblan1/xnat-exports/bnc/study-demodat2/xnat-export/sub-101/ses-01
2026-03-24 14:52:50 node1825.oscar.ccv.brown.edu xnat_tools.xnat_utils[237987] INFO ------------------------------------------------
2026-03-24 14:52:50 node1825.oscar.ccv.brown.edu xnat_tools.xnat_utils[237987] INFO Get scans.
2026-03-24 14:52:50 node1825.oscar.ccv.brown.edu xnat_tools.xnat_utils[237987] INFO ------------------------------------------------
2026-03-24 14:52:50 node1825.oscar.ccv.brown.edu xnat_tools.bids_utils[237987] INFO bids_session_dir: /users/gleblan1/xnat-exports/bnc/study-demodat2/xnat-export/sub-101/ses-01
2026-03-24 14:52:50 node1825.oscar.ccv.brown.edu xnat_tools.bids_utils[237987] INFO BIDSNAME: anat-T1w_acq-memprageRMS
2026-03-24 14:52:50 node1825.oscar.ccv.brown.edu xnat_tools.bids_utils[237987] INFO Making scan DICOM directory /users/gleblan1/xnat-exports/bnc/study-demodat2/xnat-export/sub-101/ses-01/anat-T1w_acq-memprageRMS.
2026-03-24 14:52:50 node1825.oscar.ccv.brown.edu xnat_tools.bids_utils[237987] INFO Downloading files
2026-03-24 14:52:51 node1825.oscar.ccv.brown.edu py.warnings[237987] WARNING /usr/local/lib/python3.10/site-packages/xnat_tools/bids_utils.py:471: UserWarning: Changed DICOM HEADER[ProtocolName and SeriesDescription]:             anat-t1w_acq-memprage -> anat-T1w_acq-memprageRMS             anat-t1w_acq-memprage RMS -> anat-T1w_acq-memprageRMS
2026-03-24 14:52:51 node1825.oscar.ccv.brown.edu xnat_tools.bids_utils[237987] INFO Done.
2026-03-24 14:52:51 node1825.oscar.ccv.brown.edu xnat_tools.bids_utils[237987] INFO ---------------------------------

************************
Making output BIDS Session directory /users/gleblan1/xnat-exports/bnc/study-demodat2/bids
Executing Heudiconv command: heudiconv -f reproin --bids -o /users/gleblan1 --files /users/gleblan1/xnat-exports/bnc/study-demodat2/xnat-export/sub-101/ses-01/anat-T1w_acq-memprageRMS --locator xnat-exports/bnc/study-demodat2/bids --subjects 101 --ses 01
260324-15:23:58,137 nipype.workflow INFO:
	 [Node] Setting-up "convert" in "/tmp/dcm2niixqjsr3h16/convert".
260324-15:23:58,139 nipype.workflow INFO:
	 [Node] Executing "convert" <nipype.interfaces.dcm2nii.Dcm2niix>
260324-15:23:58,274 nipype.interface INFO:
	 stdout 2026-03-24T15:23:58.273996:Chris Rorden's dcm2niiX version v1.0.20241211  (JP2:OpenJPEG) (JP-LS:CharLS) GCC8.4.0 x86-64 (64-bit Linux)
260324-15:23:58,274 nipype.interface INFO:
	 stdout 2026-03-24T15:23:58.273996:Found 1 DICOM file(s)
260324-15:23:58,274 nipype.interface INFO:
	 stdout 2026-03-24T15:23:58.273996:Convert 1 DICOM as /users/gleblan1/xnat-exports/bnc/study-demodat2/bids/sub-101/ses-01/anat/sub-101_ses-01_acq-memprageRMS_T1w_heudiconv879 (256x256x176x1)
260324-15:23:59,122 nipype.interface INFO:
	 stdout 2026-03-24T15:23:59.122845:Conversion required 0.926040 seconds (0.863915 for core code).
260324-15:23:59,142 nipype.workflow INFO:
	 [Node] Finished "convert", elapsed time 0.954788s.
260324-15:24:14,7 nipype.workflow INFO:
	 [Node] Setting-up "embedder" in "/tmp/embedmeta9_mznee6/embedder".
260324-15:24:14,11 nipype.workflow INFO:
	 [Node] Executing "embedder" <nipype.interfaces.utility.wrappers.Function>
260324-15:24:14,838 nipype.workflow INFO:
	 [Node] Finished "embedder", elapsed time 0.826124s.
Done with Heudiconv BIDS conversion.
------------------------------------------------
Get project and subject information
Project: BNC_DEMODAT2
Subject ID: XNAT_S01516
Subject label: 101
Session Suffix:  01
------------------------------------------------
```

After confirming that XNAT2BIDS is behaving as expected we will run the program on the full dataset. To do so, we invoke it as follows:

```bash
singularity exec --no-home --bind ${bids_root_dir} ${simg} \
    xnat2bids ${XNAT_SESSION} ${bids_root_dir} \
    -u ${XNAT_USER} 
```

The command above is almost identical to the one executed earlier, except we removed the line that selecteed only one run to be exported (`-i 6`) .&#x20;

### 5. Checking XNAT2BIDS results

While running `xnat2bids` singularity container in an interactive session it is important to keep the session alive throughout the run of the container. However, sometimes due to connection drops this might not always be possible. So here we provide a heuristic way of checking if `xnat2bids` ran successfully by checking the directory structure.&#x20;

#### 1. Checking logs

Upon successful completion of the `xnat2bids` pipeline, you should have 2 log files in your `${HOME}/xnat-exports/bnc/study-demodat/logs` directory - `export-<date>-<time>.log`

and `heudiconv-<date>-<time>.log`

You can check these logs for any errors or warning messages.

#### 2. Checking the file structure

If xnat2bids ran successfully, you should have 2 folders relating to the 2 steps in the pipeline `xnat-exports/` relating to downloading the data from XNAT server and `bids` relating to bidsification of the data. One easy way of checking the directory structure is to run the `tree` command -&#x20;

```bash
module load tree
tree -d ${HOME}/xnat-exports
```

Which should result in a structure similar to the output shown below:

```bash
xnat-exports/
└── bnc
    └── study-demodat2
        ├── bids
        │   ├── sourcedata
        │   │   └── sub-101
        │   │       └── ses-01
        │   │           ├── anat
        │   │           ├── dwi
        │   │           ├── fmap
        │   │           └── func
        │   │           └── mrs
        │   └── sub-101
        │       └── ses-01
        │           ├── anat
        │           ├── dwi
        │           ├── fmap
        │           └── func
        │           └── mrs
        ├── logs
        └── xnat-export
            └── sub-101
                └── ses-01
                    ├── PhoenixZIPReport
                    ├── anat-T1w_acq-memprageRMS
                    ├── anat-T1w_acq-memprageRMS_ND
                    ├── anat-T1w_acq-memprage_MPR_Cor
                    ├── anat-T1w_acq-memprage_MPR_Cor_ND
                    ├── anat-T1w_acq-memprage_MPR_Tra
                    ├── anat-T1w_acq-memprage_MPR_Tra_ND
                    ├── anat-scout_acq-aascout
                    ├── anat-scout_acq-aascoutMPRcor
                    ├── anat-scout_acq-aascoutMPRsag
                    ├── anat-scout_acq-aascoutMPRtra
                    ├── anat-scout_acq-localizer
                    ├── dwi_acq-b1500_dir-ap
                    ├── dwi_acq-b1500_dir-pa
                    ├── fmap_acq-boldGRE
                    ├── func-bold_task-checks_run-01
                    ├── func-bold_task-checks_run-01_WIP_PMU
                    ├── func-bold_task-checks_run-02
                    ├── func-bold_task-checks_run-02_WIP_PMU
                    └── func-bold_task-resting_run-01
                    └── func-bold_task-resting_run-01_WIP_PMU
                    └── mrs-mrsref_acq-PRESS_voi-Lacc
                    └── mrs-svs_acq-PRESS_voi-Lacc
```

### 6. Validate the BIDS output

After successfully running `xnat2bids` you'll need to make sure that BIDS validation passes. This process is explained in the [BIDS Validation Section](../bids-validation/)

