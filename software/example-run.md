---
description: An example of running LCModel on a test data set
---

# Example Run

### 0. Make sure you have installed LCModel

{% hint style="warning" %}
**Every user must install LCModel** for their own user. If you haven't, please refer to the [Installation Guide](lcmodel.md#installing-lcmodel-in-oscar) 
{% endhint %}

### 1. Start a VNC session

To run LCModel's gui you will nedd to start [Oscar's VNC Client](https://docs.ccv.brown.edu/oscar/connecting-to-oscar/vnc). LCModel is not very resource intensive so you can request a basic session

### 2. Launch Terminal 

* Inside your VNC session, open a **Terminal** window.
* Navigate to LCModel's **hidden** directory `cd ~/.lcmodel`

![Sample Terminal Window inside Oscar&apos;s VNC ](../.gitbook/assets/image%20%2810%29.png)

### 3. Launch lcmgui

* To launch the lcmgui, simply type `./lcmgui` from the current directory \(`~/.lcmodel`\)
* Accept license agreement

### 4. Select sample Siemens data 

* Select Siemens at the data type prompt

![Sample Data Type Window](../.gitbook/assets/image%20%2814%29.png)

* Search for the share data: `/gpfs/data/bnc/shared/lcmodel/TestData.rda` 

![Sample Data Browser Window](../.gitbook/assets/image%20%2811%29.png)

### 5. Select Basis

During installation, the basis-set was install under the LCModols' hidden directory in your home. i.e., `$HOME/.lcmodel/basis-set` which is equivalent to `/gpfs/home/$USER/.lcmodel/basis-set`

* Change the basis file to: `$HOME/.lcmodel/basis-sets/press_te30_3t_gsh_v3.basis`

![Sample Control Parameters Window](../.gitbook/assets/image%20%2813%29.png)

### 6. Run LCModel

After pressing **Run LCModel**, a two page PDF will appear, which looks as follows

![LCModel Result PDF - Page 1](../.gitbook/assets/image%20%2812%29.png)

![LCModel Result PDF - Page 2](../.gitbook/assets/image%20%289%29.png)

