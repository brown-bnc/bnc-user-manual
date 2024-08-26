# Syncing your XNAT project & Oscar data directory

This feature automates the export process by analyzing the existing projects in your data directory along with their associated subjects and sessions, and then identifies and fetches missing sessions that exist remotely on XNAT. The script will check the insertion date and time for every session in your  XNAT project. If you have data on XNAT that is newer than the sessions in your project directory on Oscar, we can assume that the XNAT data needs to be pulled over to Oscar.

### Diff: Identify data on XNAT that is not yet on Oscar&#x20;

To get a report of any project data on XNAT that is not present in your data directory, use the `--diff` flag alongside the path to the root of your BIDS directory. This option will only produce a report, not perform the sync.

If you are passing in a configuration file where bids\_root is defined, or if your data directory is `~/bids-export`, there is no need to pass `<BIDS_ROOT>` as an argument alongside `--diff.` &#x20;

```
python /oscar/data/bnc/scripts/run_xnat2bids.py --diff <BIDS_ROOT> 
```

### Sync: export new XNAT data to a project on Oscar

To sync your data directory, use `--update` alongside the path to the root of your BIDS directory.

If you are passing in a configuration file where bids\_root is defined, or if your data directory is `~/bids-export`, there is no need to pass `<BIDS_ROOT>` as an argument alongside `--update.` &#x20;

```
python /oscar/data/bnc/scripts/run_xnat2bids.py --update <BIDS_ROOT> 
```

***

**NOTE:** If you manually add resources or scan data to your project, XNAT will not automatically update the insertion date/time, so it will not be identified as new data that needs to be synced. If you would like to use the "sync" functionality on manually added data, you will need to update the date field in XNAT for the given session that you want to sync.&#x20;

To do this:

1. Open XNAT and navigate to the session page you would like to sync
2. Select Edit from the Actions panel&#x20;

<figure><img src="../../../.gitbook/assets/Screenshot 2023-09-21 at 2.57.07 PM (1).png" alt=""><figcaption></figcaption></figure>

3. Update the "Date" field to the current date, or the date of manual change.&#x20;

<figure><img src="../../../.gitbook/assets/Screenshot 2023-09-21 at 2.57.23 PM.png" alt=""><figcaption></figcaption></figure>

4. Select "Submit" at the bottom of the page.&#x20;
