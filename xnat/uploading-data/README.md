# Uploading Data

## Uploading data from the scanner

After data collection, data can be sent to XNAT directly from the scanner. Partial data transfers will get stuck, so **transfer an entire scan session at once**, rather than run-by-run. If you are the operator at the console, select your dataset in the patient browser, then click Export.

<figure><img src="../../.gitbook/assets/export.png" alt="View of the Patient Browser on our Siemens MRI console. Data can be exported to XNAT via the &#x22;Export button&#x22; in the top right of the window, or by typing Ctrl-E." width="486"><figcaption></figcaption></figure>

Make sure all the series you want to send are checked, then select XNAT and click Export.

<figure><img src="../../.gitbook/assets/xnat (1).png" alt="View of the pop up window on the Siemens MRI console that appears after selecting &#x22;Export&#x22; in the Patient Browser. In the pop up, you can ensure that each sequence in the MRI session has a checked box next to it, meaning that it is selected to export. Then, check the box next to “XNAT”, and press “Export”. "><figcaption></figcaption></figure>

## Automated routing from scanner to XNAT

If your XNAT project has been created and named to match your protocol on the scanner, XNAT will attempt to place the data coming from the scanner in the appropriate project using information from the DICOM metadata.&#x20;

## Naming for multi-session studies

If your study involves multiple scan sessions per participant, following a specific consistent naming scheme will allow XNAT to nicely organize your data so that each scan session is nested under the the correct participant like this:

<figure><img src="../../.gitbook/assets/Screenshot 2026-03-23 at 12.15.05 PM.png" alt="View of the naming convention on XNAT. Two sessions of data for Demodat2 Subject 101 are labeled &#x22;101_01&#x22; and &#x22;101_02&#x22;. "><figcaption><p>Individual scan sessions ("01" and "02") for Demodat2 participant 101</p></figcaption></figure>

To achieve this, you need to use the Last Name and Patient ID fields in a specific way when you register your participant at the beginning of a scan. In the **Last Name field**, enter the subject ID you have assigned to your participant (in this demodat example, we would enter 005). In the **Patient ID field**, enter the same **subject ID** \*underscore\* **whatever you would like to use to label your different sessions**. You could do "101\_sess1", "101\_sess2", etc., or something that describes the different phases of your study, like "101\_pretraining", "101\_training", "101\_posttraining".

<figure><img src="../../.gitbook/assets/Screenshot (105) (1).png" alt=""><figcaption><p>Using the Patient ID field to enable XNAT to nest multiple sessions under a single participant</p></figcaption></figure>

{% hint style="warning" %}
If you scan the same participant multiple times and re-use the same **Patient ID**, your data will not get properly routed to your project without an XNAT administrator's help.&#x20;
{% endhint %}


## Uploading Non-MR Data

To upload your EEG or Physio data onto XNAT, see the instruction steps at page below.

{% content-ref url="../../xnat-to-bids-intro/converting-non-mr-data/" %}
[converting-non-mr-data](../../xnat-to-bids-intro/converting-non-mr-data/)
{% endcontent-ref %}



