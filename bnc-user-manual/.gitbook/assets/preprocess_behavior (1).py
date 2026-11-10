import glob
import numpy as np
import pandas as pd
import os
import argparse
import warnings

#############################################################################################
########### Convert Psychopy CSV -> BIDS TSV (per session, skip if exists) ##################
#############################################################################################

def convert_csv_to_tsv(subj, bids_dir):
    sessions = ['ses-01', 'ses-02']
    checkHemiDur = 12  # seconds per hemifield block

    for sess in sessions:
        datadir = os.path.join(bids_dir, 'sourcedata', subj, sess, 'beh')
        outdir = os.path.join(bids_dir, subj, sess, 'func')
        os.makedirs(outdir, exist_ok=True)

        datafiles = glob.glob(os.path.join(datadir, '*Checks*csv'))
        if not datafiles:
            print(f"[{subj} {sess}] No *Checks*csv files found, skipping.")
            continue

        print(f"\n[{subj} {sess}] Found behavioral files:")
        print(datafiles)

        # Loop through files
        for fnum, datafile in enumerate(datafiles):
            df = pd.read_csv(datafile, header=0)

            # --- Checkerboard task ---
            outfilename_checks = os.path.join(outdir, f'{subj}_{sess}_task-checks_run-0{fnum+1}_events.tsv')
            if not os.path.exists(outfilename_checks):
                left_onsets = df["LeftBlockStart"].dropna().values
                right_onsets = df["RightBlockStart"].dropna().values

                left_df = pd.DataFrame({'onset': left_onsets, 'duration': checkHemiDur, 'trial_type': 'left'})
                right_df = pd.DataFrame({'onset': right_onsets, 'duration': checkHemiDur, 'trial_type': 'right'})
                checks_events_df = pd.concat([left_df, right_df]).sort_values('onset')
                checks_events_df['response_time'] = 'n/a'
                checks_events_df['stim_file'] = 'n/a'

                checks_events_df.to_csv(outfilename_checks, sep="\t", index=False)
                print(f"  created {outfilename_checks}")
            else:
                print(f"  skipping (exists) {outfilename_checks}")

            # --- Keypress task ---
            outfilename_event = os.path.join(outdir, f'{subj}_{sess}_task-keypress_run-0{fnum+1}_events.tsv')
            if not os.path.exists(outfilename_event):
                event_onsets = df['keyrespTime'].dropna().values
                trial_types = df['response'].dropna().map(
                    lambda x: 'right' if x == '2' else ('left' if x in ['y', 'Y'] else 'n/a')
                )
                event_df = pd.DataFrame({'onset': event_onsets, 'duration': 0, 'trial_type': trial_types})
                event_df.to_csv(outfilename_event, sep="\t", index=False)
                print(f"  created {outfilename_event}")
            else:
                print(f"  skipping (exists) {outfilename_event}")


#############################################################################################
######################### Convert BIDS TSV -> AFNI stimtimes (1D) ###########################
######################## Combine ses-01 and ses-02 for each subject #########################
#############################################################################################

def convert_tsv_to_afni(subj, bids_dir):
    ses_dirs = [
        os.path.join(bids_dir, subj, 'ses-01', 'func'),
        os.path.join(bids_dir, subj, 'ses-02', 'func')
    ]

    outdir = os.path.join(bids_dir, 'derivatives', 'afni', subj, 'dualsession', 'stimtimes')
    os.makedirs(outdir, exist_ok=True)

    datafiles = []
    for ses_dir in ses_dirs:
        datafiles.extend(glob.glob(os.path.join(ses_dir, '*events.tsv')))

    if not datafiles:
        print(f"[{subj}] No events.tsv files found, skipping AFNI conversion.")
        return

    print(f"\n[{subj}] Found {len(datafiles)} events.tsv files.")

    # Extract unique tasks
    tasks = sorted(list(set([
        os.path.basename(f).split('task-')[-1].split('_')[0]
        for f in datafiles
    ])))

    print(f"[{subj}] Tasks found: {tasks}")

    for task in tasks:
        alldataframes = []
        for runidx, runfile in enumerate(sorted([f for f in datafiles if f'task-{task}_' in f])):
            df = pd.read_csv(runfile, sep='\t')
            df['runidx'] = runidx
            alldataframes.append(df)

        alldata_df = pd.concat(alldataframes, ignore_index=True)

        for condition in sorted(alldata_df['trial_type'].dropna().unique()):
            cond_df = alldata_df[alldata_df.trial_type == condition]
            outfilename = os.path.join(outdir, f'{subj}_{task}_{condition}_dualsession_stimtimes.1D')

            with open(outfilename, 'w') as f:
                for runnum in range(4):  # assumes 4 runs across 2 sessions
                    run_onsets = cond_df[cond_df.runidx == runnum]['onset'].tolist()
                    line = ' '.join([str(onset) for onset in run_onsets]) if run_onsets else '*'
                    f.write(line + '\n')

            print(f"  saved {outfilename}")


#############################################################################################
########################### MAIN: Run the functions #########################################
#############################################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PsychoPy CSV - BIDS TSV - AFNI stimtimes")
    parser.add_argument("--subj", type=str, required=True, help="Subject ID (e.g. sub-001)")
    parser.add_argument("--bids_dir", type=str, required=True, help="Path to BIDS directory")
    args = parser.parse_args()

    subj = args.subj
    bids_dir = args.bids_dir

    print(f"\n=== Processing {subj} ===")

    convert_csv_to_tsv(subj, bids_dir)
    convert_tsv_to_afni(subj, bids_dir)

    print(f"\n=== Done with {subj} ===")
