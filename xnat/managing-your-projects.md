---
description: Naming your XNAT Project and your Protocol Tree
---

# Project and Protocol Naming

When a session is collected at the scanner, the data will be sent to XNAT and placed in an XNAT Project that is accessible only to the associated researchers. 

## Creating a new project in XNAT

Every protocol should have will need an XNAT project, Currently XNAT Projects can only be created by a BNC XNAT administrator. This behavior may change in the future as our process becomes more streamlined.

### Required fields

When creating new projects, XNAT asks for the following fields

| Variable | Description |
| :--- | :--- |
| Project Title | The full title of the project, which will appear in the site-wide project listing. |
| Running Title | This is an abbreviated project name, which will appear in search listings and data tables. |
| Project ID | This ID is used within the XNAT database and in all API calls related to your project and its data. Once set, it cannot be changed. |

Further details can be found in [this section of XNAT's documentation](https://wiki.xnat.org/documentation/how-to-use-xnat/creating-and-managing-projects)

### Choosing your values

The values we choose have implications on the way that protocols trees must be named at the scanner. More precisely, the `Project ID` entered in XNAT, must match the `Study Desciption` field in the scanner \(shown in the next section\). At the scanner, the `Study Description` is automatically built by concatenating the protocol tree. Traditionally, protocol trees used to be named to easily identify them and they were often re-used among studies. New limitations exist which greatly impact the naming scheme:

1. The protocol tree must start with the PI's brown username
2. The concatenated field for `Study Description` must be at most 13 characters
3. The concatenated field for `Study Description` must be unique

With those considerations in mind, we make the following recommendations

#### **Project Title**

The Project Title should contain the following fields:

1. PI's lastname
2. Study pretty name

The fields should follow that order and be **separated by spaces.** Below we present examples

```text
| PI  | |Ref #| |Name |
Shenhav TSS-TCB
Shenhav TSS-OA
```

#### **Running Title and Project ID**

Both the **Running Title and Project ID** must contain the following fields:

1. PI's short brown name
2. A pretty name that fits the length limit

and follow these rules

* Use ALL CAPS
* Seprate only with underscores
* Maximum of 13 characters

For instance,

```text
ASHENHAV_TCB
ASHENHAV_OA
```

As you can see, the 13 character limits considerably the name that you can choose as an identifier.

## Automated routing from scanner to XNAT

XNAT will attempt to place the data coming from the scanner in the appropiate project using information from the DICOM metadata. At Brown we match the conditions described in [XNAT's Third Pass](https://wiki.xnat.org/documentation/how-to-use-xnat/image-session-upload-methods-in-xnat/how-xnat-scans-dicom-to-map-to-project-subject-session) which relies on matching the Study Description

{% hint style="danger" %}
The only action required at the scanner is to set the **Study Description = XNAT's Project ID.** Typically, this means **replacing a space with underscore**. See image indicating where the Study Description field is in the scanner console
{% endhint %}

{% hint style="info" %}
If no Project was identified, the DICOM files will be placed in the “Unidentified” prearchive box. If Project was identified, but Subject and/or Session was not, the DICOM files will be placed in the appropriate project prearchive box. However, the automatic matching tool will not be functional, and additional data entry will be required.
{% endhint %}

{% hint style="info" %}
We assume that the metadata for the Patient ID and the Patient Name is correctly inferred.
{% endhint %}

![Study Description Field in the Console must match XNAT&apos;s project ID](../.gitbook/assets/img_3251.jpeg)

