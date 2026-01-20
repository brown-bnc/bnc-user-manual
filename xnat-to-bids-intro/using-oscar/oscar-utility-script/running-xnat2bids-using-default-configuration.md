# Running xnat2bids using default configuration

First, we need to load a module that will give us access to python and a few basic packages. From the command line, run the following:

```
module load anaconda3
```

Then, if the default values for resource allocation are suitable and you do not need to pass any specific arguments to `xnat2bids`, you may run the script as follows:

```
python /oscar/data/bnc/scripts/run_xnat2bids.py
```

Since, by default, no sessions are flagged for processing, you will immediately be prompted to enter a Session ID to proceed.  If you would like to process multiple sessions simultaneously, you can enter them as a comma-separated list.  Here's an example:

```
Enter Session(s) (comma separated): XNAT_E00080, XNAT_E00114, XNAT_E00152
```

After your jobs have completed, you can find all DICOM export and BIDS output data at the following location: `/oscar/home/<your_username>/bids-export/`

Likewise, logs can be found at `/oscar/scratch/<your_username>/logs/` under the following format: `xnat2bids-<session-id>-<array-job-id>.txt`

To change these output locations or take advantage of additional xnat2bids features, you'll need to [create a custom configuration file](running-xnat2bids-with-a-custom-configuration.md).

{% hint style="warning" %}
As of January 2026 (and depending on which modules you already have loaded), loading the anaconda3 module can interfere with other modules like vscode. If you have trouble, load the anaconda3 module immediately before launching the run\_xnat2bids.py script, and open a new terminal once your job is off and running.
{% endhint %}
