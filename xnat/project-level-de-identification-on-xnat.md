---
description: >-
  XNAT allows users to attach de-identification scripts to projects using the
  software library DicomEdit. The script is applied to data as it is stored on
  XNAT, and is used to change/remove DICOM tags.
---

# Project Level De-Identification on XNAT

## What is DicomEdit?&#x20;

[DicomEdit](https://bitbucket.org/xnatdcm/dicom-edit6/src/master/) is a software library written in ANTLR and Java that is used to edit DICOM tags. It can be downloaded locally and applied to MR data, but notably, it is built into XNAT to allow project-wide custom de-identification. Custom de-identification scripts are saved in the project settings and are applied to incoming data as it is archived.

There are multiple other methods of de-identifying MRI data, such as the [HOROS](https://horosproject.org/) GUI or the coding library [Pydicom](https://pydicom.github.io/). However, DicomEdit via XNAT is particularly useful for labs that would like _store_ their data in it's de-identified form, so as to further maximize data safety.&#x20;

{% hint style="info" %}
Note: DICOM tags are not edited until after data is stored on the XNAT server. Data in the rest API and the XNAT prearchive (only accessible to XNAT admins) is not yet anonymized.
{% endhint %}

The XNAT website provides a [DicomEdit Language Reference](https://wiki.xnat.org/xnat-tools/dicomedit-6-language-reference), which familiarizes users to the DicomEdit syntax. This can be used as a guide to create your own anonymization script. This tutorial provides an example DicomEdit script and instructions on how to enable this script on your XNAT project.

## Creating an Anonymization Script Using DicomEdit

### 1. Select a DicomEdit version

Brown University's current version of XNAT (1.9) is compatible with DicomEdit 6.0-6.8 and DicomEdit 4.2. Details on version compatibility can be found in [XNAT's Version Compatibility Matrix](https://wiki.xnat.org/xnat-tools/dicomedit-6-language-reference#DicomEdit6LanguageReference-VersionCompatibilityMatrix). Syntax varies between DicomEdit versions, and is backwards compatible in some instances (but not all). In this tutorial, we will be writing code using DicomEdit version 6.6.&#x20;

### 2. Determine what DICOM tags need to be anonymized

#### What are DICOM Tags?

DICOM metadata is attached to the image in the form of DICOM tags. Tags are unique to individual attributes and follow this structure:  `(group number),(element number`). Each tag also has a name, [Value Representation (VR)](https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html), [Value Multiplicity (VM)](https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.4.html), a tag definition, and the actual value/content. In this table below, we provide a few examples of information found in a DICOM header.

| DICOM Tag   | Attribute Name   | VR          | VM  | Definition                                                                                              | Value            |
| ----------- | ---------------- | ----------- | --- | ------------------------------------------------------------------------------------------------------- | ---------------- |
| (0008,0020) | Study Date       | Date        | 1   | Date the Study started.                                                                                 | 20250305         |
| (0008,0080) | Institution Name | Long String | 1   | Institution where the equipment that produced the Composite Instances is located.                       | Brown University |
| (0010,2000) | Medical Alerts   | Long String | 1-n | Conditions to which medical staff should be alerted (e.g., contagious condition, drug allergies, etc.). | ACE Inhibitors   |

A full list of DICOM tags can be found on the [DICOM Library website](https://www.dicomlibrary.com/dicom/dicom-tags/). These tags are stored in the DICOM header and can not be separated from the image, thus requiring manual or programmatic editing.&#x20;

#### De-Identifying Personally Identifiable Information (PII)

The level of anonymization needed for a project depends on your lab-specific requirements/guidelines. In more strict instances, labs may need to follow [HIPAA guidelines](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html) using the "Safe Harbor" method of data de-identification. The expandable window below lists the 18 types of identifiers that must be removed according to "Safe Harbor" HIPAA guidelines. These rules apply to not only the individual/subject/patient, but also their relatives, employers, and household members.&#x20;

<details>

<summary>The 18 types of identifiers listed in the "Safe Harbor" method of HIPAA de-identification</summary>

1. Names
2. All geographic subdivisions smaller than a state, including street address, city, county, precinct, ZIP code, and their equivalent geocodes, except for the initial three digits of the ZIP code if, according to the current publicly available data from the Bureau of the Census:
   1. The geographic unit formed by combining all ZIP codes with the same three initial digits contains more than 20,000 people; and
   2. The initial three digits of a ZIP code for all such geographic units containing 20,000 or fewer people is changed to 000
3. All elements of dates (except year) for dates that are directly related to an individual, including birth date, admission date, discharge date, death date, and all ages over 89 and all elements of dates (including year) indicative of such age, except that such ages and elements may be aggregated into a single category of age 90 or older
4. Telephone numbers
5. Vehicle identifiers and serial numbers, including license plate numbers
6. Fax numbers
7. Device identifiers and serial numbers
8. Email addresses
9. Web Universal Resource Locators (URLs)
10. Social security numbers
11. Internet Protocol (IP) addresses
12. Medical record numbers
13. Biometric identifiers, including finger and voice prints
14. Health plan beneficiary numbers
15. Full-face photographs and any comparable images
16. Account numbers
17. Any other unique identifying number, characteristic, or code, except as permitted by paragraph (c) of this section \[Paragraph (c) is presented below in the section “Re-identification”]
    1. (c) _Implementation specifications: re-identification._ A covered entity may assign a code or other means of record identification to allow information de-identified under this section to be re-identified by the covered entity, provided that:
       1. _Derivation._ The code or other means of record identification is not derived from or related to information about the individual and is not otherwise capable of being translated so as to identify the individual; and
       2. _Security._ The covered entity does not use or disclose the code or other means of record identification for any other purpose, and does not disclose the mechanism for re-identification.
18. Certificate/license numbers
    1. The covered entity does not have actual knowledge that the information could be used alone or in combination with other information to identify an individual who is a subject of the information.

</details>

#### Remove, hash, dummy, or zero?&#x20;

Some DICOM tags can be removed from the DICOM header completely, while others must remain in order for the DICOM to be considered valid. When dealing with the latter, there are are multiple ways to de-identify which depend on that attribute's [Data Element Type](https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_7.4.html).&#x20;

1. **Type 1 (Required)**
   1. Mandatory
   2. The Value Field shall contain valid data (as defined by the Value Representation and VM).&#x20;
   3. Cannot have zero length
2. **Type 1C (Conditional)**
   1. Included under certain specified conditions
   2. The Value Field shall contain valid data (as defined by the Value Representation and VM).&#x20;
   3. Cannot have zero length
3. **Type 2 (Required)**
   1. Mandatory
   2. Can have zero Value Length and no Value
   3. If the Value is known, the Value Field shall contain that value (as defined by the VR and VM)
4. **Type 2C (Conditional)**
   1. Included under certain specified conditions
   2. Can have zero Value Length and no Value
   3. If the Value is known, the Value Field shall contain that value (as defined by the VR and VM)
5. **Type 3 (Optional)**
   1. Not required
   2. If they are present, they may have zero length and no value

### De-identification Action Codes

This table from NEMA's [_DICOM PS3.15 2026c - Security and System Management Profiles (E Attribute Confidentiality Profiles)_](https://dicom.nema.org/medical/dicom/current/output/chtml/part15/chapter_e.html) provides definitions of the various actions available when de-identifying DICOM tags. This table is a guide for how to handle each individual tag we wish to edit.&#x20;

<table><thead><tr><th width="126.4609375">Indicator</th><th>Meaning</th></tr></thead><tbody><tr><td>D</td><td>replace with a non-zero length value that may be a dummy value and consistent with the VR</td></tr><tr><td>Z</td><td>replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR</td></tr><tr><td>X</td><td>remove Attribute, and if the Attribute is a Sequence, remove all Sequence Items and their contained Attributes</td></tr><tr><td>K</td><td>keep (unchanged for non-Sequence Attributes, cleaned for Sequences)</td></tr><tr><td>U</td><td>replace with a non-zero length UID that is internally consistent within a set of Instances</td></tr><tr><td>Z/D</td><td>Z unless D is required to maintain IOD conformance (Type 2 versus Type 1)</td></tr><tr><td>X/Z</td><td>X unless Z is required to maintain IOD conformance (Type 3 versus Type 2)</td></tr><tr><td>X/D</td><td>X unless D is required to maintain IOD conformance (Type 3 versus Type 1)</td></tr><tr><td>X/Z/D</td><td>X unless Z or D is required to maintain IOD conformance (Type 3 versus Type 2 versus Type 1)</td></tr></tbody></table>

### List of Demodat DICOM Tags to De-Identify

Next, we provide a table detailing: 1) DICOM tags that are created in our Demodat dataset and require de-identification according to HIPAA guidelines, 2) whether or not they are required in order for the DICOM to pass validation, and 3) their action code/de-identification method.&#x20;

