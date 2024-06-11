---
description: >-
  Reading DICOM files exported from the scanner or XNAT is not always intuitive.
  This script offered by the BNC aims to ease confusion by organizing the files
  in a way that is clear and consistent.
---

# dicomsort: a tool to organize DICOM files

Dicomsort reads information from the DICOM (Digital Imaging and Communications in Medicine) headers of each file and then renames and sorts the files alphabetically by series and slice number. It can also be used to create subdirectories for each series.&#x20;

## Accessing the Script

This script can be accessed on Oscar in the public directory: `/oscar/data/bnc/shared/scripts/oscar-scripts/`.  From there, it can be used standalone or can be integrated into larger pipelines on Oscar. Additionally, it is available for local download on the BNC's github [found here](https://github.com/brown-bnc/oscar-scripts/blob/main/dicomsort). &#x20;

{% hint style="warning" %}
This script relies on multiple AFNI commands. Before running it, ensure that AFNI is installed. On Oscar, this can be done with the command `module load afni`
{% endhint %}

<figure><img src="../.gitbook/assets/Screenshot 2024-06-11 at 4.37.13 PM.png" alt=""><figcaption><p>DICOM files before and after organization via dicomsort.</p></figcaption></figure>

## The script:&#x20;

To display the help message and see how to use the script, you can run `/oscar/data/bnc/shared/scripts/oscar-scripts/dicomsort -?` in a terminal on Oscar.

```
#!/bin/bash
#############
#This script use the afni programs dicom_hdr and dicom_hinfo to read header information, 
#reads the information and then renames and sorts the files alphabetically, optionally
#creating subdirectories for each series.  AFNI must be installed locally for 
#this script to work
#Written by Michael Worden
#Updated 02/07/2024 to add support for optionally creating subject and series 
#subdirectories
#Updated 03/15/2024 to name subdirectories by Series Description instead of Protocol Name
#############

set -euo pipefail

#defaults
sourcedir='./'
destdir='renamed'
tempfile='/tmp/dicomsort.tmp'
rename=0
recurse=1
usesubdir=0
subdir=''
useseqdir=0
seqdir=''

#DICOM field tags
snumtag='0020,0011'     #series number
anumtag='0020,0012'     #acquisition number
inumtag='0020,0013'     #instance number
nametag='0010,0010'     #patient name
idtag='0010,0020'       #patient ID
sdesctag='0008,103e'    #protocol name

usage='Usage: dicomsort [-r] [-d destdir] [-s sourcedir] [-i] [-q] [-n] [-h]'
helptxt="dicom sort is a script to sort rename dicom files in alphabetical order according to\n\
series and slice number.  AFNI must be installed on the local computer to use dicomsort."

#process command line options
while getopts ":rd:s:iqnh" options; do
  case $options in
    r ) rename=1;;
    d ) destdir=$OPTARG;;
    s ) sourcedir=$OPTARG;;
    i ) usesubdir=1;;
    q ) useseqdir=1;;
    n ) recurse=0;;
    h ) echo "$usage";;
    \? ) echo "$usage"
         echo -e "$helptxt"
#     	 echo "dicom sort is a script to sort rename dicom files in alphabetical"
#     	 echo "order according to series and slice number.  "
    	 echo "Options:"
    	 echo "-r: rename files.  Default is to copy."
    	 echo "-d: destination directoroy.  Default is ./renamed ."
    	 echo "-s: source directory.  Default is current directory"
    	 echo "-i: put files in a directory named by the subjectID."
    	 echo "-q: put files in separate sub-directories for each sequence."
    	 echo "-n: don't recursively descend into subdirectories."
    	 echo "-?: print this help message."
    	 echo "-h: print brief usage message."
         exit 1;;
    * ) echo "$usage"
          exit 1;;
  esac
done

#check to see if the destdir exists and create it if not
if [ -d "$destdir" ]; then
	echo Destination directory exists
else
	echo Creating "$destdir"
	mkdir "$destdir"	
fi
targdir="$destdir"

echo "Procecessing..."

#build a list of all the non-hidden files in the target directory
if [ "$recurse" -eq 1 ]; then
	files=$(find "$sourcedir" -type f ! -name ".*" ! -iname "DICOMDIR")
else
	files=$(find "$sourcedir" -type f -maxdepth 1 ! -name ".*" ! -iname "DICOMDIR")
fi	
	
for f in $files;
do
	echo "$f"
	
	#We are only using dicom_hdr to recognize dicom files now.  This seems clunky
	#and could probably be sped up in the future.  All valid dicom files should have 
	#the text DICM at offset 0x80 and we could just look for that in the future but 
	#this is okay for now
	dicom_hdr "$f" > "$tempfile" 
	
	# make sure it's a dicom file
	if grep 'ERROR:' "$tempfile"; then 
	  continue
	fi
	
	# Now using dicom_hinfo to get specific tags instead of dicom_hdr and grep
    snum=$(dicom_hinfo -tag "$snumtag" -no_name "$f")
    anum=$(dicom_hinfo -tag "$anumtag" -no_name "$f")
    if [ "$anum" = "null" ]; then    
        anum=0
    fi 
    inum=$(dicom_hinfo -tag "$inumtag" -no_name "$f")
	
	
	#If we want to use the the subject ID as an enclosing directory, check to see if
	#it exists and create it if not
	if [ "$usesubdir" -eq 1 ]; then
	    subdir=$(dicom_hinfo -tag "$nametag" -no_name "$f")
	    targdir="$destdir"/"$subdir"
		mkdir -p "${targdir}"
	fi
		
	#If we want to use subdirectories for each series, check to see if
	#it exists for the current series and create it if not.  The series name
	#should be prepended with a series number in case there are multiple 
	#series with the same sequence name.
	if [ "$useseqdir" -eq 1 ]; then
	    seqdir=$(dicom_hinfo -tag "$sdesctag" -no_name "$f")
	    serpre=$(printf "%02.0f_" "$snum")
	    targdir="$destdir"/"$subdir"/"$serpre$seqdir"
		mkdir -p "${targdir}"
	fi
	
	targfile=$(printf "%s/dcmS%04.0fA%04.0fI%04.0f\n" "$targdir" "$snum" "$anum" "$inum")
	
	echo "Series ${snum},  Acquisition ${anum},  Instance ${inum}"
	
	if [ "$rename" -eq 1 ]; then
		echo RENAMING "$f" to "$targfile"
		mv "$f" "$targfile"
	else
		echo COPYING "$f" to "$targfile"
		cp "$f" "$targfile"
	fi
	
done
rm "$tempfile"
echo dicomsort Complete
```
