---
description: An example of running LCModel on a test data set
---

# Example Run

## 0. Make sure you have installed LCModel

{% hint style="warning" %}
**Every user must install LCModel** for their own user. If you haven't, please refer to the [Installation Guide](lcmodel.md#installing-lcmodel-in-oscar)&#x20;
{% endhint %}

## 1. Start a VNC session

To run LCModel's GUI you will need to start [Oscar's VNC Client](https://docs.ccv.brown.edu/oscar/connecting-to-oscar/vnc). LCModel is not very resource intensive so you can request a basic session

## 2. Launch Terminal&#x20;

* Inside your VNC session, open a **Terminal** window.
* Navigate to LCModel's **hidden** directory `cd ~/.lcmodel`

<figure><img src="../../.gitbook/assets/image (27).png" alt="Example terminal in a VNC session (Oscar). The user navigated into the directory called “.lcmodel” and listed its contents with the “ls” command. Notably, “lcmgui” is listed in the directory. "><figcaption><p>Sample Terminal Window inside Oscar's VNC </p></figcaption></figure>

## 3. Launch lcmgui

* To launch the lcmgui, simply type `./lcmgui` from the current directory (`~/.lcmodel`)
* Accept license agreement

## 4. Select sample Siemens data&#x20;

* Select Siemens at the data type prompt

<figure><img src="../../.gitbook/assets/image (5) (1).png" alt="A LC Model pop up window with the title, “Select your data type”. Users should select “Siemens”. "><figcaption><p>Sample Data Type Window</p></figcaption></figure>

* Search for the share data: `/oscar/data/bnc/shared/lcmodel/TestData.rda`&#x20;

<figure><img src="../../.gitbook/assets/image (2) (1).png" alt="In the pop up titled “Select your Siemens file.”, enter your path and RDA file. In this example, the path is: “/oscar/data/bnc/shared/lcmodel/“ and the file is: “TestData.rda”. Then press “Ok”.  "><figcaption><p>Sample Data Browser Window</p></figcaption></figure>

## 5. Select Basis

During installation, the basis-set was installed under the LCModels' hidden directory in your home. i.e., `$HOME/.lcmodel/basis-set` which is equivalent to `/oscar/home/$USER/.lcmodel/basis-set`

* Change the basis file to: `$HOME/.lcmodel/basis-sets/press_te30_3t_gsh_v3.basis`

<figure><img src="../../.gitbook/assets/image (25).png" alt="In the “Control Parameters” pop up, there is a section titled &#x22;BASIS file:&#x22;. In the text box, enter: $HOME/.lcmodel/basis-sets/press_te30_3t_gsh_v3.basis. $HOME should be the path to your individual home directory."><figcaption><p>Sample Control Parameters Window</p></figcaption></figure>

## 6. Add License Key to Control Parameters

You will need to add a key to the Control Parameters. We do so as follows:

1.  Open Advanced Setting Dialog  
    <figure><img src="../../.gitbook/assets/Untitled.png" alt="In the “Control Parameters” pop up, select the “Advanced Settings” button. "><figcaption></figcaption></figure>

2. Select View/Edit Control Parameters.&#x20;  
A dialog will open  

3. Add key to Control Parameters  
Add `key= 210387309` to the control parameters as shown in the figure below. Be careful to match spaces. When done, press OK  
<figure><img src="../../.gitbook/assets/lc-model-params-with-key.png" alt="In the “View/Edit Control Parameters” pop up, a new line was added to the text box, which states: “key= 210387309”."><figcaption></figcaption></figure>

4. Save parameters file (optional)  
LCModel will ask you if you want to save the new parameters to a new file. You can do so. If you do, the next time you can select the saved file from **Advanced Settings -> Change Control-Defaults file**

## 7. Run LCModel

After pressing **Run LCModel**, a two page PDF will appear, which looks as follows

<figure><img src="../../.gitbook/assets/image (9).png" alt="Page 1 of the LC Model PDF, which depicts the metabolite spectra  and a table of metabolite values from the dataset."><figcaption><p>LCModel Result PDF - Page 1</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (3) (1) (1).png" alt="Page 2 of the LC Model PDF, which depicts the same table of metabolite values, without the spectra. Additionally, there are sections on “MISCELLANEOUS OUTPUT” and “INPUT CHANGES”. "><figcaption><p>LCModel Result PDF - Page 2</p></figcaption></figure>
