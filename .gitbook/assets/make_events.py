## This is an example script that converts behavioral data from psychopy into the events.tsv format required by BIDS
## this script expects to find csv files for the DEMODAT visual hemifield localizer (LRChx) and motion localizer (motionloc)
## in a behavioral folder within the BIDS source directory: BIDSDIR/sourcedata/beh/ .
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
datafiles = glob.glob(os.path.join(datadir, '*csv'))

print('\nfound behavioral files:')
print(datafiles)

# throw a warning if we find any behavioral data that doesn't come from one of these two tasks
for datafile in datafiles:
    if 'LRChx' not in datafile and 'motionloc' not in datafile:
        warnings.warn("Warning: task not recognized for file " + datafile)

################################
## Visual hemifield localizer ##
################################

# the checkerboard was shown in alternating blocks of 12s per hemifield
checkHemiDur = 12 

checksfiles = glob.glob(os.path.join(datadir, '*LRChx*csv'))

# if the participant completed multiple runs of a given task, we need to be sure to 
# add the 'run-xx' parameter to the filename
if len(checksfiles)>1:
    multirun = True
else:
    multirun = False

for fnum,datafile in enumerate(checksfiles):
    df = pd.read_csv(datafile,header=0)

    if multirun:
        outfilename = outdir + '/' + args.subj + '_' + args.sess + '_task-checks_run-0' + str(fnum+1) + '_events.tsv' 
    else:
        outfilename = outdir + '/' + args.subj + '_' + args.sess + '_task-checks_events.tsv' 

    # first identify the start times for all the left hemifield checkerboard blocks
    left_onsets = np.round((df['leftBlockStartTime'][df['Block_Loop.thisRepN'].notnull()]).to_numpy(),2)
    left_df = pd.DataFrame(left_onsets,columns=['onset'])
    left_df['duration']=checkHemiDur
    left_df['trial_type']='left'

    # then do the same for all the right hemifield checkerboard blocks
    right_onsets = np.round((df['rightBlockStartTime'][df['Block_Loop.thisRepN'].notnull()]).to_numpy(),2)
    right_df = pd.DataFrame(right_onsets,columns=['onset'])
    right_df['duration']=checkHemiDur
    right_df['trial_type']='right'

    # concatenate the left and right hemifield onsets and sort them in ascending order
    checks_events_df = pd.concat([left_df,right_df]).sort_values('onset')

    # we don't have any response data for this task, but normally you would include this information
    checks_events_df['response_time']='n/a'
    checks_events_df['stim_file']='n/a'

    #save out our new events.tsv file
    checks_events_df.to_csv(outfilename, sep="\t",index=False)
    print('\ncreated file: ' + outfilename)


######################
## Motion localizer ##
######################

#each block (static, flicker, moving) is 15s
motBlockDur = 15 
#each individual motion direction is 1s
motCondDur = 1 

motfiles = glob.glob(os.path.join(datadir, '*motionloc*csv'))

# if the participant completed multiple runs of a given task, we need to be sure to 
# add the 'run-xx' parameter to the filename
if len(motfiles)>1:
    multirun = True
else:
    multirun = False

for fnum,datafile in enumerate(motfiles):
    df = pd.read_csv(datafile,header=0)

    if multirun:
        outfilename = outdir + '/' + args.subj + '_' + args.sess + '_task-motionloc_run-0' + str(fnum+1) + '_events.tsv' 
    else:
        outfilename = outdir + '/' + args.subj + '_' + args.sess + '_task-motionloc_events.tsv' 

    # PsychoPy saves out stimulus times relative to the start of the experimental script, so we need to 
    # calculate the time the trigger was received from the scanner and save out our stimulus times relative 
    # to that reference
    triggerTime = df['trigger_signal.started'][0] + df['trigger_signal.rt'][0]

    # first identify the onsets of the blocks with static dots
    static_onsets = (df['Static_Fix.started'][df['Static_Loop.thisTrialN']==0]-triggerTime).round(3).to_numpy()
    static_df = pd.DataFrame(static_onsets,columns=['onset'])
    static_df['duration']=motBlockDur
    static_df['trial_type']='static'

    # then identify the onsets of the blocks with moving dots
    moving_onsets = (df['Moving_Fix.started'][df['Moving_Loop.thisTrialN']==0]-triggerTime).round(3).to_numpy()
    moving_df = pd.DataFrame(moving_onsets,columns=['onset'])
    moving_df['duration']=motBlockDur
    moving_df['trial_type']='moving'    

    # then identify the onsets of the blocks with flickering dots
    flicker_onsets = (df['Flicker_Fix.started'][df['Flicker_Loop.thisTrialN']==0]-triggerTime).round(3).to_numpy()
    flicker_df = pd.DataFrame(flicker_onsets,columns=['onset'])
    flicker_df['duration']=motBlockDur
    flicker_df['trial_type']='flicker'

    # also add onsets for individual motion directions, in case we want to model that later
    motdir_onsets = (df['Moving_Fix.started'][df['moving_rep']==1]-triggerTime).round(3).to_numpy()
    motdir_df = pd.DataFrame(motdir_onsets,columns=['onset'])
    motdir_df['duration']=motCondDur
    motdir_df['trial_type']=df['dotdir'][df['moving_rep']==1].to_numpy()

    # concatenate all the onsets into a single dataframe, again adding a column for response time 
    # even though we don't have it in this dataset
    motloc_events_df = pd.concat([static_df,moving_df, flicker_df, motdir_df]).sort_values('onset')
    motloc_events_df['response_time']='n/a'
    motloc_events_df['stim_file']='n/a'

    # save our new events.tsv file
    motloc_events_df.to_csv(outfilename, sep="\t",index=False)
    print('\ncreated file: ' + outfilename)