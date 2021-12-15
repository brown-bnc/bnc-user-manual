---
description: Naming your XNAT Project and your Protocol Tree
---

# Project and Protocol Naming

When a session is collected at the scanner, the data will be sent to XNAT and placed in an XNAT Project that is accessible only to the associated researchers.&#x20;

## Creating a new project in XNAT

Typically, every protocol tree created at the scanner needs will be associated with only one XNAT project. Currently XNAT Projects can only be created by an BNC XNAT administrator. This behavior may change in the future as our process becomes more streamlined. However, you should familiarize yourself with XNAT naming conventions below

### XNAT Project Title and ID

When creating new projects, XNAT asks for the following fields

| Variable      | Description                                                                                                                         |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Project Title | The full title of the project, which will appear in the site-wide project listing.                                                  |
| Running Title | This is an abbreviated project name, which will appear in search listings and data tables.                                          |
| Project ID    | This ID is used within the XNAT database and in all API calls related to your project and its data. Once set, it cannot be changed. |

Further details can be found in [this section of XNAT's documentation](https://wiki.xnat.org/documentation/how-to-use-xnat/creating-and-managing-projects)

### Choosing your values

The values we choose have implications on the way that protocols trees must be named at the scanner. More precisely, the `Project ID` entered in XNAT, must match the `Study Desciption` field in the scanner (shown in the next section). At the scanner, the `Study Description` is automatically built by concatenating the protocol tree. Traditionally, protocol trees used to be named to easily identify them and they were often re-used among studies. New limitations exist which greatly impact the naming scheme:

1. The protocol tree must start with the PI's brown username
2. The concatenated field for `Study Description` must be at most 13 characters
3. The concatenated field for `Study Description` must be unique

With those considerations in mind, we make the following recommendations

#### **Project Title**

The Project Title should contain the following fields:

1. PI's lastname
2. Study pretty name

The fields should follow that order and be **separated by spaces.** Below we present examples

```
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

```
ASHENHAV_TCB
ASHENHAV_OA
```

As you can see, the 13 character limits considerably the name that you can choose as an identifier.

### Project Primary Investigator and Other Investigators

Project PI and Other Investigators are used to keep a tab on who the project belongs to. While on the relay side we do not have any users, PI and project investigators on the relay are used to grant access to appropriate users on the server-side.&#x20;

**Primary Investigator:** The PI should be the faculty who owns the data.

**Other Investigators:** Anyone else who needs access to this project on the server. i.e. graduate students, postdocs

#### Creating additional investigators

Select `Create Investigator`

![](<../.gitbook/assets/image (22).png>)

Fill out the form to create a new investigator. Please note that Investigor's First Name and Last Name should match the appropriate user on the xnat server (`xnat.bnc.brown.edu`). To check the user details on server, log in as administrator on `xnat.bnc.brown.edu` and then go to `Administer -> users`.
