# ironmap

Ironmap is a script that receives preprocessed 3D+Time fMRI data and outputs one volume, where the value of each voxel is the inverse of the normalized T2\* measurement. 1/T2\* can be used as a proxy for intracellular iron (ferritin) and is particularly useful in the study of dopaminergic systems in the brain.

You can find the ironmap bash script (ironmap.sh) either in the BNC scripts directory on Oscar (`/oscar/data/bnc/scripts`) or on [github](https://github.com/brown-bnc/oscar-scripts/blob/main/ironmap.sh).&#x20;

<details>

<summary>Click here to see the full ironmap.sh script</summary>

```
#!/bin/bash
#This script calls multiple afni commands to generate a one volume NIFTI file, 
#where each voxel contains the median of the 1/nT2* measurement across time
#############################
set -euo pipefail

# Set Variables
output="ironmap"
normalize=0
mask=""
version="Version: 1.0"
usage="Usage: ironmap.sh [-i input NIFTI file] [-m brain mask] [-o output file suffix, default=ironmap] \
[-a take the average/mean of all volumes rather than the median] [-v prints script version] [-h prints help message]"
helptext="Ironmap is a script that receives preprocessed 3D+Time fMRI data and outputs one volume, \
where each voxel is the inverse of the normalized T2* measurement. It does this by:" \
steps="1) Normalizing the voxels of each volume to the mean of that volume. \
2) Taking the median of each voxel across time. \
3) Calculating the inverse."

# Command Line Options
while getopts ":i:m:o:avh" options; do
    case $options in 
        i ) input=$OPTARG;;
        m ) mask=$OPTARG;;
        o ) output=$OPTARG;;
        a ) normalize=1;;
        v ) echo $version;; 
        h ) echo $usage
            echo $helptext
            echo $steps
            echo "Options: "
            echo "-i: REQUIRED. Input one fMRI 3d+time NIFTI file."
            echo "-m: OPTIONAL. Input a brain mask. An MNI brain mask is recommended. If none is provided, "
            echo "one will be created using afni 3dAutomask."
            echo "-o: OPTIONAL. Output file suffix. Will be attached to the end of the input filename. Default is "ironmap"."
            echo "-a: OPTIONAL. Take the average/mean of each voxel across time rather than the median."
            echo "-v: Print script version."
            echo "-h: Print this help text.";;
        \? ) echo $usage;;
        * ) echo $usage
            exit 1;;
    esac
done

if [ $OPTIND -eq 1 ]; then echo "Error: No options were passed. $usage"; fi

for file in $input
do
    filebase="${file%%.*}"

# Step 1: Normalize the voxels of each volume to the mean of the entire volume
## If no mask is given: Create a mask using afni 3dAutomask
    if [ -z "$mask" ]
        then
            echo "No mask given: Creating a brain mask."
            #Create one volume by taking the mean of each voxel over time (Pre Skull Stripping)
            3dTstat -mean -prefix ${filebase}_preSS.nii.gz $input
            #Skull Strip that volume
            3dSkullStrip -input ${filebase}_preSS.nii.gz -prefix ${filebase}_SS.nii.gz
            #Create brain mask
            3dAutomask -prefix ${filebase}_automask.nii.gz ${filebase}_SS.nii.gz 
            #Remove intermediate files 
            rm ${filebase}_preSS.nii.gz ${filebase}_SS.nii.gz
            mask="${filebase}_automask.nii.gz"
            echo "Mask created."
    fi
## Take the mean of all voxels per volume
    echo "Taking the mean of each volume"
    3dmaskave -mask ${mask} -quiet ${input} > ${filebase}_volmeans.1D

## Normalize/scale each voxel (per volume) to that mean
    echo "Normalizing each voxel per volume."
    3dcalc -a ${input} -b ${filebase}_volmeans.1D -expr "(a/b)" -prefix ${filebase}_scaled.nii.gz

# Step 2: Take the median/mean of each voxel across all volumes 
    if [ $normalize -eq 0 ]
        then 
            echo "Taking the median of all volumes."
            3dTstat -median -mask ${mask} -prefix ${filebase}_scaledavg_${normalize}.nii.gz ${filebase}_scaled.nii.gz
        else
            echo "Taking the mean of all volumes."
            3dTstat -mean -mask ${mask} -prefix ${filebase}_scaledavg_${normalize}.nii.gz ${filebase}_scaled.nii.gz
    fi

# Step 3: Take the inverse, 1/nT2*
    echo "Taking the inverse."
    3dcalc -a ${filebase}_scaledavg_${normalize}.nii.gz -expr "(1/a)" -prefix ${filebase}_${output}.nii.gz

# Step 4: Remove intermediate files
    echo "Removing intermediate files." 
    rm ${filebase}_volmeans.1D ${filebase}_scaled.nii.gz ${filebase}_scaledavg_${normalize}.nii.gz 
    echo "Done!"

done 
```



</details>

### Script usage:&#x20;

`bash ironmap.sh -i <input> [optional flags]`

* `-i <input>`: REQUIRED. Input one fMRI 3d+time NIFTI file.
* `-m <mask>`: OPTIONAL. Input a brain mask. An MNI brain mask is recommended. If none is provided, one will be created using afni's 3dAutomask.
* `-o <output>`: OPTIONAL. Output file suffix. Will be attached to the end of the input filename. Default is "ironmap".
* `-a`: OPTIONAL. Take the average/mean of each voxel across time rather than the median.
* `-v`: Print script version.
* -`h`: Print this help text.

### Example Output File

<div align="center" data-full-width="false"><figure><img src="../.gitbook/assets/Screenshot 2024-12-13 at 12.03.01 PM.png" alt="" width="434"><figcaption><p>Single-volume ironmap of the <a href="https://docs.ccv.brown.edu/bnc-user-manual/demo-dataset/introduction">demodat </a>subject 005 resting state scan. The data was preprocessed using fmriprep and the mask was created within ironmap.sh using 3dautomask. Higher values are shown in white. </p></figcaption></figure></div>

### Additional Information

#### What type of data can I input?&#x20;

* Ironmap differs from other T2\* mapping techniques (QSM, ME-EPI) in that it quantifies the inverse normalized T2\* (1/nT2\*) with a _**single-echo EPI time series.**_ For background on this method, please refer to: [Larsen & Luna, 2015](https://pubmed.ncbi.nlm.nih.gov/25594607/); [Sonnenschein et al., 2022](https://pubmed.ncbi.nlm.nih.gov/35523067/). When designing an imaging sequence, it is important to choose an echo time that optimizes the T2\*-weighted signal of your regions of interest. Although resting state scans are recommended, ferritin levels remain stable over time (unlike the BOLD signal) and can be quantified using task-based data as well. If both resting-state and task-based runs are available, test-retest reliability can be measured across different conditions ([Price et al 2021](https://pubmed.ncbi.nlm.nih.gov/34471098/)).  Additionally, the 1/nT2\* ironmap can be created by aggregating data from all EPI runs/conditions.&#x20;

#### Should I take the mean or the median of each voxel across time?&#x20;

* Time averaging is an essential step in targeting the aspects of the T2\*-weighted signal which do not change over time. However, there are multiple approaches to creating a single volume T2\* map from a multi volume time series. Acquiring the median for each voxel across time is recommended, as it can reduce the impact of outlier volumes in the time series ([Parr et al., 2022](https://pubmed.ncbi.nlm.nih.gov/35344773/)). It is also acceptable to take the average/mean over time. This script takes the median by default, but the -a flag can easily be used to take the average instead. The most important consideration is that the method is consistent across runs and participants.&#x20;

#### Why does ironmap calculate the normalized inverse?&#x20;

* First, at every individual TR, ironmap.sh normalizes the value of each voxel to the mean of the entire volume. Normalization of the T2\*-weighted signal mitigates the effect of run to run variability within and between participants/sessions. In the final step, the inverse is calculated for the ease of interpretation; intracellular iron deposition and T2\* have a negative relationship (time-averaged T2\* values decrease as the amount of intracellular iron increases, [Bartzokis et al., 2022](https://www.sciencedirect.com/science/article/pii/S0730725X98001556)). Some groups report their results without taking the inverse. In these instances, lower values reflect increases in intracellular iron.&#x20;

#### What information can I gather from the ironmap?&#x20;

* Typically, the whole-brain ironmap calculation is followed by an ROI analysis that examines the mean ironmap values within specific regions of interest. Voxels across the brain should have an ironmap value of roughly \~1, with higher values associated with higher intracellular iron.&#x20;

