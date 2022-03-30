# Project Creation in XNAT

Typically, every protocol tree created at the scanner needs will be associated with only one XNAT project. **Currently XNAT Projects can only be created by an BNC XNAT administrator.** This behavior may change in the future as our process becomes more streamlined. However, you should familiarize yourself with XNAT naming conventions below

At the moment all projects **must be created in XNAT relay.** The XNAT's relay is only accessible by administrators and it has automated scripts that will automatically create matching projects in the public instance when a new project is created

## 0. Select New-> Project

In the top bar navigation select New, then Project&#x20;

![](<../.gitbook/assets/image (19).png>)

## 1. Fill Project Details

![Form for filing New Project Details](<../.gitbook/assets/image (22).png>)

Please refer to the [prior section](managing-your-projects.md#xnat-project-title-and-id) to understand **Project Title, Running Title and Project ID**

{% hint style="warning" %}
You will want to add the faculty and primary graduate student as investigators in order to set up access correctly in the public XNAT
{% endhint %}

### 1. 1 Project Primary Investigator and Other Investigators

Project PI and Other Investigators are used to keep record of who the project belongs to. While on the relay side we do not have any users, PI and project investigators on the relay are used to grant access to appropriate users on the public XNAT instance.&#x20;

**Primary Investigator:** The PI should be the faculty who owns the data.&#x20;

**Other Investigators:** Anyone else who needs access to this project on the server. i.e. graduate students, postdocs

#### Creating additional investigators

Select `Create Investigator`

![](<../.gitbook/assets/image (22) (1).png>)

Fill out the form to create a new investigator.&#x20;

{% hint style="warning" %}
If the investigor's First Name and Last Name matches the appropriate user on the xnat server (`xnat.bnc.brown.edu`), then that user will have access to the project. To check the user details on server, log in as administrator on `xnat.bnc.brown.edu` and then go to `Administer -> users`.
{% endhint %}

&#x20;
