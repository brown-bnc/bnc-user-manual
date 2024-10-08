# Step-wise via Interact Session

## 🛑 We highly recommend using the [Oscar utility script](oscar-utility-script/) instead of this older approach.

## Running XNAT2BIDS

The xnat-tools package provides a convenient `xnat2bids` script to facilitate data export and conversion to BIDS. The script is documented [here](https://brown-bnc.github.io/xnat-tools/1.0.0/xnat2bids/), and the package documentation is useful for knowing the full list of inputs and defaults. We will demonstrate how to call that script within Oscar using the BNC's demo dataset.&#x20;

### 0. Summary of commands

Before getting started, we have grouped all the commands executed in this page for your reference

```
interact -n 2 -t 01:00:00 -m 8g
version=v1.1.1
bids_root_dir=${HOME}/xnat-exports
mkdir -m 775 ${bids_root_dir} || echo "Output directory already exists"
simg=/oscar/data/bnc/simgs/brownbnc/xnat-tools-${version}.sif
XNAT_USER=${USER} 
XNAT_SESSION="XNAT_E00114"
singularity exec --no-home --bind ${bids_root_dir} \
    ${simg} \
    xnat2bids ${XNAT_SESSION} ${bids_root_dir} \
    -u ${XNAT_USER} \
    -i 7
```



### 1. Start an interactive session

#### 1.1 Desktop app on Open OnDemand&#x20;

Connecting via the Desktop app on Open OnDemand is a friendly way to request an graphical interactive session in Brown's supercomputer - Oscar. When you request a new Desktop session, you will be asked to specify the necessary resources. For this example, you can choose the basic job with `2 Cores and 7GB Memory`. Once logged in, you are already inside an interactive session.&#x20;

<figure><img src="../../.gitbook/assets/Screen Shot 2022-10-25 at 3.59.53 PM.png" alt=""><figcaption></figcaption></figure>

Once your requested session is running, you can launch it by clicking the Launch Desktop button.

<figure><img src="../../.gitbook/assets/Screen Shot 2022-10-25 at 4.37.12 PM.png" alt=""><figcaption></figcaption></figure>

At this point, simply open the terminal

![OOD Desktop app. Teal arrow points to Terminal icon to be launched](<../../.gitbook/assets/Screen Shot 2022-10-25 at 4.02.19 PM.png>)

#### 1.2 SSH&#x20;

To connect via SSH, you type `ssh username@ssh.ccv.brown.edu`. If this is your first time connecting via ssh, you will be asked to trust the remote computer (Oscar), your Brown credentials, and unless you are connected to VPN, you will be required to use DUO.

At this point you arrive at a login node. **We will need to start an interactive session/job** by typing

```
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

We recommend using the latest available version. You can get a list of the released versions [here](https://github.com/brown-bnc/xnat-tools/releases). The version specified here is likely the latest we have tested. If you test a newer version, we'd love your contributions to this documentation!

```
version=v1.1.1
```

#### &#x20;2.2 Set up paths

**BIDS Root directory**

This is the directory where data will be written. If the directory does not exist then it needs to be created.&#x20;

{% hint style="info" %}
For this sample walkthrough, you can use the path exactly as shown below. The `${USER}` variable is a systemwide variable and it is automatically interpreted as your OSCAR user. However, once you are using your own data, you should export to directories in your PI's data folder, which typically follows the pattern `/gpfs/data/<PI oscar user>`
{% endhint %}

```
bids_root_dir=${HOME}/xnat-exports
mkdir -m 775 ${bids_root_dir} || echo "Output directory already exists"
```

**Path to Singularity Image**&#x20;

This is maintained by bnc and we will be pointing to the version defined above

```
simg=/oscar/data/bnc/simgs/brownbnc/xnat-tools-${version}.sif
```

#### XNAT USER and SESSION&#x20;

Typically, your XNAT user is the same as your Brown user. Finding the session ID was explained in [an earlier section](../getting-started.md#requirements). In this example we leverage the `$USER` variable to set your XNAT user. This is possible because both oscar username and XNAT username are typically the same (i.e your Brown username). For the session, we are using the accession number for participant 005 of the demo dataset

```
XNAT_USER=${USER} #only change if oscar user doesn't match XNAT user (rare)
XNAT_SESSION="XNAT_E00114" #ACCESSION of 005 participant in sample data
```

### 3. Understanding Singularity Containers&#x20;

In the following section we will demonstrate how to run our software. Instead of directly installing the Python package `xnat-tools` we are going to run it from inside a **container**, which we have been referring to as "the singularity image/container". If you are new to containers, in a nutshell, a container allows for packaging all OS and package dependencies together so it can run in any computer. Docker containers have become very popular, you can learn a bit more about them [here](https://www.docker.com/resources/what-container). Singularity is a type of container that has specialized on running on shared HPC clusters. You can learn little more about Singularity [here](https://singularity.hpcng.org/user-docs/master/introduction.html#why-use-singularity). We referred to docker containers and singularity containers interchangeably, as they can easily be converted from one format to another.

In the specific case of `xnat-tools` , the wrapping container has `Python` , `dcm2niix` and `heudiconv` installed which are all needed by our software. The [Dockerfile](https://github.com/brown-bnc/xnat-tools/blob/master/Dockerfile) for `xnat-tools` provides some insight into how containers are built.

**Understanding the file system of a container**

Containers have their own file system, which is completely independent and isolated from the host where the container is run

{% hint style="info" %}
Because a container does not have the same directory structure as the host, we have to remember that paths like `/oscar/data/<PI>` only exist in Oscar, but not inside the container
{% endhint %}

**Sharing paths between a container and the host computer (OSCAR)**

If we want a directory/file that exists in OSCAR to be available inside our container, we need to tell Singularity that. We do so, by **binding a volume. This achieved by passing the flag `--bind <oscar_path>:<container_path>`.** If we want the path inside the container to be exactly as the path in OSCAR, we can omit the destination path, that is `--bind <oscar_path>`.

{% hint style="info" %}
The `--bind` flag can also be passed as `-B`
{% endhint %}

**Singularity default behavior when it comes to sharing paths and environment variables**

While generally speaking, a container is mostly isolated from the host, there are few exceptions. And these exceptions and default behaviors are different for Singularity and Docker. We will focus on Singularity rules here. By default Singularity binds the following locations

```
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

```
--no-home
--contain
--containall
--no-mount
```

If you see such flags in our examples and want to learn more about them visit [this doc](https://singularity.hpcng.org/user-docs/master/bind\_paths\_and\_mounts.html)

### 4. Running the executable

#### Printing the help

Let's start by making sure that we can successfully run our `xnat2bids` executable inside the container.

```
singularity exec ${simg} xnat2bids --help
```

Let's expand on the above command:

`singularity`: invokes singularity

`exec`: tells singularity we will be executing a command, in this case the command is `xnat2bids`

`${simg}`: is the singularity image/container that we will be using. We are passing the value of the variable we defined in Step 2. In our case, this is interpreted/evaluated as `/oscar/data/bnc/simgs/brownbnc/xnat-tools-v1.1.1.sif`&#x20;

`xnat2bids`: is the command to be executed, and it is followed by any necessary inputs. In this case `--help`

If the above command is successful, you'll be seeing the following output in your terminal

```
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

```
singularity exec --no-home --bind ${bids_root_dir} ${simg} \
    xnat2bids ${XNAT_SESSION} ${bids_root_dir} \
    -u ${XNAT_USER} \
    -i 7
```

Once again, let's expand on the command above:

`singularity`: invokes singularity

`exec`: tells singularity we will be executing a command, in this case the command is `xnat2bids`

`${simg}`: is the singularity image/container that we will be using. We are passing the value of the variable we defined in Step 2. In our case, this is interpreted/evaluated as `/oscar/data/bnc/simgs/brownbnc/xnat-tools-v1.1.1.sif`&#x20;

`xnat2bids`: is the command to be executed, and it is followed by any necessary inputs. In this case we are passing it the positional arguments `${XNAT_SESSION}` and `${bids_root_dir}` and we are also passing the arguments `-u ${XNAT_USER}` and `-i 7`. The `-i` is asking to only process the first sequence. For a full list of inputs, please see the  [xnat-tools documentation](https://brown-bnc.github.io/xnat-tools/1.0.0/xnat2bids/)

After running the command, you'll be asked to interactively type your Brown/XNAT password.

A successful run will print out the following output:

```
------------------------------------------------
Get project and subject information
Project: BNC_DEMODAT
Subject ID: XNAT_S00111
Session Suffix:  SESSION1
Subject label: 005
------------------------------------------------
2023-04-10 13:45:51 node1147.oscar.ccv.brown.edu xnat_tools.bids_utils[151813] INFO Making output xnat-export session directory /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/xnat-export/sub-005/ses-session1
2023-04-10 13:45:51 node1147.oscar.ccv.brown.edu xnat_tools.xnat_utils[151813] INFO ------------------------------------------------
2023-04-10 13:45:51 node1147.oscar.ccv.brown.edu xnat_tools.xnat_utils[151813] INFO Get scans.
2023-04-10 13:45:51 node1147.oscar.ccv.brown.edu xnat_tools.xnat_utils[151813] INFO ------------------------------------------------
2023-04-10 13:45:53 node1147.oscar.ccv.brown.edu xnat_tools.bids_utils[151813] INFO bids_session_dir: /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/xnat-export/sub-005/ses-session1
2023-04-10 13:45:53 node1147.oscar.ccv.brown.edu xnat_tools.bids_utils[151813] INFO BIDSNAME: anat-T1w_acq-memprageRMS
2023-04-10 13:45:53 node1147.oscar.ccv.brown.edu xnat_tools.bids_utils[151813] INFO Making scan DICOM directory /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/xnat-export/sub-005/ses-session1/anat-T1w_acq-memprageRMS.
2023-04-10 13:45:55 node1147.oscar.ccv.brown.edu xnat_tools.bids_utils[151813] INFO Downloading files
2023-04-10 13:45:55 node1147.oscar.ccv.brown.edu py.warnings[151813] WARNING /usr/local/lib/python3.10/site-packages/xnat_tools/bids_utils.py:324: UserWarning: Changed DICOM HEADER[ProtocolName and SeriesDescription]:             anat-t1w_acq-memprage -> anat-T1w_acq-memprageRMS             anat-t1w_acq-memprage RMS -> anat-T1w_acq-memprageRMS                                                                                                                                                                        
  warnings.warn(                                                                                                                                                           

2023-04-10 13:47:24 node1147.oscar.ccv.brown.edu xnat_tools.bids_utils[151813] INFO Done.
2023-04-10 13:47:24 node1147.oscar.ccv.brown.edu xnat_tools.bids_utils[151813] INFO ---------------------------------
************************
Making output BIDS Session directory /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids
Executing Heudiconv command: heudiconv -f reproin --bids     -o /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids     --dicom_dir_template /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/xnat-export/sub-{subject}/ses-{session}/*/*.dcm     --subjects 005 --ses session1
INFO: Running heudiconv version 0.11.6 latest 0.12.2
INFO: Need to process 1 study sessions
INFO: PROCESSING STARTS: {'subject': '005', 'outdir': '/oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids/', 'session': 'session1'}
INFO: Processing 176 dicoms
INFO: Analyzing 176 dicoms
INFO: Filtering out 0 dicoms based on their filename
INFO: Generated sequence info for 1 studies with 176 entries total
INFO: Processing 1 seqinfo entries
INFO: Doing conversion using dcm2niix
INFO: Converting /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprageRMS_T1w (176 DICOMs) -> /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids/sub-005/ses-session1/anat . Converter: dcm2niix . Output types: ('nii.gz', 'dicom')
230410-13:47:25,907 nipype.workflow INFO:
         [Node] Setting-up "convert" in "/tmp/dcm2niixwwgutois/convert".
INFO: [Node] Setting-up "convert" in "/tmp/dcm2niixwwgutois/convert".
230410-13:47:25,950 nipype.workflow INFO:
         [Node] Executing "convert" <nipype.interfaces.dcm2nii.Dcm2niix>
INFO: [Node] Executing "convert" <nipype.interfaces.dcm2nii.Dcm2niix>
230410-13:47:26,127 nipype.interface INFO:
         stdout 2023-04-10T13:47:26.127796:Compression will be faster with 'pigz' installed
INFO: stdout 2023-04-10T13:47:26.127796:Compression will be faster with 'pigz' installed
230410-13:47:26,127 nipype.interface INFO:
         stdout 2023-04-10T13:47:26.127796:Chris Rorden's dcm2niiX version v1.0.20190902  (JP2:OpenJPEG) (JP-LS:CharLS) GCC5.5.0 (64-bit Linux)
INFO: stdout 2023-04-10T13:47:26.127796:Chris Rorden's dcm2niiX version v1.0.20190902  (JP2:OpenJPEG) (JP-LS:CharLS) GCC5.5.0 (64-bit Linux)
230410-13:47:26,127 nipype.interface INFO:
         stdout 2023-04-10T13:47:26.127796:Found 176 DICOM file(s)
INFO: stdout 2023-04-10T13:47:26.127796:Found 176 DICOM file(s)
230410-13:47:26,128 nipype.interface INFO:
         stdout 2023-04-10T13:47:26.127796:Convert 176 DICOM as /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprageRMS_T1w_heudiconv918 (256x256x176x1)
INFO: stdout 2023-04-10T13:47:26.127796:Convert 176 DICOM as /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprageRMS_T1w_heudiconv918 (256x256x176x1)
230410-13:47:27,158 nipype.interface INFO:
         stdout 2023-04-10T13:47:27.158623:Conversion required 1.140682 seconds (1.140108 for core code).
INFO: stdout 2023-04-10T13:47:27.158623:Conversion required 1.140682 seconds (1.140108 for core code).
230410-13:47:27,174 nipype.workflow INFO:
         [Node] Finished "convert", elapsed time 1.166935s.
INFO: [Node] Finished "convert", elapsed time 1.166935s.
WARNING: Failed to find task field in /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprageRMS_T1w.json.
230410-13:47:37,646 nipype.workflow INFO:
         [Node] Setting-up "embedder" in "/tmp/embedmeta9qnhxt9z/embedder".
INFO: [Node] Setting-up "embedder" in "/tmp/embedmeta9qnhxt9z/embedder".
230410-13:47:37,659 nipype.workflow INFO:
         [Node] Executing "embedder" <nipype.interfaces.utility.wrappers.Function>
INFO: [Node] Executing "embedder" <nipype.interfaces.utility.wrappers.Function>
230410-13:47:40,993 nipype.workflow INFO:
         [Node] Finished "embedder", elapsed time 3.333115s.
INFO: [Node] Finished "embedder", elapsed time 3.333115s.
INFO: Post-treating /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids/sub-005/ses-session1/anat/sub-005_ses-session1_acq-memprageRMS_T1w.json file
INFO: Adding "IntendedFor" to the fieldmaps in /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids/sub-005/ses-session1.
WARNING: We cannot add the IntendedFor field: no fmap/ in /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids/sub-005/ses-session1
INFO: Populating template files under /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids/
INFO: PROCESSING DONE: {'subject': '005', 'outdir': '/oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids/', 'session': 'session1'}
Done with Heudiconv BIDS Convesion.
2023-04-10 13:47:41 node1147.oscar.ccv.brown.edu xnat_tools.bids_postprocess[151813] INFO ---------------------------------
2023-04-10 13:47:41 node1147.oscar.ccv.brown.edu xnat_tools.bids_postprocess[151813] INFO Processing Subjects ['005']: 
2023-04-10 13:47:41 node1147.oscar.ccv.brown.edu xnat_tools.bids_postprocess[151813] INFO ---------------------------------
2023-04-10 13:47:41 node1147.oscar.ccv.brown.edu xnat_tools.bids_postprocess[151813] INFO ---------------------------------
2023-04-10 13:47:41 node1147.oscar.ccv.brown.edu xnat_tools.bids_postprocess[151813] INFO Processing Sessions ['session1']: 
2023-04-10 13:47:41 node1147.oscar.ccv.brown.edu xnat_tools.bids_postprocess[151813] INFO ---------------------------------
2023-04-10 13:47:41 node1147.oscar.ccv.brown.edu xnat_tools.bids_utils[151813] INFO Processing participant 005 at path /oscar/data/<group>/<user>/xnat-exports/bnc/study-demodat/bids/sub-005
2023-04-10 13:47:41 node1147.oscar.ccv.brown.edu xnat_tools.bids_utils[151813] INFO List of sessions sub-directories ['session1']
```

After confirming that XNAT2BIDS is behaving as expected we will run the program on the full dataset. To do so, we invoke it as follows:

```
singularity exec --no-home --bind ${bids_root_dir} ${simg} \
    xnat2bids ${XNAT_SESSION} ${bids_root_dir} \
    -u ${XNAT_USER} \
    -s 6
```

The command above is almost identical to the one executed earlier, the only new argument is `-s 6` . In this instance we are running `xnat2bids` on all scan sequences, except series 6. Series 6 corresponds to the individual echoes of a multi-echo MPRAGE and it's typically not used in BIDS apps. We only export the RMS of the echos (#7). We explain this a bit more in the [BIDS Ready Protocols](../../xnat/bids-compliant-protocols.md#important-considerations) section. After successful execution, near the bottom of your log should be the line:

```
INFO: PROCESSING DONE: {'subject': '001', 'outdir': '/users/<your-user>/xnat-exports/bnc/study-demodat/bids/', 'session': '01'}
```

### 5. Checking XNAT2BIDS results

While running `xnat2bids` singularity container in an interactive session it is important to keep the session alive throughout the run of the container. However, sometimes due to connection drops this might not always be possible. So here we provide a heuristic way of checking if `xnat2bids` ran successfully by checking the directory structure.&#x20;

#### 1. Checking logs

Upon successful completion of the `xnat2bids` pipeline, you should have 2 log files in your `${HOME}/xnat-exports/bnc/study-demodat/logs` directory - `export-<date>-<time>.log`

and `heudiconv-<date>-<time>.log`

You can check these logs for any errors or warning messages.

#### 2. Checking the file structure

If xnat2bids ran successfully, you should have 2 folders relating to the 2 steps in the pipeline `xnat-exports/` relating to downloading the data from XNAT server and `bids` relating to bidsification of the data. One easy way of checking the directory structure is to run the `tree` command -&#x20;

```
module load tree/2.0.2
tree -d ${HOME}/xnat-exports
```

Which should result in a structure similar to the output shown below:

```
xnat-exports/
└── bnc
    └── study-demodat
        ├── bids
        │   ├── sourcedata
        │   │   └── sub-001
        │   │       └── ses-01
        │   │           ├── anat
        │   │           ├── dwi
        │   │           ├── fmap
        │   │           └── func
        │   └── sub-001
        │       └── ses-01
        │           ├── anat
        │           ├── dwi
        │           ├── fmap
        │           └── func
        ├── logs
        └── xnat-export
            └── sub-001
                └── ses-01
                    ├── anat-scout_acq-aascout
                    ├── anat-scout_acq-aascoutMPRcor
                    ├── anat-scout_acq-aascoutMPRsag
                    ├── anat-scout_acq-aascoutMPRtra
                    ├── anat-scout_acq-localizer
                    ├── anat-T1w_acq-memprageRMS
                    ├── dwi_acq-b1500_dir-ap
                    ├── dwi_acq-b1500_dir-ap_SBRef
                    ├── dwi_acq-b1500_dir-pa
                    ├── dwi_acq-b1500_dir-pa_SBRef
                    ├── fmap_acq-boldGRE
                    ├── fmap_acq-boldSE_dir-ap
                    ├── fmap_acq-boldSE_dir-pa
                    ├── fmap_acq-diffSE_dir-ap
                    ├── fmap_acq-diffSE_dir-pa
                    ├── func-bold_task-checks_run-01
                    ├── func-bold_task-checks_run-02
                    ├── func-bold_task-motionloc
                    ├── func-bold_task-resting
                    └── func-bold_task-ssrt
```

### 6. Validate the BIDS output

After successfully running `xnat2bids` you'll need to make sure that BIDS validation passes. This process is explained in the [BIDS Validation Section](../bids-validation/)
