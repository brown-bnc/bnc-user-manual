---
description: Naming your XNAT Project and your Protocol Tree
---

# Project and Protocol Naming

When a session is collected at the scanner, the data will be sent to XNAT and placed in an XNAT Project that is accessible only to the associated researchers.&#x20;

{% hint style="warning" %}
For XNAT to route data coming from the scanner to the appropriate project, the XNAT Project ID and the Scanner Protocol tree need to be named consistently
{% endhint %}

### XNAT Project Title and ID

When creating new projects, XNAT asks for the following fields

| Variable      | Description                                                                                                                         |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Project Title | The full title of the project, which will appear in the site-wide project listing.                                                  |
| Running Title | This is an abbreviated project name, which will appear in search listings and data tables.                                          |
| Project ID    | This ID is used within the XNAT database and in all API calls related to your project and its data. Once set, it cannot be changed. |

Further details can be found in [this section of XNAT's documentation](https://wiki.xnat.org/documentation/how-to-use-xnat/creating-and-managing-projects)

### Choosing your values

The values we choose have implications on the way that protocol trees must be named at the scanner. Particularly, the `Project ID` entered in XNAT must match the `Study Description` field in the scanner (shown in the next section). At the scanner, the `Study Description` is automatically built by concatenating the protocol tree. Traditionally, protocol trees were named to be easily identifiable, and they were often reused across multiple studies. However, new limitations exist which greatly impact the naming scheme:

1. The protocol tree must start with the PI's brown username
2. The concatenated field for `Study Description` must be at most 27 characters
3. The concatenated field for `Study Description` must be unique

With those considerations in mind, we make the following recommendations:

#### **Project Title**

The Project Title should contain the following fields:

1. PI's Lastname
2. Custom Study Name

The fields should follow that order and be **separated by spaces.** Below we present examples

```
| PI  | |Ref #| |Name |
Shenhav TSS-TCB
Shenhav TSS-OA
```

#### **Running Title and Project ID**

Both the **Running Title and Project ID** must contain the following fields:

1. PI's Brown Credential (short name)
2. Custom Name (within length limit)

and follow these rules

* Use ALL CAPS
* Separate only with underscores
* Maximum of 13 characters

For instance,

```
ASHENHAV_TCB
ASHENHAV_OA
```

As you can see, the 13 character limits considerably the name that you can choose as an identifier.
