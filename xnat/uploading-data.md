# Uploading Data

## Uploading data from the scanner

After data collection, data can be sent to XNAT directly from the scanner. If you are the operator at the console, please select:

{% hint style="warning" %}
Details of the console settings coming soon
{% endhint %}

## Uploading historic data

### Method 1: Using Globus and XNAT's inbox

This is the preferred method to transfer large amounts of data to the XNAT server. We leverage [Globus](https://www.globus.org) as a secure, fast and resilient transferring service that is enabled for Brown's research storages. If you are not familiar with Globus, you can learn more from Brown's [documentation](https://docs.ccv.brown.edu/globus/). 

#### Pre-requisites

Before uploading data to a project the following pre-requisites need to be completed

1. The project **must** exist in XNAT
2. You must have signed in into Globus at least once using your Brown's Credentials. To do so, make sure to find Brown University unde the list of organizations.![](https://gblobscdn.gitbook.com/assets%2F-LtBPWc3lCoK-ZiQIe15%2F-M54q3ji-pth_NceEVA5%2F-M54vJLchHgpZLC2CMbL%2Fimage.png?alt=media&token=e49aa5ef-7a68-418d-8955-6198a510a857)
3. You to fill in the following [form](https://forms.gle/XhA9c7UssSzBB1NE7) to request data-upload access 
4. After receiving an email confirmation from XNAT maintainers, you will be able to transfer data using globus.



#### Transfer

{% tabs %}
{% tab title="1. Have you enpoints ready" %}
XNAT's administrator should have shared a new folder in Globus named with you XNAT's Project ID.

You should have the endpoint where you data is currently hosted already set up. Please see [Brown's Documentation](https://docs.brown.edu/globus) for setting up your endpoints for files.brown.edu and Oscar's GPFS. 
{% endtab %}

{% tab title="2. Organizing the Data" %}
Once you have permissions to the projects folder please orgineze data as follows

PROJECT\_ID\(ROOT\)/participant-id/SESSION. For instance to upload data for participant's 123 in the SANES SADLUM Data, the organization looks as follows

![](../.gitbook/assets/image%20%284%29.png)
{% endtab %}

{% tab title="3. Upload" %}
1. Start Globus Transfer
2. Wait for Globus transfer to complete. You should receive a notification
3. Make a REST call to XNAT as follows. For more details on using XNAT's inbox, see [`here`](https://wiki.xnat.org/documentation/how-to-use-xnat/image-session-upload-methods-in-xnat/using-dicom-inbox-to-import-an-image-session)\`\`

```text
export XNAT_USER=test_user
export PROJECT_ID=SANES_SADLUM
export PARTICIPANT_ID=123
export SESSION_LABEL=ses-01

curl -u ${XNAT_USER} -X POST "https://bnc.brown.edu/xnat/data/services/import?import-handler=inbox&cleanupAfterImport=true&PROJECT_ID=${PROJECT_ID}&SUBJECT_ID=${PARTICIPANT_ID}&EXPT_LABEL=${SESSION_LABEL}&path=/data/xnat/inbox/${PROJECT_ID}/${PARTICIPANT_ID}" -k
```
{% endtab %}
{% endtabs %}



  






