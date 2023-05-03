# Uploading Data

Uploading data from the scanner

After data collection, data can be sent to XNAT directly from the scanner. Partial data transfers can sometimes get stuck, so **transfer an entire scan session at once**, rather than run-by-run. If you are the operator at the console, select your dataset in the patient browser, then click Transfer -> Send to -> `XNATRELAY`.

<figure><img src="../.gitbook/assets/Send to capture (1).jpg" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/Transfer selector (1).jpg" alt=""><figcaption></figcaption></figure>

### Automated routing from scanner to XNAT

If your XNAT project has been created and named to match your protocol tree, XNAT will attempt to place the data coming from the scanner in the appropriate project using information from the DICOM metadata. At Brown we match the conditions described in [XNAT's Third Pass](https://wiki.xnat.org/documentation/how-to-use-xnat/image-session-upload-methods-in-xnat/how-xnat-scans-dicom-to-map-to-project-subject-session) which relies on matching the Study Description with the Project ID

{% hint style="danger" %}
Typically there is no action required at the scanner since the protocol tree is concatenated to match the study description. That is **Study Description = XNAT's Project ID.** **Spaces are automatically replaced with underscore upon arrival in XNAT**. See image indicating where the Study Description field is in the scanner console
{% endhint %}

{% hint style="info" %}
If no Project was identified, the DICOM files will be placed in the “Unidentified” prearchive box. If Project was identified, but Subject and/or Session was not, the DICOM files will be placed in the appropriate project prearchive box. However, the automatic matching tool will not be functional, and additional data entry will be required.
{% endhint %}

{% hint style="info" %}
We assume that the metadata for the Patient ID and the Patient Name is correctly inferred.
{% endhint %}

![Study Description Field in the Console must match XNAT's project ID](../.gitbook/assets/IMG\_3251.jpeg)

### Naming for multi-session studies

If your study involves multiple scan sessions per participant, following a specific consistent naming scheme will allow XNAT to nicely organize your data so that each scan session is nested under the the correct participant like this:

<figure><img src="../.gitbook/assets/Screen Shot 2022-10-26 at 11.34.40 AM (1).png" alt=""><figcaption><p>Individual scan sessions ("SESSION1" and "SESSION2") for participant 005</p></figcaption></figure>

To achieve this, you need to use the Last Name and Patient ID fields in a specific way when you register your participant at the beginning of a scan. In the **Last Name field**, enter the subject ID you have assigned to your participant (in this demodat example, we would enter 005). In the **Patient ID field**, enter the same **subject ID** \*underscore\* **whatever you would like to use to label your different sessions**. You could do "005\_sess1", "005\_sess2", etc., or something that describes the different phases of your study, like "005\_pretraining", "005\_training", "005\_posttraining".

<figure><img src="../.gitbook/assets/multisess.JPG" alt=""><figcaption><p>Using the Patient ID field to enable XNAT to nest multiple sessions under a single participant</p></figcaption></figure>

## Uploading historic data (NOT Available at the moment 5/25/21)

### Method 1: Using Globus and XNAT's inbox

This is the preferred method to transfer large amounts of data to the XNAT server. We leverage [Globus](https://www.globus.org) as a secure, fast and resilient transferring service that is enabled for Brown's research storages. If you are not familiar with Globus, you can learn more from Brown's [documentation](https://docs.ccv.brown.edu/globus/).&#x20;

#### Pre-requisites

Before uploading data to a project the following pre-requisites need to be completed

1. The project **must** exist in XNAT
2. You must have signed in into Globus at least once using your Brown's Credentials. To do so, make sure to find Brown University under the list of organizations.![](https://gblobscdn.gitbook.com/assets%2F-LtBPWc3lCoK-ZiQIe15%2F-M54q3ji-pth\_NceEVA5%2F-M54vJLchHgpZLC2CMbL%2Fimage.png?alt=media\&token=e49aa5ef-7a68-418d-8955-6198a510a857)
3. You need to fill in the following [form](https://forms.gle/XhA9c7UssSzBB1NE7) to request data-upload access&#x20;
4. After receiving an email confirmation from XNAT maintainers, you will be able to transfer data using globus.



#### Transfer

{% tabs %}
{% tab title="1. Have your endpoints ready" %}
XNAT's administrator should have shared a new folder in Globus named with your XNAT's Project ID.

You should have the endpoint where your data is currently hosted already set up. Please see [Brown's Documentation](https://docs.brown.edu/globus) for setting up your endpoints for files.brown.edu and Oscar's GPFS.&#x20;
{% endtab %}

{% tab title="2. Organizing the Data" %}
Once you have permissions to the projects folder please organize data as follows

PROJECT\_ID(ROOT)/participant-id/SESSION. For instance to upload data for participant 123 in the SANES SADLUM Data, the organization looks as follows

![](<../.gitbook/assets/image (29).png>)
{% endtab %}

{% tab title="3. Upload" %}
1. Start Globus Transfer
2. Wait for Globus transfer to complete. You should receive a notification
3. Make a REST call to XNAT as follows. For more details on using XNAT's inbox, see [`here`](https://wiki.xnat.org/documentation/how-to-use-xnat/image-session-upload-methods-in-xnat/using-dicom-inbox-to-import-an-image-session)

```
export XNAT_USER=test_user
export PROJECT_ID=SANES_SADLUM
export PARTICIPANT_ID=123

curl -u ${XNAT_USER} -X POST "https://bnc.brown.edu/xnat/data/services/import?import-handler=inbox&cleanupAfterImport=true&PROJECT_ID=${PROJECT_ID}&SUBJECT_ID=${PARTICIPANT_ID}&EXPT_LABEL=${PARTICIPANT_ID}&path=/data/xnat/inbox/${PROJECT_ID}/${PARTICIPANT_ID}" -k
```
{% endtab %}
{% endtabs %}



\




