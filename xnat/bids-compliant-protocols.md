# BIDS Compliant Protocols

## Naming Pattern

We provide custom code to export your XNAT imaging session to BIDS format. The process relies on the naming of your sequences. It is helpful to familiarize yourself with the [BIDS Standard](https://bids-specification.readthedocs.io/en/stable/) to better understand the heuristics used. We also provide a short overview in [this section](../bids/introduction-to-bids.md).

We rely on [Heudiconv](https://github.com/nipy/heudiconv) to convert files to the BIDS format. More specifically we use the [ReproIn specification](https://github.com/repronim/reproin) and [heuristic file](https://github.com/nipy/heudiconv/blob/master/heudiconv/heuristics/reproin.py). In general, it is expected that names at the scanner follow the following pattern

```text
<seqtype[-label]>[_ses-<SESID>][_task-<TASKID>][_acq-<ACQLABEL>][_run-<RUNID>][_dir-<DIR>][<more BIDS>][__<custom>]
```

Where:

```text
<...> - value to be entered
[...] - optional -- might be nearly mandatory for some modalities (e.g.,
         run for functional) and very optional for others
*ID - alpha-numerical identifier (e.g. 01,02, pre, post, pre01) for a run,
       task, session. Note that makes more sense to use numerical values for
       RUNID (e.g., _run-01, _run-02) for obvious sorting and possibly
       descriptive ones for e.g. SESID (_ses-movie, _ses-localizer)
       
 <seqtype[-label]>
   a known BIDS sequence type which is usually a name of the folder under
   subject's directory. And (optional) label is specific per sequence type
   (e.g. typical "bold" for func, or "T1w" for "anat"), which could often
   (but not always) be deduced from DICOM. Known to BIDS modalities are:

     anat - anatomical data.  Might also be collected multiple times across
            runs (e.g. if subject is taken out of magnet etc), so could
            (optionally) have "_run" definition attached. For "standard anat"
            labels, please consult to "8.3 Anatomy imaging data" but most
            common are 'T1w', 'T2w', 'angio'
     func - functional (AKA task, including resting state) data.
            Typically contains multiple runs, and might have multiple different
            tasks different per each run
            (e.g. _task-memory_run-01, _task-oddball_run-02)
     fmap - field maps
     dwi  - diffusion weighted imaging (also can as well have runs)

_ses-<SESID> (optional)
    a session.  Having a single sequence within a study would make that study
    follow "multi-session" layout. A common practice to have a _ses specifier
    within the scout sequence name. You can either specify explicit session
    identifier (SESID) or just say to maintain, create (starts with 1).
    You can also use _ses-{date} in case of scanning phantoms or non-human
    subjects and wanting sessions to be coded by the acquisition date.

_task-<TASKID> (optional)
    a short name for a task performed during that run.  If not provided and it
    is a func sequence, _task-UNKNOWN will be automatically added to comply with
    BIDS. Consult http://www.cognitiveatlas.org/tasks on known tasks.

_acq-<ACQLABEL> (optional)
    a short custom label to distinguish a different set of parameters used for
    acquiring the same modality (e.g. _acq-highres, _acq-lowres  etc)

_run-<RUNID> (optional)
    a (typically functional) run. The same idea as with SESID.

_dir-[AP,PA,LR,RL,VD,DV] (optional)
    to be used for fmap images, whenever a pair of the SE images is collected
    to be used to estimate the fieldmap

<more BIDS> (optional)
    any other fields (e.g. _acq-) from BIDS acquisition

__<custom> (optional)
  after two underscores any arbitrary comment which will not matter to how
  layout in BIDS. But that one theoretically should not be necessary,
  and (ab)use of it would just signal lack of thought while preparing sequence
  name to start with since everything could have been expressed in BIDS fields.
```

## Things to Watch

* All **scout** and **localizer** sequences need to have a `scout` label. For example:
  * `anat-scout_acq-localizer`
  * `anat-scout_acq-aascout`
* Functional runs **must** have \_task- field defined
* Do not use "+", "\_", "-" or "." within SESID, TASKID, ACQLABEL, RUNID
* If run was canceled -- just copy canceled run \(with the same index\) and re-run

  it. Files with overlapping name will be considered duplicate/canceled session

  and only the last one would remain.  The others would acquire

  \_\_dup0  suffix.

* Currently the **fieldmaps** collected with our Siemens scanner use the "old way" described [here](https://osf.io/2hjhx/wiki/Brain%20Imaging%20Data%20Structure%20%28BIDS%29/#LCNI_fieldmapshttpslcniuoregonedukbarticleskb0003_29)
* To indicate **runs** in your protocol, without explicitly indicating the run number, simply label the run as `run+`

## Sample Protocols

```text
anat-scout_acq-aascout
anat-scout_acq-localizer
anat-T1w_acq-memprage
fmap_acq-greAP
func-bold_task-TSSblock_acq-2dot4mmSMS4TR1200AP_run+
```





