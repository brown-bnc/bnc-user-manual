# convert enhanced multi-frame DICOMs to legacy single-frame

Most neuroimaging software is slowly implementing support for the enhanced multi-frame format, which has been around for years now and is becoming ubiquitous. However, when there is no option but to use the legacy single-frame format (such as with Nexstim TMS devices, as of August 2024), you can use a conversion tool from dcm4che.

We host this singularity image on Oscar: /oscar/data/bnc/simgs/dcm4che/dcm4che-tools-5.32.0.sif

You can convert a T1 MPRAGE in a few simple steps:

1. Put your T1 on Oscar (in this example I put it in my data directory)
2. In a terminal (easiest is via an Open OnDemand desktop session), change directory to wherever your T1.dcm is
3. Run this command, replacing the <mark style="color:blue;">blue</mark> with the path to your data directory, <mark style="color:green;">green</mark> with whatever you want your output files to be named, and <mark style="color:red;">red</mark> with the file name of your enhanced DICOM:

`singularity exec -B`` `<mark style="color:blue;">`/path/to/data/directory/`</mark>` ``/oscar/data/bnc/simgs/dcm4che/dcm4che-tools-5.32.0.sif emf2sf --out-file`` `<mark style="color:green;">`sub-999_t1mprage.dcm`</mark> <mark style="color:red;">`1.3.12.2.1107.5.2.43.67050.30000024042614494562600000019-6-1-1bp2iaj.dcm`</mark>
