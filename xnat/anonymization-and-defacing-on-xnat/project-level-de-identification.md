---
description: >-
  XNAT allows users to attach de-identification scripts to projects using the
  software library DicomEdit. The script is applied to data as it is stored on
  XNAT, and is used to change/remove DICOM tags.
---

# Project Level De-Identification

## What is DicomEdit?&#x20;

[DicomEdit](https://bitbucket.org/xnatdcm/dicom-edit6/src/master/) is a software library written in ANTLR and Java that is used to edit DICOM tags. It can be downloaded locally and applied to MR data, but notably, it is built into XNAT to allow project-wide custom de-identification. Custom de-identification scripts are saved in the project settings and are applied to incoming data as it is archived.

There are multiple other methods of de-identifying MRI data, such as the [HOROS](https://horosproject.org/) GUI or the coding library [Pydicom](https://pydicom.github.io/). However, DicomEdit via XNAT is particularly useful for labs that would like to _store_ their data in its de-identified form, so as to further maximize data safety.&#x20;

{% hint style="info" %}
Note: DICOM tags are not edited until after data is stored on the XNAT server. Data in the XNAT prearchive (only accessible to XNAT admins) is not yet anonymized.
{% endhint %}

The XNAT website provides a [DicomEdit Language Reference](https://wiki.xnat.org/xnat-tools/dicomedit-6-language-reference), which familiarizes users to the DicomEdit syntax. This can be used as a guide to create your own anonymization script. This tutorial provides an example DicomEdit script and instructions on how to enable this script on your XNAT project.

## Creating an Anonymization Script Using DicomEdit

### 1. Select a DicomEdit version

Brown University's current version of XNAT (1.10.0) is compatible with DicomEdit 6.0-6.9 and DicomEdit 4.2. Details on version compatibility can be found in [XNAT's Version Compatibility Matrix](https://wiki.xnat.org/xnat-tools/dicomedit-6-language-reference#DicomEdit6LanguageReference-VersionCompatibilityMatrix). Syntax varies between DicomEdit versions, and it is backwards compatible in some instances (but not all). In this tutorial, we will be writing code using DicomEdit version 6.6.&#x20;

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

This table from NEMA: [_DICOM PS3.15 2026c - Security and System Management Profiles (E Attribute Confidentiality Profiles)_](https://dicom.nema.org/medical/dicom/current/output/chtml/part15/chapter_e.html) provides definitions of the various actions available when de-identifying DICOM tags. This table is a guide for how to handle each individual tag we wish to edit.&#x20;

<table><thead><tr><th width="126.4609375">Indicator</th><th>Meaning</th></tr></thead><tbody><tr><td>D</td><td>replace with a non-zero length value that may be a dummy value and consistent with the VR</td></tr><tr><td>Z</td><td>replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR</td></tr><tr><td>X</td><td>remove Attribute, and if the Attribute is a Sequence, remove all Sequence Items and their contained Attributes</td></tr><tr><td>K</td><td>keep (unchanged for non-Sequence Attributes, cleaned for Sequences)</td></tr><tr><td>U</td><td>replace with a non-zero length UID that is internally consistent within a set of Instances</td></tr><tr><td>Z/D</td><td>Z unless D is required to maintain IOD conformance (Type 2 versus Type 1)</td></tr><tr><td>X/Z</td><td>X unless Z is required to maintain IOD conformance (Type 3 versus Type 2)</td></tr><tr><td>X/D</td><td>X unless D is required to maintain IOD conformance (Type 3 versus Type 1)</td></tr><tr><td>X/Z/D</td><td>X unless Z or D is required to maintain IOD conformance (Type 3 versus Type 2 versus Type 1)</td></tr></tbody></table>

### List of Demodat DICOM Tags to De-Identify

Next, we provide a table detailing:

1. All DICOM tags that require de-identification according to HIPAA guidelines, cross referenced with NEMA's "Table E.1-1. Application Level Confidentiality Profile Attributes"
   1. Tags were included if they are known to be in MR DICOMs, or if their usage is unclear.&#x20;
   2. Categories include: Enhanced MR (E), Legacy MR (L), and M (MR). Unclear DICOM categorizations are left blank.&#x20;
2. Further information on the tag, such as: VR, VM, Definition, Examples, Retirement Status
3. Whether or not the tag is required in order for the DICOM to pass validation
4. Its action code/de-identification method, according to NEMA's "Table E.1-1. Application Level Confidentiality Profile Attributes"

**This DICOM De-identification table is currently found in a** [**public google sheet**](https://docs.google.com/spreadsheets/d/1uqdLbYpDlFV6JnkVY6N_p79cFQ6oRlcVU8qYuufSogM/edit?usp=sharing)**.**&#x20;

### 3. Writing the Script

This script de-identifies the list of DICOM tags in the table above (tags present in the MRI scans exported from our scanner which contain Personally Identifiable Information).  XNAT provides documentation on [the syntax of DicomEdit versions 6+](https://wiki.xnat.org/xnat-tools/dicomedit-6-language-reference).&#x20;

```
version "6.6"

// ##############################################################
// ################ Anonymize Legacy DICOM Tags #################
// ##############################################################

// Delete the specific CSA Image and Series Header Info blocks completely
-(0029, {SIEMENS MR HEADER}10)
-(0029, {SIEMENS MR HEADER}20)

// ###############################################################################
// ###### De-identify all tags indicated in Table E.1-1. Application #############
// ############ Level Confidentiality Profile Attributes #########################
// ###############################################################################

// ################ Remove Non-required Tags ####################

// Remove Optional Tags
-(0008,0012)     // Instance Creation Date (X/D)
-(0008,0013)     // Instance Creation Time (X/Z/D)
-(0008,0015)     // Instance Creation DateTime (X)
-(0008,0021)     // Series Date (X/D)
-(0008,0022)     // Acquisition Date (X/Z)
-(0008,0031)     // Series Time (X/D)
-(0008,0032)     // Acquisition Time (X/Z)
-(0008,0054)     // Retrieve AE Title (X)
-(0008,0081)     // Institution Address (X)
-(0008,0082)     // Institution Code Sequence (X/Z/D)
-(0008,0096)     // Referring Physician Identification Sequence (X)
-(0008,009D)     // Consulting Physician Identification Sequence (X)
-(0008,0201)     // Timezone Offset From UTC (X)
-(0008,1010)     // Station Name (X/Z/D)
-(0008,1040)     // Institutional Department Name (X)
-(0008,1041)     // Institutional Department Type Code Sequence (X)
-(0008,1048)     // Physician(s) of Record (X)
-(0008,1049)     // Physician(s) of Record Identification Sequence (X)
-(0008,1050)     // Performing Physician's Name (X)
-(0008,1052)     // Performing Physician Identification Sequence (X)
-(0008,1060)     // Name of Physician(s) Reading Study (X)
-(0008,1062)     // Physician(s) Reading Study Identification Sequence (X)
-(0008,1070)     // Operators' Name (X/Z/D)
-(0008,1072)     // Operator Identification Sequence (X/D)
-(0008,1080)     // Admitting Diagnoses Description (X)
-(0008,1084)     // Admitting Diagnoses Code Sequence (X)
-(0008,1110)     // Referenced Study Sequence (X)
-(0008,1120)     // Referenced Patient Sequence (X)
-(0008,1301)     // Principal Diagnosis Code Sequence (X)
-(0008,1302)     // Primary Diagnosis Code Sequence (X)
-(0008,1303)     // Secondary Diagnoses Code Sequence (X)
-(0008,1304)     // Histological Diagnoses Code Sequence (X)
-(0008,2111)     // Derivation Description (X)
-(0010,0011)     // Person Names to Use Sequence (X)
-(0010,0012)     // Name to Use (X)
-(0010,0013)     // Name to Use Comment (X)
-(0010,0014)     // Third Person Pronouns Sequence (X)
-(0010,0015)     // Pronoun Code Sequence (X)
-(0010,0016)     // Pronoun Comment (X)
-(0010,0021)     // Issuer of Patient ID (X)
-(0010,0032)     // Patient's Birth Time (X)
-(0010,1010)     // Patient's Age (X)
-(0010,1020)     // Patient's Size (X)
-(0010,1030)     // Patient's Weight (X)
-(0010,0041)     // Gender Identity Sequence (X)
-(0010,0042)     // Sex Parameters for Clinical Use Category Comment (X)
-(0010,0043)     // Sex Parameters for Clinical Use Category Sequence (X)
-(0010,0044)     // Gender Identity Code Sequence (X)
-(0010,0045)     // Gender Identity Comment (X)
-(0010,0046)     // Sex Parameters for Clinical Use Category Code Sequence (X)
-(0010,0047)     // Sex Parameters for Clinical Use Category Reference (X)
-(0010,0050)     // Patient's Insurance Plan Code Sequence (X)
-(0010,0101)     // Patient's Primary Language Code Sequence (X)
-(0010,0102)     // Patient's Primary Language Modifier Code Sequence (X)
-(0010,1001)     // Other Patient Names (X)
-(0010,1002)     // Other Patient IDs Sequence (X)
-(0010,1005)     // Patient's Birth Name (X)
-(0010,1040)     // Patient's Address (X)
-(0010,1060)     // Patient's Mother's Birth Name (X)
-(0010,1080)     // Military Rank (X)
-(0010,1081)     // Branch of Service (X)
-(0010,1100)     // Referenced Patient Photo Sequence (X)
-(0010,2000)     // Medical Alerts (X)
-(0010,2110)     // Allergies (X)
-(0010,2150)     // Country of Residence (X)
-(0010,2152)     // Region of Residence (X)
-(0010,2154)     // Patient's Telephone Numbers (X)
-(0010,2155)     // Patient's Telecom Information (X)
-(0010,2161)     // Ethnic Group Code Sequence (X)
-(0010,2162)     // Ethnic Groups (X)
-(0010,2180)     // Occupation (X)
-(0010,21A0)     // Smoking Status (X)
-(0010,21B0)     // Additional Patient History (X)
-(0010,21C0)     // Pregnancy Status (X)
-(0010,21D0)     // Last Menstrual Date (X)
-(0010,21F0)     // Patient's Religious Preference (X)
-(0010,2203)     // Patient's Sex Neutered (X/Z)
-(0010,2297)     // Responsible Person (X)
-(0010,2299)     // Responsible Organization (X)
-(0010,4000)     // Patient Comments (X)
-(0012,0022)     // Issuer of Clinical Trial Protocol ID (X)
-(0012,0023)     // Other Clinical Trial Protocol IDs Sequence (X)
-(0012,0032)     // Issuer of Clinical Trial Site ID (X)
-(0012,0041)     // Issuer of Clinical Trial Subject ID (X)
-(0012,0043)     // Issuer of Clinical Trial Subject Reading ID (X)
-(0012,0051)     // Clinical Trial Time Point Description (X)
-(0012,0055)     // Issuer of Clinical Trial Time Point ID (X)
-(0012,0071)     // Clinical Trial Series ID (X)
-(0012,0072)     // Clinical Trial Series Description (X)
-(0012,0073)     // Issuer of Clinical Trial Series ID (X)
-(0012,0082)     // Clinical Trial Protocol Ethics Committee Approval Number (X)
-(0018,1000)     // Device Serial Number (X/Z/D)
-(0018,1008)     // Gantry ID (X)
-(0018,1009)     // Unique Device Identifier (X)
-(0018,100A)     // UDI Sequence (X)
-(0018,1042)     // Contrast/Bolus Start Time (X)
-(0018,1043)     // Contrast/Bolus Stop Time (X)
-(0018,1200)     // Date of Last Calibration (X)
-(0018,1201)     // Time of Last Calibration (X)
-(0018,1202)     // DateTime of Last Calibration (X)
-(0018,1205)     // Date of Installation (X)
-(0018,A001)     // Contributing Equipment Sequence (X)
-(0018,A002)     // Contribution DateTime (X)
-(0018,A003)     // Contribution Description (X)
-(0020,4000)     // Image Comments (X)
-(0020,9158)     // Frame Comments (X)
-(0032,1032)     // Requesting Physician (X)
-(0032,1033)     // Requesting Service (X)
-(0032,1060)     // Requested Procedure Description (X/Z)
-(0032,1066)     // Reason for Visit (X)
-(0032,1067)     // Reason for Visit Code Sequence (X)
-(0032,1070)     // Requested Contrast Agent (X)
-(0038,0010)     // Admission ID (X)
-(0038,0014)     // Issuer of Admission ID Sequence (X)
-(0038,0020)     // Admitting Date (X)
-(0038,0021)     // Admitting Time (X)
-(0038,0050)     // Special Needs (X)
-(0038,0060)     // Service Episode ID (X)
-(0038,0062)     // Service Episode Description (X)
-(0038,0064)     // Issuer of Service Episode ID Sequence (X)
-(0038,0300)     // Current Patient Location (X)
-(0038,0400)     // Patient's Institution Residence (X)
-(0038,0500)     // Patient State (X)
-(0038,4000)     // Visit Comments (X)
-(0040,0001)     // Scheduled Station AE Title (X)
-(0040,0002)     // Scheduled Procedure Step Start Date (X)
-(0040,0003)     // Scheduled Procedure Step Start Time (X)
-(0040,0004)     // Scheduled Procedure Step End Date (X)
-(0040,0005)     // Scheduled Procedure Step End Time (X)
-(0040,0006)     // Scheduled Performing Physician's Name (X)
-(0040,0007)     // Scheduled Procedure Step Description (X)
-(0040,0009)     // Scheduled Procedure Step ID (X)
-(0040,000B)     // Scheduled Performing Physician Identification Sequence (X)
-(0040,0010)     // Scheduled Station Name (X)
-(0040,0011)     // Scheduled Procedure Step Location (X)
-(0040,0012)     // Pre-Medication (X)
-(0040,0241)     // Performed Station AE Title (X)
-(0040,0242)     // Performed Station Name (X)
-(0040,0243)     // Performed Location (X)
-(0040,0244)     // Performed Procedure Step Start Date (X)
-(0040,0245)     // Performed Procedure Step Start Time (X)
-(0040,0250)     // Performed Procedure Step End Date (X)
-(0040,0251)     // Performed Procedure Step End Time (X)
-(0040,0253)     // Performed Procedure Step ID (X)
-(0040,0254)     // Performed Procedure Step Description (X)
-(0040,0275)     // Request Attributes Sequence (X)
-(0040,0280)     // Comments on the Performed Procedure Step (X)
-(0040,051A)     // Container Description (X)
-(0040,0555)     // Acquisition Context Sequence (X)
-(0040,0556)     // Acquisition Context Description (X)
-(0040,0600)     // Specimen Short Description (X)
-(0040,0602)     // Specimen Detailed Description (X)
-(0040,1001)     // Requested Procedure ID (X)
-(0040,1002)     // Reason for the Requested Procedure (X)
-(0040,1004)     // Patient Transport Arrangements (X)
-(0040,1005)     // Requested Procedure Location (X)
-(0040,100A)     // Reason for Requested Procedure Code Sequence (X)
-(0040,1010)     // Names of Intended Recipients of Results (X)
-(0040,1011)     // Intended Recipients of Results Identification Sequence (X)
-(0040,1102)     // Person's Address (X)
-(0040,1103)     // Person's Telephone Numbers (X)
-(0040,1104)     // Person's Telecom Information (X)
-(0040,1400)     // Requested Procedure Comments (X)
-(0040,2004)     // Issue Date of Imaging Service Request (X)
-(0040,2005)     // Issue Time of Imaging Service Request (X)
-(0040,2008)     // Order Entered By (X)
-(0040,2009)     // Order Enterer's Location (X)
-(0040,2010)     // Order Callback Phone Number (X)
-(0040,2011)     // Order Callback Telecom Information (X)
-(0040,2400)     // Imaging Service Request Comments (X)
-(0040,3001)     // Confidentiality Constraint on Patient Data Description (X)
-(0040,4005)     // Scheduled Procedure Step Start DateTime (X)
-(0040,4008)     // Scheduled Procedure Step Expiration DateTime (X)
-(0040,4010)     // Scheduled Procedure Step Modification DateTime (X)
-(0040,4011)     // Expected Completion DateTime (X)
-(0040,4025)     // Scheduled Station Name Code Sequence (X)
-(0040,4027)     // Scheduled Station Geographic Location Code Sequence (X)
-(0040,4028)     // Performed Station Name Code Sequence (X)
-(0040,4030)     // Performed Station Geographic Location Code Sequence (X)
-(0040,4034)     // Scheduled Human Performers Sequence (X)
-(0040,4035)     // Actual Human Performers Sequence (X)
-(0040,4036)     // Human Performer's Organization (X)
-(0040,4037)     // Human Performer's Name (X)
-(0040,4050)     // Performed Procedure Step Start DateTime (X)
-(0040,4051)     // Performed Procedure Step End DateTime (X)
-(0040,4052)     // Procedure Step Cancellation DateTime (X)
-(0040,A032)     // Observation DateTime (X/D)
-(0040,A033)     // Observation Start DateTime (X)
-(0040,E004)     // HL7 Document Effective Time (X)
-(0044,0004)     // Approval Status DateTime (X)
-(0044,000B)     // Product Expiration DateTime (X)
-(0044,0010)     // Substance Administration DateTime (X)
-(0050,001B)     // Container Component ID (X)
-(0050,0020)     // Device Description (X)
-(0074,1234)     // Receiving AE (X)
-(0074,1236)     // Requesting AE (X)
-(0088,0200)     // Icon Image Sequence (X)
-(0100,0420)     // SOP Authorization DateTime (X)
-(0400,0115)     // Certificate of Signer (D)
-(0400,0310)     // Certified Timestamp (X)
-(0400,0402)     // Referenced Digital Signature Sequence (X)
-(0400,0403)     // Referenced SOP Instance MAC Sequence (X)
-(0400,0404)     // MAC (X)
-(0400,0550)     // Modified Attributes Sequence (X)
-(0400,0551)     // Nonconforming Modified Attributes Sequence (X)
-(0400,0552)     // Nonconforming Data Element Value (X)
-(0400,0561)     // Original Attributes Sequence (X)
-(0400,0600)     // Instance Origin Status (X)
-(2030,0020)     // Text String (X)
-(2100,0040)     // Creation Date (X)
-(2100,0050)     // Creation Time (X)
-(2100,0070)     // Originator (X)
-(2200,0005)     // Barcode Value (X/Z)

// Table E.1-1 lists these as Z, but they are SQ elements. DicomEdit can't write
// an empty sequence so remove instead.
-(0040,0513)
-(0040,0562)
-(0040,0610)
-(0040,1101)

// Remove nested references
-(0008,1111)     // Referenced Performed Procedure Step Sequence (X/Z/D)
-(0008,9092)     // Referenced Image Evidence Sequence (conditionally required, removed) (not in table E)

// ################ Set Required Tags to Empty String #####################
(0008,0030) := " "     // Study Time (Z) 
(0008,0033) := " "     // Content Time (Z/D) 
(0008,0050) := " "     // Accession Number (Z)
(0008,0090) := " "     // Referring Physician's Name (Z)
(0008,009C) := " "     // Consulting Physician's Name (Z)
(0012,0021) := " "     // Clinical Trial Protocol Name (Z)
(0012,0030) := " "     // Clinical Trial Site ID (Z)
(0012,0031) := " "     // Clinical Trial Site Name (Z)
(0012,0050) := " "     // Clinical Trial Time Point ID (Z)
(0012,0060) := " "     // Clinical Trial Coordinating Center Name (Z)
(0018,0010) := " "     // Contrast/Bolus Agent (Z/D)
(0020,0010) := " "     // Study ID (Z)
(0400,0564) := " "     // Source of Previous Values (Z)

// ######################## Set Dummy Values ##########################

(0008,0080) := "anonymized"         // Institution Name (X/Z/D)
// (0008,0106) := "19000101000000"     //  Context Group Version (D), VR is DT
// (0008,0107) := "19000101000000"     // Context Group Local Version (D), VR is DT
// Change birthday to a generic date (01/01/1900)
(0010,0030) := "19000101"           // Patient's Birth Date (Required, Empty if Unknown (Z))
(0010,0040) := "O"                  // Patient's Sex (Required, Empty if Unknown (Z))
(0012,0010) := "anonymized"         // Clinical Trial Sponsor Name (D)
(0012,0020) := "anonymized"         // Clinical Trial Protocol ID (D)
(0012,0040) := "anonymized"         // Clinical Trial Subject ID (D)
(0012,0042) := "anonymized"         // Clinical Trial Subject Reading ID (D)
(0012,0081) := "anonymized"         // Clinical Trial Protocol Ethics Committee Name (D)
(0040,0512) := "anonymized"         // Container Identifier (D)
(0040,0551) := "anonymized"         // Specimen Identifier (D)
(0040,A121) := "19000101"           // Date (D), VR is DA, must be YYYYMMDD
(0040,A122) := "000000"             // Time (D), VR is TM, must be HHMMSS
(0040,A123) := "anonymized"         // Person Name (D)
(0400,0563) := "anonymized"         // Modifying System (D)
(0400,0565) := "COERCE"             // Reason for the Attribute Modification (D)

// ########################### Hash UIDs  #############################

// Hash UIDs -- TOP LEVEL ONLY.
// Tags that also occur nested are handled in the Enhanced DICOM block below.
// Do NOT add sequence (SQ) tags such as (0020,9221) or (0020,9222) here;
// they are containers, not UIDs, and will fail to hash.
hashUIDList [(0002,0003), (0008,0014), (0008,0017), (0008,0058), (0018,1002), (0018,100B), (0020,0200), (0020,9161), (0040,0554), (0040,A124), (0040,A172), (0088,0140), (0400,0100), (300A,0054), (300A,0700)]

//              (0002,0003)        // Media Storage SOP Instance UID (U)
//              (0008,0014)        // Instance Creator UID (U)
//              (0008,0017)        // Acquisition UID (U)
//              (0008,0058)        // Failed SOP Instance UID List (U) (removed in debugging)
//              (0018,1002)        // Device UID (U)
//              (0018,100B)        // Manufacturer's Device Class UID (U)
//              (0020,0200)        // Synchronization Frame of Reference UID (U)
//              (0020,9161)        // Concatenation UID (U)
//              (0040,0554)        // Specimen UID (U)
//              (0040,A124)        // UID (U)
//              (0040,A172)        // Referenced Observation UID (Trial) (U)
//              (0088,0140)        // Storage Media File-set UID (U)
//              (0400,0100)        // Digital Signature UID (U)
//              (300A,0054)        // Table Top Position Alignment UID (U)
//              (300A,0700)        // Treatment Session UID (U)

// ########################### Shift Times ############################

// Date and Time Information
// Shift Dates/Times by 14 days(TOP LEVEL ONLY)
// Tags that are nested are handled in the Enhanced DICOM block below.

tagPathsToShift := {
(0008,0020), (0008,0023), (0400,0105), (0400,0562)}
shiftDateTimeListByIncrement[ tagPathsToShift, 14, "days"]

// (0008,0020)     // Study Date (Z)
// (0008,0023)     // Content Date (Z/D)
// (0400,0105)     // Digital Signature DateTime (D)
// (0400,0562)     // Attribute Modification DateTime (D)

// ######### Enhanced DICOM: Nested Sequence Handling #################

// Siemens enhanced MR stores per-frame timing and dimension UIDs inside
// functional group sequences.
// The container sequences themselves are required for the image to load
// correctly and are NOT deleted. Only their contents are altered.

// Nested UIDs
hashUIDList [*/(0008,0018), */(0008,1155), */(0020,000D), */(0020,000E), */(0020,0052), */(0020,9164)]

//   */(0008,0018)   // SOP Instance UID (U), top level and nested
//   */(0008,1155)   // Referenced SOP Instance UID (U), inside referenced-image sequences
//   */(0020,000D)   // Study Instance UID (U)
//   */(0020,000E)   // Series Instance UID (U)
//   */(0020,0052)   // Frame of Reference UID (U)
//   */(0020,9164)   // Dimension Organization UID (U), inside (0020,9221) and (0020,9222)

// Nested dates and times (same 14 day shift)
nestedTagPathsToShift := {
*/(0008,002A), */(0018,9074), */(0018,9151), */(0040,A120)}
shiftDateTimeListByIncrement[ nestedTagPathsToShift, 14, "days"]

//   */(0008,002A)   // Acquisition DateTime (X/Z/D)
//   */(0018,9074)   // Frame Acquisition DateTime (D), in Frame Content Sequence
//   */(0018,9151)   // Frame Reference DateTime (D), in Frame Content Sequence
//   */(0040,A120)   // DateTime (D)

// ####################################################################
// ####################### Mark as Anonymized #########################
// ####################################################################

// Mark DICOM as de-identified
(0012,0062) := "YES"
(0012,0063) := "dicomedit used to anonymize PII tags"  // De-identification Method
```

{% hint style="info" %}
Please note that some DICOM tags are missing from this script because they are already de-identified when the file is created (for example, Subject ID/Name).&#x20;
{% endhint %}

## Applying Your DicomEdit Script to an XNAT Project

{% hint style="info" %}
This section is for educational purposes. If you are interested in applying a de-identification script to your data, this will be completed by an XNAT admin.&#x20;
{% endhint %}

XNAT offers a built in setting where project owners can save a DicomEdit script. When enabled, this script is applied to all incoming data for that specific project. The anonymization script is saved in the manage tab within any XNAT project, which is accessible to project owners and XNAT admins.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2026-07-17 at 10.02.01 AM.png" alt="The &#x22;Manage&#x27; tab is located in the project page on XNAT."><figcaption></figcaption></figure>

After selecting the "Manage" tab, Go to the section titled "Anonymization Script". There, you can paste your DicomEdit script. Ensure that the "Enable Script" box is checked, and then press save. Now, all incoming data to this project will have the script applied to it!

<figure><img src="../../.gitbook/assets/Screenshot 2026-07-17 at 10.03.31 AM.png" alt="In the manage tab, there is a section called &#x22;Anonymization Script&#x22;. Here, we have pasted the example DicomEdit script. The &#x22;Enable Script&#x22; box is checked and the &#x22;Save&#x22; button is pressed. "><figcaption></figcaption></figure>