| DICOM Tag    | VR                | Description                                  | Definition                                                                                                                    | Example Value                                              | Required/ Optional         | Data Element Type | Condition (if 1C or 2C)                                                                                                                                              | Deidentification Method |
| ------------ | ----------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | -------------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| (0002,0003)  | Unique Identifier | Media Storage SOP Instance UID               | Uniquely identifies the SOP Instance associated with the Data Set placed in the file and following the File Meta Information. | 1.3.12.2.1107.5.2.43.67050.2025051609442897388301262       | Required                   | 1                 |                                                                                                                                                                      | U                       |
|  (0008,0012) | Date              | Instance Creation Date                       | Date the SOP Instance was created.                                                                                            | 20250305                                                   | Optional                   | 3                 |                                                                                                                                                                      | X/D                     |
| (0008,0013)  | Time              | Instance Creation Time                       | Time the SOP Instance was created.                                                                                            | 153118.732500                                              | Optional                   | 3                 |                                                                                                                                                                      | X/Z/D                   |
| (0008,0018)  | Unique Identifier | SOP Instance UID                             | Uniquely identifies the SOP Instance.                                                                                         | 1.3.12.2.1107.5.2.43.67050.2025030515372349046402286       | Required                   | 1                 |                                                                                                                                                                      | U                       |
| (0008,0020)  | Date              | Study Date                                   | Date the Study started.                                                                                                       | 20250305                                                   | Required, Empty if Unknown | 2                 |                                                                                                                                                                      | Z                       |
| (0008,0021)  | Date              | Series Date                                  | Date the Series started.                                                                                                      | 20250305                                                   | Optional                   | 3                 |                                                                                                                                                                      | X/D                     |
| (0008,0023)  | Date              | Content Date                                 | The date the data creation was started.                                                                                       | 20250305                                                   | Required                   | 1                 |                                                                                                                                                                      | Z/D                     |
| (0008,002A)  | Date Time         | Acquisition DateTime                         | The date and time that the acquisition of data started.                                                                       | 20250305153118.732500                                      | Conditionally Required     | 1C                | Required if Image Type (0008,0008) Value 1 is ORIGINAL or MIXED and SOP Class UID is not "1.2.840.10008.5.1.4.1.1.4.4" (Legacy Converted). May be present otherwise. | X/Z/D                   |
| (0008,0030)  | Time              | Study Time                                   | Time the Study started.                                                                                                       | 152347.800000                                              | Required, Empty if Unknown | 2                 |                                                                                                                                                                      | Z                       |
| (0008,0031)  | Time              | Series Time                                  | Time the Series started.                                                                                                      | 153723.474000                                              | Optional                   | 3                 |                                                                                                                                                                      | X/D                     |
| (0008,0033)  | Time              | Content Time                                 | The time the data creation was started. This is the time the pixel data is created, not the time the data is acquired.        | 153742.101000                                              | Required                   | 1                 |                                                                                                                                                                      | Z/D                     |
| (0008,0050)  | Short String      | Accession Number                             | A departmental Information System generated number that identifies the Imaging Service Request.                               | 2819497684894126                                           | Required, Empty if Unknown | 2                 |                                                                                                                                                                      | Z                       |
| (0008,0080)  | Long String       | Institution Name                             | Institution where the equipment that produced the Composite Instances is located.                                             | Brown University                                           | Optional                   | 3                 |                                                                                                                                                                      | X/Z/D                   |
| (0008,0081)  | Short Text        | Institution Address                          | Mailing address of the institution where the equipment that produced the Composite Instances is located.                      | Olive Street 60,Providence, RI, US, 02912                  | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0008,0090)  | Person Name       | Referring Physician's Name                   | Name of the Patient's referring physician.                                                                                    | REMOVED                                                    | Required, Empty if Unknown | 2                 |                                                                                                                                                                      | Z                       |
| (0008,1010)  | Short String      | Station Name                                 | User defined name identifying the machine that produced the Composite Instances.                                              | AWP67050                                                   | Optional                   | 3                 |                                                                                                                                                                      | X/Z/D                   |
| (0008,1030)  | Long String       | Study Description                            | Institution-generated description or classification of the Study performed.                                                   | BNC DEMODAT2                                               | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0008,103E)  | Long String       | Series Description                           | Description of the Series.                                                                                                    | anat-scout\_acq-aascout                                    | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0008,1111)  | Sequence          | Referenced Performed Procedure Step Sequence | Uniquely identifies the Performed Procedure Step SOP Instance to which the Series is related.                                 |                                                            | Conditionally Required     | 1C                | Required if a Performed Procedure Step SOP Class was involved in the creation of this Series.                                                                        | X/Z/D                   |
| (0010,0010)  | Person Name       | Patient's Name                               | Patient's Full Name                                                                                                           | 101                                                        | Required, Empty if Unknown | 2                 |                                                                                                                                                                      | Z                       |
| (0010,0020)  | Long String       | Patient ID                                   | Primary identifier for the Patient.                                                                                           | 101\_01                                                    | Required, Empty if Unknown | 2                 |                                                                                                                                                                      | Z/D                     |
| (0010,0021)  | Long String       | Issuer of Patient ID                         | Identifier of the Assigning Authority (system, organization, agency, or department) that issued the Patient ID.               |                                                            | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0010,0030)  | Date              | Patient’s Birth Date                         | Birth date of the Patient.                                                                                                    | 19880101                                                   | Required, Empty if Unknown | 2                 |                                                                                                                                                                      | Z                       |
| (0010,0040)  | Code String       | Patient's Sex                                | Sex of the named Patient. Must be M (male), F (female), or O (other).                                                         | F                                                          | Required, Empty if Unknown | 2                 |                                                                                                                                                                      | Z                       |
| (0010,1010)  | Age String        | Patient's Age                                | Age of the Patient.                                                                                                           | 037Y                                                       | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0010,1020)  | Decimal String    | Patient's Size                               | Length or size of the Patient, in meters.                                                                                     | 1.7018                                                     | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0010,1030)  | Decimal String    | Patient's Weight                             | Weight of the Patient, in kilograms.                                                                                          | 52.1631                                                    | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0010,2000)  | Long String       | Medical Alerts                               | Conditions to which medical staff should be alerted (e.g., contagious condition, drug allergies, etc.).                       | ACE Inhibitors                                             | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0010,2110)  | Long String       | Allergies                                    | Description of prior reaction to contrast agents, or other patient allergies or adverse reactions.                            | Latex Allergy                                              | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0012,0062)  |                   | Patient Identity Removed                     |                                                                                                                               | NO                                                         |                            |                   |                                                                                                                                                                      |                         |
| (0018,1000)  | Long String       | Device Serial Number                         | Manufacturer's serial number of the device.                                                                                   | 35016                                                      | Required                   | 1                 |                                                                                                                                                                      | X/Z/D                   |
| (0018,1030)  | Long String       | Protocol Name                                | User-defined description of the conditions under which the Series was performed.                                              | anat-scout\_acq-aascout                                    | Optional                   | 3                 |                                                                                                                                                                      | X/D                     |
| (0020,000D)  | Unique Identifier | Study Instance UID                           | Unique identifier for the Study.                                                                                              | 1.3.12.2.1107.5.2.43.67050.30000025051410180446400000027   | Required                   | 1                 |                                                                                                                                                                      | U                       |
| (0020,000E)  | Unique Identifier | Series Instance UID                          | Unique identifier of a Series that is part of this Study and contains the referenced Composite Object(s).                     | 1.3.12.2.1107.5.2.43.67050.2025051609442873134001130.0.0.0 | Required                   | 1                 |                                                                                                                                                                      | U                       |
| (0020,0010)  | Short String      | Study ID                                     | User or equipment generated Study identifier.                                                                                 | b2435425-a1df-47                                           | Required, Empty if Unknown | 2                 |                                                                                                                                                                      | Z                       |
| (0020,0052)  | Unique Identifier | Frame of Reference UID                       | Uniquely identifies the Frame of Reference for a Series.                                                                      | 1.3.12.2.1107.5.2.43.67050.2.20250516094219023.0.0.0       | Required                   | 1                 |                                                                                                                                                                      | U                       |
| (0040,0244)  | Date              | Performed Procedure Step Start Date          | Date on which the Performed Procedure Step started.                                                                           | 20250516                                                   | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0040,0245)  | Time              | Performed Procedure Step Start Time          | Time on which the Performed Procedure Step started.                                                                           | 93357.2                                                    | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0040,0250)  | Date              | Performed Procedure Step End Date            | Date on which the Performed Procedure Step ended.                                                                             | 20250516                                                   | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0040,0253)  | Short String      | Performed Procedure Step ID                  | User or equipment generated identifier of that part of a Procedure that has been carried out within this step.                | USfbfecb51151346                                           | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0040,0254)  | Long String       | Performed Procedure Step Description         | Institution-generated description or classification of the Procedure Step that was performed.                                 | BNC DEMODAT2                                               | Optional                   | 3                 |                                                                                                                                                                      | X                       |
| (0040,2004)  | Date              | Issue Date of Imaging Service Request        | Date on which the Imaging Service Request was issued by the requester.                                                        | 20250516                                                   | Optional                   | 3                 |                                                                                                                                                                      | X                       |

