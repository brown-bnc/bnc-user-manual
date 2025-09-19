---
hidden: true
---

# WIP Second-Level Analysis using gen\_group\_command.py

## Use gen\_group\_command.py to build your statistical tests and run the group analysis

Similar to how afniproc.py generates a processing script per subject, afni's [gen\_group\_command.py](https://afni.nimh.nih.gov/pub/dist/doc/program_help/gen_group_command.py.html) generates group analyses scripts. We will be using this meta-script to write two variations of group analysis: one using the afni command `3dttest++`, and one with `3dMEMA`.&#x20;

### 3dttest++

[3dttest++](https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dttest++.html) is an afni command that &#x20;

{% code title="gen_group_command_3dttest.sh" %}
```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -c 8
#SBATCH --mem=10G
#SBATCH --time 1:00:00
#SBATCH -J gen_group_command_3dttest
#SBATCH --output=logs/gen_group_command_3dttest-%A_%a.out
#SBATCH --mail-user example_user@brown.edu 
#SBATCH --mail-type ALL

# To run this, type on the terminal: sbatch gen_group_command_3dttest.sh

##########################################################################################################
########################### Create Group Results and Log Directories ###############################################
##########################################################################################################

bidsdir=/path/to/bids # <--- FILL THIS IN
outdir=$bidsdir/derivatives/afni/groupresults
mkdir -p "$outdir"

echo "Creating group results directory at $outdir"

while read subID; do
    src=$bidsdir/derivatives/afni/${subID}/dualsession/${subID}.dualsession.results/stats.${subID}_dualsession_REML+tlrc.HEAD
    src_brik=${src%.HEAD}.BRIK

    if [[ -f "$src" && -f "$src_brik" ]]; then
        cp "$src" "$src_brik" "$outdir/"
        echo "Copied stats for $subID"
    else
        echo "Missing REML stats for $subID"
    fi
done < subjects.txt

logdir=$bidsdir/derivatives/afni/scripts/logs
mkdir -p $logdir

echo "Creating log directory at $logdir"

cd $outdir

##########################################################################################################
####################### Run Group Statistics with 3dttest++ ##############################################
##########################################################################################################

# Run 3dttest++ for the checks task
gen_group_command.py \
    -command 3dttest++ \
    -write_script cmd.ttest.checks  \
    -dsets $outdir/*REML*.HEAD  \
    -subs_betas "left_vs_right_chx#0_Coef" \
    -subs_tstats "left_vs_right_chx#0_Tstat" \
    -prefix ttest_group_checks_LR

tcsh -xef cmd.ttest.checks |& tee $logdir/output.ttest.checks.log

# Run 3dttest++ for the keypress task
gen_group_command.py \
    -command 3dttest++ \
    -write_script cmd.ttest.keypress  \
    -dsets $outdir/*REML*.HEAD  \
    -subs_betas "left_vs_right_press#0_Coef" \
    -subs_tstats "left_vs_right_press#0_Tstat" \
    -prefix ttest_group_keypress_LR

tcsh -xef cmd.ttest.keypress |& tee $logdir/output.ttest.keypress.log

```
{% endcode %}

#### View the Output

### 3dMEMA

AFNI's 3dMEMA performs a "mixed effects meta analysis", which, based on your experimental design, could take the form of t-tests, ANOVAs, ANCOVAs, and more. For this dataset, we will be doing a single-sample test (The input to 3dMEMA is one beta coefficient per subject, taken from the REML statistical file which was output from afniproc.py). 3dMEMA differs from 3dttest++  in that it accounts for variability within and across subjects. &#x20;

{% hint style="info" %}
3dMEMA requires R.&#x20;
{% endhint %}

{% code title="gen_group_command_3dMEMA.sh" %}
```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -c 8
#SBATCH --mem=10G
#SBATCH --time 1:00:00
#SBATCH -J gen_group_command_3dMEMA
#SBATCH --output=logs/gen_group_command_3dMEMA-%A_%a.out
#SBATCH --mail-user example_user@brown.edu 
#SBATCH --mail-type ALL

# To run this, type on the terminal: sbatch gen_group_command_3dMEMA.sh

##########################################################################################################
########################### Create Group Results and Log Directories ###############################################
##########################################################################################################

bidsdir=/path/to/bids # <--- FILL THIS IN
outdir=$bidsdir/derivatives/afni/groupresults
mkdir -p "$outdir"

echo "Creating group results directory at $outdir"

while read subID; do
    src=$bidsdir/derivatives/afni/${subID}/dualsession/${subID}.dualsession.results/stats.${subID}_dualsession_REML+tlrc.HEAD
    src_brik=${src%.HEAD}.BRIK

    if [[ -f "$src" && -f "$src_brik" ]]; then
        cp "$src" "$src_brik" "$outdir/"
        echo "Copied stats for $subID"
    else
        echo "Missing REML stats for $subID"
    fi
done < subjects.txt

logdir=$bidsdir/derivatives/afni/scripts/logs
mkdir -p $logdir

echo "Creating log directory at $logdir"

cd $outdir

##########################################################################################################
####################### Run Group Statistics with 3dMEMA #################################################
##########################################################################################################

# Allow AFNI to use system R instead of internal R_io.so
export AFNI_ALLOW_SYSTEM_R=YES

echo "AFNI 3dMEMA requires R to run. Searching for R installation:"
echo "Rscript: $(which Rscript)"

# Run 3dMEMA for the checks task
gen_group_command.py \
    -command 3dMEMA \
    -write_script cmd.mema.checks  \
    -dsets $outdir/*REML*.HEAD  \
    -subs_betas "left_vs_right_chx#0_Coef" \
    -subs_tstats "left_vs_right_chx#0_Tstat" \
    -prefix mema_group_checks_LR

tcsh -xef cmd.mema.checks |& tee $logdir/output.mema.checks.log

# Run 3dMEMA for the keypress task
gen_group_command.py \
    -command 3dMEMA \
    -write_script cmd.mema.keypress  \
    -dsets $outdir/*REML*.HEAD  \
    -subs_betas "left_vs_right_press#0_Coef" \
    -subs_tstats "left_vs_right_press#0_Tstat" \
    -prefix mema_group_keypress_LR

tcsh -xef cmd.mema.keypress |& tee $logdir/output.mema.keypress.log

```
{% endcode %}

