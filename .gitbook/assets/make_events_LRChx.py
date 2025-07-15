## This is an example script that converts behavioral data from psychopy into the events.tsv format required by BIDS
## this script expects to find csv files for the DEMODAT2 visual hemifield localizer (LRChx)
## in a behavioral folder within the BIDS source directory: BIDSDIR/sourcedata/sub-xxx/ses-xx/beh/ 
## The resulting events.tsv files are output into: BIDSDIR/sub-xx/ses-xx/func/ .

import glob
import numpy as np
import pandas as pd
import os
import argparse
import warnings

## take as input base directory, subject number, session number
parser = argparse.ArgumentParser(description='automatically convert DEMODAT PsychoPy behavioral files to BIDS events.tsv files')
parser.add_argument('--subj',type=str,help='subject in sub-000 format', required=True)
parser.add_argument('--sess',type=str,help='session (string) e.g. ses-01', required=True)
parser.add_argument('--bids_dir',help='full path to top level of BIDS directory', required=True)
args = parser.parse_args()

## find all behavioral files for that subject and session
datadir = os.path.join(args.bids_dir,'sourcedata',args.subj, args.sess, 'beh')
outdir = os.path.join(args.bids_dir, args.subj, args.sess, 'func')
datafiles = glob.glob(os.path.join(datadir, '*Checks*csv'))

print('\nfound behavioral files:')
print(datafiles)

# throw a warning if we find any behavioral data that doesn't come from one of these two tasks
for datafile in datafiles:
    if 'Checks' not in datafile:
        warnings.warn("Warning: task not recognized for file " + datafile)

################################
## Visual hemifield localizer ##
################################

# the checkerboard was shown in alternating blocks of 12s per hemifield
checkHemiDur = 12 

for fnum,datafile in enumerate(datafiles):
    df = pd.read_csv(datafile,header=0)

    #debugging: list columns to make sure the needed ones are being read (so as not to get a key error)
    print(f"\nColumns in {datafile}:")
    print(df.columns.tolist())

    outfilename_checks = os.path.join(outdir, f'{args.subj}_{args.sess}_task-checks_run-0{fnum+1}_events.tsv')
    
    # first identify the start times for all the left hemifield checkerboard blocks
    left_onsets = df["LeftBlockStart"].dropna().values
    left_df = pd.DataFrame({'onset': left_onsets, 'duration': checkHemiDur, 'trial_type': 'left'})

    # then do the same for all the right hemifield checkerboard blocks
    right_onsets = df['RightBlockStart'].dropna().values
    right_df = pd.DataFrame({'onset': right_onsets, 'duration': checkHemiDur, 'trial_type': 'right'})

    # concatenate the left and right hemifield onsets and sort them in ascending order
    checks_events_df = pd.concat([left_df, right_df]).sort_values('onset')
    checks_events_df['response_time'] = 'n/a'
    checks_events_df['stim_file'] = 'n/a'
    
    #save out our new events.tsv file
    checks_events_df.to_csv(outfilename_checks, sep="\t", index=False)
    print('\ncreated file: ' + outfilename_checks)

###################################
## Event-Related Task: Key Press ##
###################################

for fnum, datafile in enumerate(datafiles):
    df = pd.read_csv(datafile, header=0)
    
    outfilename_event = os.path.join(outdir, f'{args.subj}_{args.sess}_task-keypress_run-0{fnum+1}_events.tsv')
    
    # Extract keypress response times and map responses
    event_onsets = df['keyrespTime'].dropna().values
    trial_types = df['response'].dropna().map(lambda x: 'right' if x == '2' else ('left' if x in ['y', 'Y'] else 'n/a'))
    
    event_df = pd.DataFrame({'onset': event_onsets, 'duration': 0, 'trial_type': trial_types})
    
    event_df.to_csv(outfilename_event, sep="\t", index=False)
    print('\ncreated file: ' + outfilename_event)