### 3. Writing the Script

This script de-identifies the list of DICOM tags in the table above (tags present in the MRI scans exported from our scanner which contain Personally Identifiable Information).  XNAT provides documentation on [the syntax of DicomEdit versions 6+](https://wiki.xnat.org/xnat-tools/dicomedit-6-language-reference).&#x20;

```
version "6.6"

// Selected tags are found in the DICOMS produced at the Brown MRF; other sites may include other tags 

// ##############################################################
// ###################### DICOM Table E ##########################
// ##############################################################

// De-identify all tags indicated in Table E.1-1. Application Level Confidentiality Profile Attributes

// Remove Optional Tags
-(0008,0012)     // Instance Creation Date (X/D)
-(0008,0013)     // Instance Creation Time (X/Z/D)
-(0008,0021)     // Series Date (X/D)
-(0008,0031)     // Series Time (X/D) 
-(0008,0080)     // Institution Name (X/Z/D)
-(0008,0081)     // Institution Address (X)
-(0008,1010)     // Station Name (X/Z/D)
-(0010,1010)     // Patient's Age (X)
-(0010,1020)     // Patient's Size (X)
-(0010,1030)     // Patient's Weight (X)
-(0010,2000)     // Medical Alerts (X)
-(0010,2110)     // Allergies (X)
-(0018,1000)     // Device Serial Number (X/Z/D)
-(0040,0244)     // Performed Procedure Step Start Date (X)
-(0040,0245)     // Performed Procedure Step Start Time (X)
-(0040,0250)     // Performed Procedure Step End Date (X)
-(0040,0253)     // Performed Procedure Step ID (X)
-(0040,0254)     // Performed Procedure Step Description (X)
-(0040,2004)     // Issue Date of Imaging Service Request (X)

// Set Required Tags to Empty String
(0008,0030) := " "     // Study Time (Z)
(0008,0033) := " "     // Content Time (Z/D)
(0008,0050) := " "     // Accession Number (Z)
(0008,0090) := " "     // Referring Physician's Name (Z)
(0020,0010) := " "     // Study ID (Z)

// Set Dummy Values
(0010,0040) := "O"                         // Patient's Sex (Required, Empty if Unknown (Z))
// Change birthday to a generic date (01/01/1900)
(0010,0030) := "19000101"                  // Patient's Birth Date (Required, Empty if Unknown (Z))

// ####################################################################
// ########################### Hash UIDs  #############################
// ####################################################################

// Remove nested references 
-(0008,1111)     // Referenced Performed Procedure Step Sequence (X/Z/D)
-(0008,9092)    // Referenced Image Evidence Sequence (conditionally required, removed)

// Hash UIDs
hashUIDList [(0002,0003), (0008,0018), (0020,000D), (0020,000E), (0020,0052)]

//              (0002,0003)        // Media Storage SOP Instance UID (U)
//              (0008,0018)        // SOP Instance UID (U)
//              (0020,000D)        // Study Instance UID (U)
//              (0020,000E)        // Series Instance UID (U)
//              (0020,0052)        // Frame of Reference UID (U)

// ####################################################################
// ########################### Shift Times ############################
// ####################################################################

// Date and Time Information
// Shift Dates/Times Date by 14 days
tagPathsToShift := {
(0008,0020), (0008,0023), (0008,002A)}
shiftDateTimeListByIncrement[ tagPathsToShift, 14, "days"]

// (0008,0020)     // Study Date (Z)
// (0008,0023)     // Content Date (Z/D)
// (0008,002A)     // Acquisition DateTime (1C condition met; X/Z/D)

// ####################################################################
// ####################### Mark as Anonymized ###########################
// ####################################################################

// Mark DICOM as de-identified
(0012,0062) := "YES"
(0012,0063) := "dicomedit used to anonymize PII tags"  // De-identification Method

```

{% hint style="info" %}
Please note that some DICOM tags are missing from this script because they are already de-identified when the file is created (for example, subject ID/name).&#x20;
{% endhint %}

## Applying Your DicomEdit Script to an XNAT Project

XNAT offers a built in setting where project owners can save a DicomEdit script. When enabled, this script is applied to all incoming data for that specific project. The anonymization script is saved in the manage tab within any XNAT project.

<figure><img src="../.gitbook/assets/Screenshot 2026-07-17 at 10.02.01 AM.png" alt="The &#x22;Manage&#x27; tab is located in the project page on XNAT."><figcaption></figcaption></figure>

After selecting the "Manage" tab, Go to the section titled "Anonymization Script". There, you can paste your DicomEdit script. Ensure that the "Enable Script" box is checked, and then press save. Now, all incoming data to this project will have the script applied to it!

<figure><img src="../.gitbook/assets/Screenshot 2026-07-17 at 10.03.31 AM.png" alt="In the manage tab, there is a section called &#x22;Anonymization Script&#x22;. Here, we have pasted the example DicomEdit script. The &#x22;Enable Script&#x22; box is checked and the &#x22;Save&#x22; button is pressed. "><figcaption></figcaption></figure>

Here you can view the DICOM headers for a T1-weighted MEMPRAGE (Demodat2 subject 101 session 01) both before and after the example anonymization script was applied. Always make sure to check the final header when developing/editing an anonymization script, to ensure that all PII has been properly de-identified!

{% file src="../.gitbook/assets/T1w_header.txt" %}

{% file src="../.gitbook/assets/anonymized_T1w_header.txt" %}
