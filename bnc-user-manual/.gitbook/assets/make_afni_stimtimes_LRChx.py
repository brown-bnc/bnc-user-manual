## This is an example script that reads events.tsv files in BIDS format and creates the .1D stimulus timing files AFNI 
## needs for programs like 3dDeconvolve.
## The resulting .1D files are output into: BIDSDIR/derivatives/afni/sub-xx/ses-xx/stimtimes/ .

import glob
import numpy as np
import pandas as pd
import os
import argparse

## take as input bids directory, subject number, session number
parser = argparse.ArgumentParser(description='automatically convert BIDS events.tsv files to stimulus timing .1D files required by AFNI')
parser.add_argument('--subj',type=str,help='subject in sub-000 format', required=True)
parser.add_argument('--sess',type=str,help='session (string) e.g. ses-01', required=True)
parser.add_argument('--bids_dir',help='full path to top level of BIDS directory', required=True)
args = parser.parse_args()

## find all behavioral files for that subject and session
# specify the BIDS directory with the events.tsv files and the output directory in the derivatives folder
datadir = os.path.join(args.bids_dir, args.subj, args.sess, 'func')
outdir = os.path.join(args.bids_dir,'derivatives','afni',args.subj,args.sess,'stimtimes')

#create the output directory if it doesn't yet exist
if not os.path.exists(outdir):
   os.makedirs(outdir)

#look for the datafiles
datafiles = glob.glob(os.path.join(datadir, '*events.tsv'))

print('\nfound behavioral files:')
print(datafiles)

# make a list of unique task names
tasks = []
for d, datafile in enumerate(datafiles):
    tasks.append(datafiles[d].split('task-')[-1].split('_')[0])
tasks = list(set(tasks))

for task in tasks:

    # find all the events.tsv files corresponding to this particular task
    files = [i for i in datafiles if task in i]

    # read all the events.tsv files in as pandas dataframes, and concatenate
    alldataframes = []
    for r, runfile in enumerate(files):
        data_df = pd.read_csv(runfile,sep='\t', index_col=None, header=0)
        data_df['runidx'] = r
        alldataframes.append(data_df)
    alldata_df = pd.concat(alldataframes, axis=0, ignore_index=True)

    for condition in np.unique(alldata_df.trial_type):
        cond_df = alldata_df[alldata_df.trial_type==condition]
        outfilename = outdir+'/'+args.subj+'_'+task+'_' + condition+'_stimtimes.1D'
        with open(outfilename, 'w') as f:
            for runnum in np.unique(cond_df.runidx):
                onsets = cond_df[cond_df.runidx==runnum]['onset'].to_list()
                f.write(' '.join([str(item) for item in onsets]))
                f.write('\n')

    